from http import HTTPStatus

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View

from .constants import PAGE_SIZE
from .forms import ProjectForm
from .models import Project, StatusChoices


class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"
    paginate_by = PAGE_SIZE

    def get_queryset(self):
        return super().get_queryset().select_related("owner").prefetch_related("participants")


class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project-details.html"
    context_object_name = "project"

    def get_queryset(self):
        return super().get_queryset().select_related("owner").prefetch_related("participants")


class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"
    login_url = reverse_lazy("users:login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = False
        return context

    def form_valid(self, form):
        project = form.save(commit=False)
        project.owner = self.request.user
        project.save()
        project.participants.add(self.request.user)
        return redirect("projects:details", pk=project.id)


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/create-project.html"
    login_url = reverse_lazy("users:login")

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        if project.owner != request.user:
            return redirect("projects:details", pk=project.id)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_edit"] = True
        return context

    def get_success_url(self):
        return reverse_lazy("projects:details", kwargs={"pk": self.object.id})


class FavoriteProjectsListView(LoginRequiredMixin, ListView):
    template_name = "projects/favorite_projects.html"
    context_object_name = "projects"
    login_url = reverse_lazy("users:login")

    def get_queryset(self):
        return self.request.user.favorites.select_related("owner").prefetch_related("participants").all()


class ToggleFavoriteView(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:login")

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))
        favorites = request.user.favorites

        if favorites.filter(pk=project.pk).exists():
            favorites.remove(project)
            is_favorited = False
        else:
            favorites.add(project)
            is_favorited = True

        return JsonResponse({"status": "ok", "favorited": is_favorited})


class ToggleParticipateView(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:login")

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))

        if project.owner == request.user:
            return JsonResponse({"error": "Доступ запрещен"}, status=HTTPStatus.FORBIDDEN)

        if project.status != StatusChoices.OPEN:
            return JsonResponse({"error": "Проект закрыт"}, status=HTTPStatus.BAD_REQUEST)

        participants = project.participants
        if request.user in participants.all():
            participants.remove(request.user)
            is_participant = False
        else:
            participants.add(request.user)
            is_participant = True

        return JsonResponse({"status": "ok", "participant": is_participant})


class CompleteProjectView(LoginRequiredMixin, View):
    login_url = reverse_lazy("users:login")

    def post(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs.get("pk"))

        if project.owner != request.user:
            return JsonResponse({"error": "Доступ запрещен"}, status=HTTPStatus.FORBIDDEN)

        project.status = StatusChoices.CLOSED
        project.save(update_fields=["status"])

        return JsonResponse(
            {"status": "ok", "project_status": StatusChoices.CLOSED.value}
        )
