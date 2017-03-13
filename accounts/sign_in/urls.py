from django.conf.urls import url
from accounts.sign_in.views import SignInUserRegister, SignInUserLogIn

urlpatterns = [
    url(r'^register', SignInUserRegister.as_view(), name='sign_in_register'),
    url(r'^log_in', SignInUserLogIn.as_view(), name='sign_in_log_in'),
]