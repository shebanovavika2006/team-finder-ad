from django.contrib.auth import authenticate, login, logout
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from .constants import USERS_PER_PAGE, UserFilters
from .forms import CustomPasswordChangeForm, LoginForm, ProfileEditForm, RegisterForm
from .models import User
from .services import generate_default_avatar


class UserRegisterView(CreateView):
    model = User
    form_class = RegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("projects:list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("projects:list")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        generate_default_avatar(self.object)
        login(self.request, self.object)
        return response


class UserLoginView(LoginView):
    form_class = LoginForm
    template_name = "users/login.html"
    redirect_authenticated_user = True

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)
        
        if user is not None:
            login(self.request, user)
            return redirect("projects:list")
        
        form.add_error(None, "Указаны неверные данные для входа")
        return self.form_invalid(form)


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("projects:list")


class ParticipantListView(ListView):
    model = User
    template_name = "users/participants.html"
    context_object_name = "participants"
    paginate_by = USERS_PER_PAGE

    def get_queryset(self):
        qs = super().get_queryset()
        active_filter = self.request.GET.get("filter")
        user = self.request.user

        if active_filter and user.is_authenticated:
            if active_filter == UserFilters.FAVORITE_OWNERS:
                qs = qs.filter(owned_projects__in=user.favorites.all())
            elif active_filter == UserFilters.PARTICIPATING_OWNERS:
                qs = qs.filter(owned_projects__participants=user)
            elif active_filter == UserFilters.INTERESTED_IN_MY:
                qs = qs.filter(favorites__owner=user)
            elif active_filter == UserFilters.MY_PARTICIPANTS:
                qs = qs.filter(participated_projects__owner=user)

        return qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_filter"] = self.request.GET.get("filter")
        return context


class UserProfileDetailView(DetailView):
    model = User
    template_name = "users/user-details.html"
    context_object_name = "user"

    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            "owned_projects__owner", 
            "participated_projects__owner"
        )


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileEditForm
    template_name = "users/edit_profile.html"
    login_url = reverse_lazy("users:login")

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse_lazy("users:user_details", kwargs={"pk": self.request.user.pk})


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = "users/change_password.html"
    login_url = reverse_lazy("users:login")

    def get_success_url(self):
        return reverse_lazy("users:user_details", kwargs={"pk": self.request.user.pk})
