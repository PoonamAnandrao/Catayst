from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from .views import LoginView, FileUploadView,filter_csv
from catalyst_app import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

router = DefaultRouter()


urlpatterns = [
    path("",LoginView.as_view(), name = 'home'),
    path('login/', LoginView.as_view(), name='login'),
    path('file_upload/', FileUploadView.as_view(), name='file_upload'),
    path('user_details/', views.user_detail, name='user_details'),
    path('filter/', filter_csv, name='filter_csv'),
    path('filter_page/<int:matching_count>/', TemplateView.as_view(template_name='filter.html'), name='filter_page'),
    path('filter_page/', TemplateView.as_view(template_name='filter.html'), name='filter_page'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('index/', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
     path('add_user/', views.add_user, name='add_user'),

]

urlpatterns += router.urls