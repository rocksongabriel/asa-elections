from django import forms

from .models import Support


class SupportForm(forms.ModelForm):
    """Support Form to let people submit complaints"""

    class Meta:
        model = Support
        fields = ["full_name", "student_id", "email_address", "message"]
