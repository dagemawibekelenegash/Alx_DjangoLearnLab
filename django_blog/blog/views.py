from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import CommentForm
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import PostForm
from .models import Post, Comment


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

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            form = self.get_form()
            if form.is_valid():
                form.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        return super().post(request, *args, **kwargs)


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post=self.object)
        context["comment_form"] = CommentForm()
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    success_url = reverse_lazy("post_list")


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    success_url = reverse_lazy("post_list")


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"

    def test_func(self):
        post = self.get_object()
        return post.author == self.request.user

    success_url = reverse_lazy("post_list")


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs["pk"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)

    def get_success_url(self):
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})
