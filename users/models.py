from django.conf import settings
from django.contrib.auth import get_user, get_user_model
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _

if "mailer" in settings.INSTALLED_APPS:
    from mailer import send_mail
else:
    from django.core.mail import send_mail


# Custom User Manager
class CustomUserManager(UserManager):
    """Custom user manager for the user model"""

    def create_user_account_and_send_mail(self, student_id=None, email=None, campus=None):
        """This method will take a student ID, email, campus and create an account. Then email the credentials to the email"""
        # generate password
        password = self.make_random_password(length=8)
        # create user account
        try:
            self.create_user(username=student_id, email=email, campus=campus, password=password)
            print(f"----------------- Account created for {student_id} -------------------")
        except IntegrityError as e:
            print(f"Error {e} occurred")
        except ValueError as e:
            print(f"Error {e} occurred")
        else:
            # send email
            subject = "Credentials to vote in the ASA Elections 2021"
            message = f"PLEASE USE THIS TO LOG IN\n\nStudent ID: {student_id}\nPassword: {password}\n\nUse it to login so that you can vote."
            send_mail(
                subject=subject,
                message=message, 
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            # Get user and mark user as credentials_sent
            user = get_user_model().objects.get(username=student_id)
            user.credentials_sent = True
            user.save()
            print(f"----------------- Email for {student_id} account sent to {email} successfully --------------------")


class User(AbstractUser):
    """Model to represent a user"""

    MAIN_CAMPUS = "MC"
    CITY_CAMPUS = "CC"

    CAMPUS = (
        (MAIN_CAMPUS, "Main Campus",),
        (CITY_CAMPUS, "City Campus",),
    )

    campus = models.CharField(_("Campus"), choices=CAMPUS, default=MAIN_CAMPUS, max_length=20,
                              help_text="Select the campus the student is on", null=False, blank=False)
    voted = models.BooleanField(default=False)
    credentials_sent = models.BooleanField(_("Credentials Sent"), default=False)

    objects = CustomUserManager()

    def __str__(self):
        return self.username


class UserCredential(models.Model):
    """Model to create a user credential and email the credentials"""

    MAIN_CAMPUS = "MC"
    CITY_CAMPUS = "CC"

    CAMPUS = (
        (MAIN_CAMPUS, "Main Campus",),
        (CITY_CAMPUS, "City Campus",),
    )

    student_id = models.CharField(_("Student ID"), null=False, blank=False, max_length=20, help_text="Enter the Student ID of the student")
    email = models.CharField(_("Email of Student"), null=False, blank=False, max_length=300, help_text="Enter the email address of the student")
    campus = models.CharField(_("Campus"), choices=CAMPUS, default=MAIN_CAMPUS, max_length=20,
                              help_text="Select the campus the student is on", null=False, blank=False)
    
    def __str__(self):
        return self.student_id

    def clean(self):
        try:
            user = get_user_model().objects.get(username=self.student_id)
            if user:
                raise ValidationError("A user with this student ID already exists")
        except ObjectDoesNotExist:
            pass
        return super().clean()

    def save(self, **kwargs):
        get_user_model().objects.create_user_account_and_send_mail(
            student_id=self.student_id, 
            email=self.email, 
            campus=self.campus
        )
        return super().save(**kwargs)

    class Meta:
        verbose_name = "User Credential"
        verbose_name_plural = "User Credentials"
