from django.urls import path
from django.contrib.auth.views import LogoutView, LoginView
from . import views

app_name = 'camps'

urlpatterns = [
    path('', views.camp_list, name='camp_list'),
    path('register/', views.register_user, name='register_user'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('<int:pk>/', views.camp_detail, name='camp_detail'),
    path('<int:pk>/register/', views.register_for_camp, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('login/', LoginView.as_view(template_name='camps/login.html'), name='login'),
] 