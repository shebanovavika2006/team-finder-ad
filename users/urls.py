from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("register/", views.UserRegisterView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    
    path("list/", views.ParticipantListView.as_view(), name="participants"),
    path("<int:pk>/", views.UserProfileDetailView.as_view(), name="user_details"),
    
    path("edit-profile/", views.ProfileUpdateView.as_view(), name="edit_profile"),
    path("change-password/", views.UserPasswordChangeView.as_view(), name="change_password"),
]
