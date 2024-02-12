from django.urls import path
from .views import ItemList, UserSignup, UserLogin, UserLogout

urlpatterns = [
    path('items/', ItemList.as_view(), name='item-list'),
    path('signup/', UserSignup.as_view(), name='user-signup'),
    path('login/', UserLogin.as_view(), name='user-login'),
    path('logout/', UserLogout.as_view(), name='user-logout'),
]
