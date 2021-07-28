from django.core.exceptions import ValidationError
from django.db import models
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.conf import settings
from django.urls import reverse

User = settings.AUTH_USER_MODEL


class Category(models.Model):
    """Model to represent the categories the candidates are in"""

    MAIN_CAMPUS = "MC"
    CITY_CAMPUS = "CC"

    CAMPUS = (
        (MAIN_CAMPUS, "Main Campus",),
        (CITY_CAMPUS, "City Campus",),
    )

    campus = models.CharField(_("Campus"), choices=CAMPUS, default=MAIN_CAMPUS, max_length=20,
                              help_text="Select the campus the student is on", null=False, blank=False)

    name = models.CharField(_("Name of Category"),
                            max_length=50,
                            blank=False,
                            null=False,
                            help_text="Enter the name of the category")
    slug = models.SlugField(_("Slug"),
                            max_length=50,
                            blank=False,
                            null=False,
                            help_text="Slug of the category",
                            unique=True,
                            default="")
    voters = models.ManyToManyField(User, related_name="voted_categories", blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("vote_app:vote", kwargs={"slug": self.slug})

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.get_campus_display()}")
        return super().save(**kwargs)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Candidate(models.Model):
    """Model to represent the candidate"""
    full_name = models.CharField(_("Name of Candidate"),
                                 max_length=50,
                                 blank=False,
                                 null=False,
                                 help_text="Enter the name of the candidate")   
    slug = models.SlugField(max_length=50, default="")
    picture = models.ImageField(_("Picture of Candidate"),
                                blank=False,
                                null=False,
                                upload_to="candidates/pictures/",
                                help_text="Upload the image of the candidate")
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="candidates",
        null=False,
        blank=False,
        help_text="Select the category the candidate belongs to")
    vetting_score = models.FloatField(
        _("Vetting Score"), 
        default=0, 
        help_text="Enter the score the candidate had at vetting, please don't include the percentage sign"
    )
    number_of_votes = models.PositiveIntegerField(_("Number of Votes"),
                                                  default=0)
    yes = models.PositiveBigIntegerField(_("Number of Yeses",), default=0)
    no = models.PositiveIntegerField(_("Number of Nos"), default=0)

    # display picture in admin
    def image_tag(self):
        if self.picture:
            return mark_safe(
                '<img src="%s" style="width: 100px; height:100px;" />' %
                self.picture.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'

    # increase vote of candidate
    def upvote(self, **kwargs):
        self.number_of_votes += 1
        return super().save(**kwargs)

    # increase the yeses
    def yes_vote(self, **kwargs):
        self.yes += 1
        return super().save(**kwargs)

    # increase the nos
    def no_vote(self, **kwargs):
        self.no += 1
        return super().save(**kwargs)

    def save(self, **kwargs):
        self.full_name = " ".join(self.full_name.split())  # Remove any spaces that will mistakenly crawl into the full_name
        self.slug = slugify(self.full_name) # set the slug
        return super().save(**kwargs)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ["-vetting_score"]
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"




class Support(models.Model):
    """Model for the support form"""
    MAIN_CAMPUS = "MC"
    CITY_CAMPUS = "CC"

    CAMPUS = (
        (MAIN_CAMPUS, "Main Campus",),
        (CITY_CAMPUS, "City Campus",),
    )

    full_name = models.CharField(_("Full Name"), max_length=50, help_text="Enter your full name", null=False, blank=False)
    student_id = models.CharField(_("Student ID"), max_length=20, help_text="Enter your ID", null=False, blank=False)
    campus = models.CharField(_("Campus"), choices=CAMPUS, default=MAIN_CAMPUS, max_length=20,
                              help_text="Select your campus", null=False, blank=False)
    email_address = models.EmailField(_("Email Address"), max_length=300, help_text="Enter your email address", blank=False, null=True)
    message = models.TextField(_("Complaint"), max_length=1000, help_text="Enter your message", null=False, blank=False)


    def __str__(self): 
        return f"{self.full_name}, {self.student_id}"

    class Meta:
        verbose_name = "Support Form"
        verbose_name_plural = "Support Forms"



# VOTING AND RESULTS PAGE VIEW CONTROL
class PageControlPanel(models.Model):
    name = models.CharField(_("Name of Panel"), help_text="Enter the name of the panel", max_length=255, null=False, blank=False)
    enable_voting_page = models.BooleanField(_("Enable Voting Page"), help_text="Tick this button if you want people to be able to visit the voting page to vote")
    enable_results_page = models.BooleanField(_("Enable Results Page"), help_text="Tick this box if you want people to be able to view the election results page")

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        if not self.pk and PageControlPanel.objects.exists():
            raise ValidationError("There can be only one instance of Page Control Panel")
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Page Control Panel"
        verbose_name_plural = "Page Control Panel"