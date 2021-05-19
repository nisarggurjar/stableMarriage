from django.urls import path
from .views import *
urlpatterns = [
    path('login/', Login, name='login'),
    path('logout/', Logout, name='logout'),
    path('signup/', Signup, name='signup'),
    path('rooms/', Rooms, name='rooms'),
    path('mess/', Mess, name='mess'),
    path('contactus/', contact, name='contact'),
    path('preferences/',Preferences, name='preferance'),
    path('results/', Results, name='results'),
]
