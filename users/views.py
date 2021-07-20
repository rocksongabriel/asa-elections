from django.urls.base import reverse_lazy
from django.contrib.auth.views import LoginView


# Login form
class UserLoginView(LoginView):
    template_name = "users/login.html"
    redirect_field_name = reverse_lazy("vote_app:vote-categories")
