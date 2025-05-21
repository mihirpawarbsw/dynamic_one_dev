from django.contrib import admin
from django.urls import path,include
from . import views
from .views import UserCreateView
from .views import authenticate_user


urlpatterns = [

    path('',views.indexpage_404,name=' Index page'),#comment if login is not required
    path('login_with_password',views.indexpage,name=' Index page'),#comment if login is not required
    # path('',views.indexpage,name=' Index page'),#comment if login is not required
    path('login',views.login,name=' login page'),
    path('logout',views.logout,name=' logout page'),
	path('api_logout_with_redirect_url',views.api_logout_with_redirect_url,name=' logout page'),
    path('forgot_password',views.forgot_password,name=' forgot_password function'),
    path('recover_password',views.recover_password_view,name=' recover_password View'),
    path('change_password',views.change_password,name=' change_password View'),
    path('user',views.user,name=' users View'),
    path('check_change_password_url_valid',views.check_change_password_url_valid,name=' check_change_password_url_valid View'),
    path('display_users_data',views.display_users_data,name='display_users_data View'),
    # path('landingpage/<str:email>/', views.landingpage), 
    path('landingpage_logic/',views.landingpage_logic),
    path('landingpage/',views.landingpage,name='landingpage'),
    path('useraction',views.useraction,name='useraction page 404 error display'),
    path('user_action',views.user_action,name='user_action page 500 error display'),
    ################# API url start #################
    path('api/users/', UserCreateView.as_view(), name='user-create'),
    path('api/authenticate/', authenticate_user, name='authenticate_user'),
    path('api/verify-token-and-login/', views.verify_token_and_login, name='verify-token-and-login'),
    ################ API url end ####################
]