from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Book, Genre
from .forms import ReadingForm, GenreForm

def home(request):
    return render(request, 'home.html')

def signup(request):
    from django.contrib.auth.forms import UserCreationForm
    from django.contrib.auth import login
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

class BookList(ListView):
    model = Book

class BookDetail(DetailView):
    model = Book
    template_name = 'books/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_genre = Genre.objects.all()
        genre_form = GenreForm()
        reading_form = ReadingForm()
        context['all_genre'] = all_genre
        context['genre_form'] = genre_form
        context['reading_form'] = reading_form
        return context

class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author', 'description', 'pages']

class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author', 'description', 'pages', 'genre']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('book-list')



def associate_genre(request, pk):
    book = Book.objects.get(id=pk)
    selected_genre_ids = request.POST.getlist('genre')

    if selected_genre_ids:
        selected_genre_ids = [int(genre_id) for genre_id in selected_genre_ids]
        book.genre.set(selected_genre_ids)
    else:
        book.genre.clear()

    return redirect('book-detail', pk=pk)


def add_and_associate_genre(request, pk):
    book = Book.objects.get(id=pk)
    form = GenreForm(request.POST)

    if form.is_valid():
        new_genre = form.save()
        book.genre.add(new_genre.id)
        return redirect('book-detail', pk=pk)

# Reading views

def add_reading(request, pk):
    form = ReadingForm(request.POST)
    if form.is_valid():
        new_reading = form.save(commit=False)
        new_reading.book_id = pk
        new_reading.save()
    return redirect('book-detail', pk=pk)


