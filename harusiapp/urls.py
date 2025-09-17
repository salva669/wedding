from django.urls import path
from harusiapp import views, HodViews
from harusi import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path('', views.IndexPageView, name='index'),
    path('login/', views.user_login, name='login'),
    path('ingia/', views.LoginPageView, name='ingia'),
    path('home_content/', HodViews.admin_home, name='home_content'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)