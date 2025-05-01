from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my-login', views.my_login, name='my-login'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('state-user', views.state_user, name="state-user"),
    path('participants',views.participant, name="participants"),
    path ('logout-user', views.logout_user, name="logout-user"),
    path('add-admin', views.add_admin, name="add-admin"),
    path('state-board', views.state_board, name="state-board"),
    path('state-cord', views.state_cord, name="state-cord"),   # the cord means cordinators
    path('state-part', views.state_part, name="state-part"),   # the part means participants
    path('state-pass-change', views.state_password, name="state-pass-change"),


    path('state-forgot-password', views.state_forgot_password, name='state-forgot-password'),
]
