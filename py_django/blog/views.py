from django.conf import settings
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import DetailView, FormView, ListView, TemplateView
from django.views.generic.dates import (
    ArchiveIndexView,
    DayArchiveView,
    MonthArchiveView,
    TodayArchiveView,
    YearArchiveView,
)

from .forms import PostSearchForm
from .models import Post


# template_name_suffix = "_list"
class PostLV(ListView):
    model = Post
    template_name = "blog/post_all.html"
    context_object_name = "posts"
    paginate_by = 2


# template_name_suffix = "_detail"
class PostDV(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["disqus_short"] = f"{settings.DISQUS_SHORTNAME}"
        context["disqus_id"] = f"post-{self.object.id}-{self.object.slug}"
        context["disqus_url"] = f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}"
        context["disqus_title"] = f"{self.object.slug}"
        return context


# template_name_suffix = "_archive"
class PostAV(ArchiveIndexView):
    model = Post
    date_field = "modify_dt"


# template_name_suffix = "_archive_year"
class PostYAV(YearArchiveView):
    model = Post
    date_field = "modify_dt"
    make_object_list = True


# template_name_suffix = "_archive_month"
class PostMAV(MonthArchiveView):
    model = Post
    date_field = "modify_dt"


# template_name_suffix = "_archive_day"
class PostDAV(DayArchiveView):
    model = Post
    date_field = "modify_dt"


# template_name_suffix = "_archive_day"
class PostTAV(TodayArchiveView):
    model = Post
    date_field = "modify_dt"


class TagCloudTV(TemplateView):
    template_name = "taggit/taggit_cloud.html"


class TaggedObjectLV(ListView):
    template_name = "taggit/taggit_post_list.html"
    model = Post

    def get_queryset(self):
        return Post.objects.filter(tags_name=self.kwargs.get("tag"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tagname"] = self.kwargs["tag"]
        return context


class SearchFormView(FormView):
    form_class = PostSearchForm
    template_name = "blog/post_search.html"

    def form_valid(self, form):
        search_word = form.cleaned_data["search_word"]
        post_list = Post.objects.filter(
            Q(title__icontains=search_word)
            | Q(description__icontains=search_word)
            | Q(content__icontains=search_word)
        ).distinct()

        context = {
            "form": form,
            "search_term": search_word,
            "object_list": post_list,
        }
        return render(self.request, self.template_name, context)
