from django.views.generic import DetailView, ListView

from .models import Bookmark


class BookmarkLV(ListView):
    model = Bookmark


class BookmarkDV(DetailView):
    model = Bookmark
