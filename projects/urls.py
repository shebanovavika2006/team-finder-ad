from django.urls import path

from . import views

app_name = "projects"

urlpatterns = [
    path("", views.ProjectListView.as_view(), name="list"),
    path("projects/list/", views.ProjectListView.as_view(), name="list_alias"),
    path("projects/create-project/", views.ProjectCreateView.as_view(), name="create"),
    path("projects/<int:pk>/", views.ProjectDetailView.as_view(), name="details"),
    path("projects/<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="edit"),
    
    path("favorites/", views.FavoriteProjectsListView.as_view(), name="favorites"),
    path("projects/favorites/", views.FavoriteProjectsListView.as_view(), name="favorites_alias"),
    path("projects/<int:pk>/toggle-favorite/", views.ToggleFavoriteView.as_view(), name="toggle_favorite"),
    
    path("projects/<int:pk>/toggle-participate/", views.ToggleParticipateView.as_view(), name="participate"),
    path("projects/<int:pk>/complete/", views.CompleteProjectView.as_view(), name="complete"),
]
