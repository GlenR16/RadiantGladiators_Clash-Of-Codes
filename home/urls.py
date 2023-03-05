from django.contrib import admin
from django.urls import path,include
from .views import IndexView,LoginView,LogoutView,SignupView,PasswordChangeView,DashboardView,FaviconView,ProfileView,RecommendedView,get_otp,check_otp,APIView


urlpatterns = [
    path("",IndexView.as_view(),name="index"), # Landing page that user will see.
    path("login/",LoginView.as_view(),name="login"), # User can login here.
    path("logout/",LogoutView.as_view(),name="logout"), # User can logout here.
    path("signup/",SignupView.as_view(),name="signup"), # User can signup here.
    path("profile/",ProfileView.as_view(),name="profile"), # User can view/change profile here.
    path("recommended/",RecommendedView.as_view(),name="recommended"), # User can view recommended profiles.
    path("get_otp/",get_otp,name="getotp"), # User can request otp.
    path("check_otp/",check_otp,name="checkotp"), # User can check their otp.
    #path("change_password/",PasswordChangeView.as_view(),name="change_password"), # User can change their password here.
    path("dashboard/",DashboardView.as_view(),name="dashboard"), # Main Dashboard here.
    path("api/",APIView,name="api"), # API  here.
    path('favicon.ico', FaviconView),
]