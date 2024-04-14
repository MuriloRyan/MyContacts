from django.urls import path

from . import views

urlpatterns = [
    path('api/login', views.api_login, name="database_login"),
    path('api/register', views.api_register, name='database_register'),
    path('api/validate/token', views.api_validate_token, name='token_validation'),
    path('api/logoff', views.api_logoff, name='api_logoff'),

    path('api/create/contact', views.create_contact, name='database_create_token')
]