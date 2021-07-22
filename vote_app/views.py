from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Candidate, Category, PageControlPanel

User = get_user_model()
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")


class VotingCategoriesListPage(CustomLoginRequiredMixin, TemplateView):
    """view for displaying the various categories to vote in"""
    template_name = "vote/new-voting-categories-list.html"
    model = Category
    context_object_name = "categories"
    login_url = reverse_lazy("users:login")

    def get(self, request, *args, **kwargs):
        control_panel = PageControlPanel.objects.first()
        
        if control_panel.enable_voting_page:
            voter = request.user
            context = {
                # fetch categories only of the user
                "categories": self.model.objects.filter(campus=voter.campus).exclude(voters=voter), # remove the categories the voter has already voted in
                "user": request.user
            }
            if context["categories"].count() > 0:
                return render(request, self.template_name, context)
                
            else:
                # Mark the user as voted
                user = get_user_model().objects.get(username=voter.username)
                user.voted = True
                user.save()
                return render(request, template_name="vote/new-voting-completed.html")
        return render(request, "vote/new-vote-page-disabled.html")


class VotingPage(CustomLoginRequiredMixin, TemplateView):
    """view for the voting page"""
    template_name = "vote/new-vote-page.html"
    success_url = reverse_lazy("vote_app:vote-categories")

    CandidateInlineFormset = inlineformset_factory(Category,
                                                   Candidate,
                                                   fields=(
                                                       "full_name",
                                                       "picture",
                                                   ),
                                                   extra=0,
                                                   can_delete=False)

    def post(self, request, slug):
        category = Category.objects.get(slug=slug)
        formset = self.CandidateInlineFormset(request.POST,
                                              request.FILES,
                                              instance=category)

        # Vote Yes / No when it is only one candidate
        if category.candidates.count() == 1:
            for key in request.POST.keys():
                if 'upvote' in key:
                    # Get the full name from the key
                    full_name = " ".join([name.capitalize() for name in key.split("_")[1].split("-")])
                    # Get the candidate's full name
                    candidate = Candidate.objects.get(full_name=full_name)
                    # Increase the yes count of the candidate
                    candidate.yes_vote()
                elif 'downvote' in key:
                    # Get the full name from the key
                    full_name = " ".join([name.capitalize() for name in key.split("_")[1].split("-")])
                    # Get the candidate's full name
                    candidate = Candidate.objects.get(full_name=full_name)
                    # Increase the no count of the candidate
                    candidate.no_vote()
        else: # Increase number of votes
            # Get the upvote key if we are working with multiple candidates
            for key in request.POST.keys():
                if 'upvote' in key:
                    # Get the full name from the key
                    full_name = " ".join([name.capitalize() for name in key.split("_")[1].split("-")])
                    # Get the candidate using the full name
                    candidate = Candidate.objects.get(full_name=full_name)
                    # Upvote the candidate 
                    candidate.upvote()

        # Get the user and add him to the voters of the category
        voter = request.user
        
        # Add the voter to the category's voters
        category.voters.add(voter)

        # Check the forms validity and save it
        if formset.is_valid():
            formset.save()
        return HttpResponseRedirect(self.success_url)

    def get(self, request, slug):
        control_panel = PageControlPanel.objects.first()
        if control_panel.enable_voting_page:
            user = request.user
            category = Category.objects.get(slug=slug)

            # Check if the user has voted in the category already and redirect him if he has
            if user.username in [voter.username for voter in category.voters.filter(username__search=user.username)]:
                return render(request, template_name="vote/new-already-voted.html", context={"user": user})

            formset = self.CandidateInlineFormset(instance=category)
            context = {"category": category, "formset": formset}
            if context["category"].candidates.count() == 1:
                return render(request, "vote/new-vote-page-individual.html", context)
            return render(request, self.template_name, context)
        return render(request, "vote/new-vote-page-disabled.html")


# Election Results
class AllCategoriesResultsPageView(TemplateView):
    """view for the results"""
    template_name = "vote/new-results-all-categories-display.html"
    model = Category
    
    def get(self, request, **kwargs):
        voter=request.user
        control_panel = PageControlPanel.objects.first()
        if control_panel.enable_results_page:
            context = {
                "categories": self.model.objects.filter(campus=voter.campus)
            }
            return render(request, self.template_name, context)
        return render(request, "vote/new-results-page-disabled.html")


class ResultPageView(DetailView):
    """view for the result of an individual portfolio"""
    template_name = "vote/new-result-page.html"
    model = Category
    context_object_name = "category"

    def get(self, request, slug):
        control_panel = PageControlPanel.objects.first()
        if control_panel.enable_voting_page:
            category = Category.objects.get(slug=slug)
            if category.candidates.count() == 1: # If it is only one candidate, render a different template
                return render(request, "vote/new-result-page-individual.html", {"category": category})
            return render(request, self.template_name, {"category": category})