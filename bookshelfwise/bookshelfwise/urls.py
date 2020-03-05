"""bookshelfwise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path

from books.views import BookList, BookCreateUpdate, GoogleBookAPISearch, BookAPIList, index

urlpatterns = [
    path("", index, name="index"),
    path('admin/', admin.site.urls),
    re_path(r'^books', BookList.as_view(), name="browse"),
    re_path(r'^update/(?P<pk>\d+)?', BookCreateUpdate.as_view(), name="create-update"),
    path('expand', GoogleBookAPISearch.as_view(), name="expand"),
    path('api/books', BookAPIList.as_view(), name="api"),
]
