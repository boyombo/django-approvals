"""apapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
from sample import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('edit_author/<int:pk>/', views.edit_author, name='edit_author'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
]
