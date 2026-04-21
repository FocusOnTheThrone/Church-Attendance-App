from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('switch-organization/', views.switch_organization_view, name='switch_organization'),
    path('logout/', views.custom_logout_view, name='logout'),
    path('password-change/', auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('accounts:password_change_done')), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
