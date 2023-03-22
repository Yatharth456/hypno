from django.urls import path
from user_auth import views


urlpatterns = [
    path('signup/', views.Register.as_view(), name='signup'),
    path('confirm/',views.UserVerification.as_view(), name='confirm'),
    path('signin/', views.Login.as_view(), name='signin'),
    path('update-password/', views.UpdatePasswordAPIView.as_view(), name='update_password'),
    path('admin-users/', views.UserAdminView.as_view(), name='user_admin'),
    path('admin-users/<int:pk>/', views.UserAdminView.as_view(), name='user-detail'),
    path('user/<int:pk>/', views.UserView.as_view(), name='get_or_disable1'),
]
