from django.urls import path
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView

urlpatterns = [
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),
    path('signup/', views.registration, name='signup'),
    path('userpro/', views.userProfile, name='userprofile'),
    path('ownerprofile/', views.ownerprofile, name='ownerprofile'),
    path('password/', views.change_password, name='password'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    
    path('reset/password/', PasswordResetView.as_view(template_name = 'session/reset_password.html'), name='password_reset'),
    path('reset/password/done/', PasswordResetDoneView.as_view(template_name = 'session/reset_password_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name = 'session/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(template_name = 'session/password_reset_complete.html'), name='password_reset_complete'),
     
     
]
