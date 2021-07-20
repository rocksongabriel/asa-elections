from django.urls import path

from .views import (AllCategoriesResultsPageView, ResultPageView,
                    VotingCategoriesListPage, VotingPage)

app_name = "vote_app"
urlpatterns = [
    path("election-categories/", VotingCategoriesListPage.as_view(), name="vote-categories"),
    path("election-categories/<slug:slug>/add-new-vote/", VotingPage.as_view(), name="vote"),

    path("election-results/", AllCategoriesResultsPageView.as_view(), name="results"),
    path("election-results/category/<slug:slug>/", ResultPageView.as_view(), name="result"),
]
