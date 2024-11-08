from django.shortcuts import render
from .models import Book
from .models import Library
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from .forms import BookForm


def list_books(request):
    books = Book.objects.all()  # Get all books
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"


class CustomLoginView(LoginView):
    template_name = "relationship_app/login.html"


class CustomLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


def list_books(request):
    book = Book.objects.all()
    context = {"books": book}
    return render(request, "relationship_app/list_books.html", context)


def role_required(role):
    def decorator(user):
        return hasattr(user, "userprofile") and user.userprofile.role == role

    return decorator


@user_passes_test(role_required("Admin"))
def admin_view(request):
    context = {
        "role": "Admin",
        "message": "Welcome, Admin!",
        "total_books": 150,
        "total_members": 50,
        "total_librarians": 5,
    }
    return render(request, "relationship_app/admin_view.html", context)


@user_passes_test(role_required("Librarian"))
def librarian_view(request):
    context = {
        "role": "Librarian",
        "message": "Welcome, Librarian!",
        "assigned_books": 120,
        "total_members": 50,
    }
    return render(request, "relationship_app/librarian_view.html", context)


@user_passes_test(role_required("Member"))
def member_view(request):
    context = {
        "role": "Member",
        "message": "Welcome, Member!",
        "borrowed_books": 5,
        "membership_expiration": "2024-12-31",
    }
    return render(request, "relationship_app/member_view.html", context)


@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "add_book.html", {"form": form})


@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "edit_book.html", {"form": form, "book": book})


@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "delete_book.html", {"book": book})
