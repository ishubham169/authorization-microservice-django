from django.urls import path
from django.conf.urls import include
from .views import sign_up, login


urlpatterns = [
    path('sign_up/', sign_up),
    path('login/', login),

]
