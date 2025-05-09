from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # super users
    path('dashboard', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),

    path('state-user', views.state_user, name="state-user"),
    path('participants',views.participant, name="participants"),
    path('add-admin', views.add_admin, name="add-admin"),
    path('state-user-view/<int:pk>', views.state_user_view, name="state-user-view"),
    path('state-user-delete/<int:pk>', views.state_user_delete, name="state-user-delete"),
    path('post-detail/<int:pk>', views.post_detail, name='post-detail'),
    path('registered-state/<str:state_code>/', views.registered_state, name="registered-state"),
    path('registered-state/<str:state>/', views.registered_state_view, name='registered-state'),
    path('post/', views.post, name='post'),
    path('post-view/<int:pk>', views.post_view, name='post-view'),
    path('post-edit/<int:pk>', views.post_edit, name='post-edit'),
    path('post-delete/<int:pk>', views.post_delete, name='post-delete'),
    

    # state ceditnators
    path('state-board', views.state_board, name="state-board"),
    path('state-cord', views.state_cord, name="state-cord"),   
    path('state-part', views.state_part, name="state-part"),   
    path('state-part-view/<int:pk>', views.state_part_view, name="state-part-view"),   
    path('update-part/<int:pk>', views.update_part, name="update-part"),   
    path('delete-part/<int:pk>', views.delete_part, name="delete-part"), 
    



    # password and logs
    path('my-login', views.my_login, name='my-login'),
    path ('logout-user', views.logout_user, name="logout-user"),
    path('state-pass-change', views.state_password, name="state-pass-change"),
    path('state-forgot-password', views.state_forgot_password, name='state-forgot-password'),
    
]
