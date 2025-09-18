from django.urls import path
from harusiapp import views, HodViews
from harusi import settings
from django.conf.urls.static import static
from django.contrib import admin


urlpatterns = [
    path('', views.IndexPageView, name='index'),
    #path('login/', views.user_login, name='login'),
    path('ingia/', views.LoginPageView, name='ingia'),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user,name="logout"),
    path('doLogin',views.doLogin,name="do_login"),
    path('admin_home',HodViews.admin_home,name="admin_home"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)