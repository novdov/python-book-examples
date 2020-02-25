"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, re_path

from . import views

app_name = "blog"
urlpatterns = [
    # /blog/
    path("", views.PostLV.as_view(), name="index"),
    # /blog/post/
    path("post/", views.PostLV.as_view(), name="post_list"),
    # /blog/posts/django-example/
    re_path(r"^post/(?P<slug>[-\w]+)/$", views.PostDV.as_view(), name="post_detail"),
    # /blog/archive/
    path("archive/", views.PostAV.as_view(), name="post_archive"),
    # /blog/archive/2020/
    path("archive/<int:year>/", views.PostYAV.as_view(), name="post_year_archive"),
    # /blog/archive/2020/fab/
    path("archive/<int:year>/<str:month>/", views.PostMAV.as_view(), name="post_month_archive"),
    # /blog/archive/2020/fab/23/
    path(
        "archive/<int:year>/<str:month>/<int:day>/",
        views.PostDAV.as_view(),
        name="post_day_archive",
    ),
    path("archive/today/", views.PostTAV.as_view(), name="post_today_archive"),
    # /blog/tag/
    path("tag/", views.TagCloudTV.as_view(), name="tag_cloud"),
    # /blog/tag/tag_name/
    path("tag/<str:tag>/", views.TaggedObjectLV.as_view(), name="tagged_object_list"),
]
