from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import permission_required
from .models import Document
from .forms import DocumentForm
from .templates.bookshelf import book_list
from .forms import ExampleForm


@permission_required("bookshelf.can_view", raise_exception=True)
def document_list(request):
    documents = Document.objects.all()
    return render(request, "document_list.html", {"documents": documents})


@permission_required("bookshelf.can_view", raise_exception=True)
def document_detail(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    return render(request, "document_detail.html", {"document": document})


@permission_required("bookshelf.can_create", raise_exception=True)
def document_create(request):
    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("document_list")
    else:
        form = DocumentForm()
    return render(request, "document_form.html", {"form": form})


@permission_required("bookshelf.can_edit", raise_exception=True)
def document_edit(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == "POST":
        form = DocumentForm(request.POST, instance=document)
        if form.is_valid():
            form.save()
            return redirect("document_detail", document_id=document.id)
    else:
        form = DocumentForm(instance=document)
    return render(request, "document_form.html", {"form": form})


@permission_required("bookshelf.can_delete", raise_exception=True)
def document_delete(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    if request.method == "POST":
        document.delete()
        return redirect("document_list")
    return render(request, "document_confirm_delete.html", {"document": document})
