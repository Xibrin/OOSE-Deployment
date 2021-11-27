from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_view, name="user"),
    path('profile', views.profile_view, name="profile"),

    # User Creation and Authentication
    path('login', views.login_view, name="login"),
    path('logout', views.logout_view, name="logout"),
    path('register', views.register_view, name="register"),
    path('preferences', views.preferences_view, name="preferences"),

    # Search Events
    path('search', views.search_view, name="search"),
    path('search/events', views.events_view, name="events"),
]