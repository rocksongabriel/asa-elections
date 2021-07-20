from django.shortcuts import render
from django.views.generic import TemplateView
from vote_app.forms import SupportForm
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template, render_to_string
from django.utils.html import strip_tags


class HomePage(TemplateView):
    template_name = "pages/homepage.html"
    form_class = SupportForm

    def support_request_mail(self, full_name, student_id, email_address, msg):
        email_template = "vote/email/support-submitted.html"
        subject = "Voter with Issue"
        context = {
            "full_name": full_name,
            "student_id": student_id,
            "email_address": email_address,
            "msg": msg
        }
        html_message = render_to_string(email_template, context=context)
        plain_message = strip_tags(html_message)
        return send_mail(
            subject,
            plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            html_message=html_message,
            fail_silently=False
        )
    

    def get(self, request, **kwargs):
        context = {
            "form": self.form_class()
        }
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # TODO - email the admins the issue, or send them an sms or something of the sort
            form.save()
            self.support_request_mail(
                form.cleaned_data["full_name"],
                form.cleaned_data["student_id"],
                form.cleaned_data["email_address"],
                form.cleaned_data["message"]
            )
            return render(request, template_name="pages/complaint-submitted.html")
        return render(request, self.template_name, {"form": form})

