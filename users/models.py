from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user, get_user_model


# Custom User Manager
class CustomUserManager(UserManager):
    """Custom user manager for the user model"""

    def create_user_account_and_send_mail(self, student_id=None, email=None, campus=None):
        """This method will take a student ID, email, campus and create an account. Then email the credentials to the email"""
        # generate password
        password = self.make_random_password(length=8)
        # create user account
        self.create_user(username=student_id, email=email, campus=campus, password=password)
        # send email
        subject = "Credentials to vote in the ASA Elections 2021"
        message = f"Student ID: {student_id}\nPassword:{password}\n\nUse it to login so that you can vote."
        send_mail(
            subject=subject,
            message=message, 
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        print("Account Created for {student_id} and Email Sent to {email} Successfully")



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

    objects = CustomUserManager()

    def __str__(self):
        return self.username


