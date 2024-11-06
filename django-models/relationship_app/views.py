from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseForbidden

# Create your views here.


def list_books(request):
    books = Book.objects.all()  # Get all books
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


class CustomLoginView(LoginView):
    template_name = "login.html"


class CustomLogoutView(LogoutView):
    template_name = "logout.html"


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "register.html", {"form": form})


def is_admin(user):
    return user.userprofile.role == "Admin"


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "admin_view.html")


def is_librarian(user):
    return user.userprofile.role == "Librarian"


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "librarian_view.html")


def is_member(user):
    return user.userprofile.role == "Member"


@user_passes_test(is_member)
def member_view(request):
    return render(request, "member_view.html")
