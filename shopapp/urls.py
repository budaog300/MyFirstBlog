from django.contrib import admin
from django.contrib.auth.views import PasswordChangeView, PasswordResetView, PasswordChangeDoneView, \
    PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView
from django.urls import path, re_path, reverse_lazy
from . import views
from django.conf import settings

from .forms import CustomPasswordRestForm

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contacts/', views.contacts, name='contacts'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile_pk'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('article/post/<int:post_id>/', views.show_post, name='post'),
    path('all_posts/', views.all_posts, name='all_posts'),
    path('category/<int:cat_id>/', views.show_category, name='category'),
    path('popular_posts/', views.popular_posts, name='popular_posts'),
    path('search_results/', views.search_results_view, name='search_results'),
    path('popular_posts/', views.popular_posts, name='popular_posts'),
    path('users_view/', views.users_view, name='users_view'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    re_path(r'^logout/$', views.logout_view, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

    # Сброс пароля внутренний
    path('password-change/', PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', PasswordChangeDoneView.as_view(template_name="registration/password_change_done.html"), name='password_change_done'),

    # Сброс пароля по почте
    path('password-reset/',
         PasswordResetView.as_view(
             template_name="registration/password_reset_form.html",
             email_template_name="registration/password_reset_email.html",
             success_url=reverse_lazy("password_reset_done"),
             form_class=CustomPasswordRestForm
         ),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(
             template_name="registration/password_reset_confirm.html",
             success_url=reverse_lazy("password_reset_complete")
         ),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"),
         name='password_reset_complete'),

    # Тестовая страница
    path('test/', views.test_view, name='test'),
]
