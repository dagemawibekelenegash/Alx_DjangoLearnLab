from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render


class UserLoginView(LoginView):
    template_name = "blog/login.html"


class UserLogoutView(LogoutView):
    template_name = "blog/logout.html"


class UserRegisterView(CreateView):
    template_name = "blog/register.html"
    form_class = UserCreationForm
    success_url = reverse_lazy("login")


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = "blog/profile.html"
    model = User
    form_class = UserChangeForm
    success_url = reverse_lazy("profile")

    def get_object(self, queryset=None):
        return self.request.user
