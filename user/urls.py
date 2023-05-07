from django.urls import path
from django.contrib.auth import views as auth_views
from user.forms import UserLoginForm

from . import views

urlpatterns = [
    path('register/', views.register, name='user-register'),
    path('login/', auth_views.LoginView.as_view(template_name='user/login.html', authentication_form=UserLoginForm), name='user-login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'), name='user-logout'),
    path('profile/', views.profile, name='user-profile'),
    path('admin_update_list/<int:position_type>', views.admin_update_list, name='user-admin_update_list'),
    path('admin_update/<int:user_id>', views.admin_update, name='user-admin_update'),
]