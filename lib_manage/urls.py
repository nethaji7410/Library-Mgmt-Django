from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('' , views.signup),
    path('login' ,views.login),
    path('verify_otp',views.verify_otp),
    path('signout',views.signout,name='signout'),
    path("home",views.home,name="home"),
    path("home",views.home,name="home"),
    path("readers",views.readers,name="readerspage"),
    path("save_student/",views.save_student,name="save_student"),

]
