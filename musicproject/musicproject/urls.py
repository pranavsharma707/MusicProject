"""musicproject URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from musicapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.register),
    path('home/',views.home,name='home'),
    path('music/',views.show,name='music'),
    path('play/<int:id>/',views.play, name="play"),
    path('login/',views.user_login),
    path('logout/',views.user_logout),
    path('comment/<int:id>/',views.comment,name='comment'),
    # path('likes/<int:pk>/',views.likes,name='likes'),
    path('likes/',views.likes,name='likes')
    # path('reply/',views.reply,name='reply'),
    # path('dislikes/<int:pk>/',views.dislikes,name='dislikes')
    ]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    