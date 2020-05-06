from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name="userLogin"),
    path('signup/', views.registerView, name="userSignup"),
    path('logout/', views.logoutView, name="logout")
]
