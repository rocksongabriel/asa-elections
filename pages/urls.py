from django.urls import path

from .views import HomePage, ElectoralCommissionBoardPage

app_name="pages"
urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("electoral-commission-board-members/", ElectoralCommissionBoardPage.as_view(), name="ec-board-page")
]
