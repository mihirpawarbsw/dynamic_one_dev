
import json
import os
import time
import re
import pandas as pd
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from io import StringIO
from django.contrib.sessions.models import Session
from django.db import connection
from matplotlib import pyplot as plt
import warnings
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login as dj_login, logout as del_logout, get_user_model, \
    update_session_auth_hash
from django.db import connection
from datetime import date
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
import webbrowser
from django.contrib.auth.decorators import login_required
from django.utils.timezone import make_aware
from django.conf import settings
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta
warnings.filterwarnings('ignore')
import hashlib
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import logging
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse  # For named URL redirection
from rest_framework.response import Response  # Import for DRF response

# Create your views here.
def indexpage_404(request):
    return render(request,'404.html')

def useraction(request):
    return render(request,'404.html')

def user_action(request):
    return render(request,'500.html')

def indexpage(request):
    return render(request,'index.html')

def login_old(request):
    # import pandas as pd
    if request.method == 'POST':

        loginemail = request.POST['email']
        loginpassword = request.POST['password']
        user = authenticate(username=loginemail, password=loginpassword)
        if user is not None:
            request.session['is_logged'] = True
            username = user.username
            email = user.email
            user_id = user.id
            print('if============',user)
            return redirect('/landingpage', {'title': 'upload-data'})
        else:
            print('else====')
            messages.error(request, 'Invalid Username And Password')
            return redirect(settings.HOMEPAGE_REDIRECT_URL)

def login(request):
    # import pandas as pd
    if request.method == 'POST':
        loginemail = request.POST['email']
        loginpassword = request.POST['password']
        UserModel = get_user_model()
        
        # print('user1---->',user1)
        # user = authenticate(username=user1, password=loginpassword)
        try:
            user1 = UserModel.objects.get(email=loginemail)
            # user = authenticate(username=user1, password=loginpassword)
            user = authenticate(username=user1, password=loginpassword)
            print('TRy block====================>')
        except UserModel.DoesNotExist:
            print('except block====================>')
            user = None

        # print(user)
        # exit()
        if user is not None:
            username=user.username
            email=user.email
            user_id=user.id
            logintime=datetime.now()
            request.session['user_id'] =user_id

            
            # query = "INSERT INTO user_log_details (user_id,username,email,login_time) VALUES('" + str(user_id) + "','" + str(username) + "','" + str(email) + "','" + str(logintime)+ "')"
            # # print(query)
            # cursor = connection.cursor()
            # cursor.execute(query)

            
            if user.is_active:
                dj_login(request, user,backend='django.contrib.auth.backends.ModelBackend')
                request.session['is_logged']= True
                return redirect('/landingpage')   
                # return redirect('/main_dashboard')   
 
            else:
                messages.error(request,'Invalid email and password')
                return redirect(settings.HOMEPAGE_REDIRECT_URL)
        else:
            # print('123')
            messages.error(request, 'Invalid email and password')
            return redirect(settings.HOMEPAGE_REDIRECT_URL)
    return render(request,'index.html',{'title':'index'})


# def landingpage(request):
#     # if request.session.has_key('is_logged'):
#     #     username1 = request.user.username
#     #     return render(request,'landingpage.html',{'username':username1})
#     # return redirect(settings.HOMEPAGE_REDIRECT_URL)
# def landingpage(request):
#     # Retrieve the email from query parameters
#     login_email = request.GET.get('email')
    
#     # Check if the user is already logged in
#     if request.session.get('is_logged'):
#         username = request.user.username
#         return render(request, 'landingpage.html', {'username': username})
#     else:
#         # Handle missing or invalid email
#         if not login_email or '@' not in login_email:
#             return render(request, '404.html', status=404)
#         else:
#             # Check if the email exists in the database
#             try:
#                 with connection.cursor() as cursor:
#                     cursor.execute("SELECT EXISTS(SELECT 1 FROM auth_user WHERE email=%s)", [login_email])
#                     exists = cursor.fetchone()[0]

#                 if exists:
#                     UserModel = get_user_model()
#                     user = get_object_or_404(UserModel, email=login_email)
                    
#                     # Authenticate the user (password is hardcoded for simplicity)
#                     # Ideally, the password should be securely handled
#                     user = authenticate(username=user.username, password='test')
#                     # user = authenticate(username=user.username, password='Bc$!T00l@2024')
                    
#                     if user and user.is_active:
#                         dj_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#                         request.session['is_logged'] = True
#                         return render(request, 'landingpage.html', {'username': user.username})
#                     else:
#                         return render(request, '404.html', status=404)
#                 else:
#                     return render(request, '404.html', status=404)

#             except Exception as e:
#                 # Optionally log the exception
#                 return render(request, '500.html', status=500)

# @login_required(login_url='/')
# def logout(request):
#     del request.session['is_logged']
#     del_logout(request)
#     return redirect(settings.HOMEPAGE_REDIRECT_URL)

# @login_required(login_url='/')
def logout(request):
    
    del_logout(request)
    auth_logout(request)
    # Optionally, delete session data if needed (though auth_logout handles it)
    if 'is_logged' in request.session:
        del request.session['is_logged']
    # return redirect('http://apps.brand-scapes.com/onedashboard/logout')
    # return redirect('https://shiseido.brand-scapes.com/logout')
    # return redirect(settings.HOMEPAGE_REDIRECT_URL)

    # Get the host of the current request
    # host = request.get_host()
    # Get the host from session if it exists, otherwise get from request
    host = request.session.get('host_url', request.get_host())
    print('host--------->',host)

    # Check for different hosts and redirect accordingly
    # if host == '127.0.0.1:8000':
    #     return redirect(settings.HOMEPAGE_REDIRECT_URL)
    # elif host == 'http://apps.brand-scapes.com':
    #     return redirect('http://apps.brand-scapes.com/onedashboard/logout')
    # elif host == 'https://shiseido.brand-scapes.com':
    #     return redirect('https://shiseido.brand-scapes.com/logout')
    return redirect(settings.HOMEPAGE_REDIRECT_URL)


def md5_email(email):
    # Convert the email address to bytes
    email_bytes = email.encode('utf-8')

    # Create an MD5 hash object
    md5_hash = hashlib.md5()

    # Update the hash object with the email bytes
    md5_hash.update(email_bytes)

    # Get the hexadecimal representation of the MD5 hash
    md5_hexdigest = md5_hash.hexdigest()

    return md5_hexdigest


def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        key_email = md5_email(email)
        check_mail_id = "Select id from auth_user where email='"+str(email)+"'"
        print('check_mail_id',check_mail_id)
        
        cursor = connection.cursor()
        cursor.execute(check_mail_id)
        rows1 = cursor.fetchone()
        print('check_mail_id',rows1)
        if rows1 is not None:
            print("Row data:", rows1)
            # TRIM('"+ str( 'username') +"'),TRIM('"+str('email')+"')
            query = "INSERT INTO password_reset_temp(email,key_tem) VALUES (TRIM('"+ str(email) +"'),'" + str(key_email) + "')"
            cursor = connection.cursor()
            cursor.execute(query)
            rowcount = cursor.rowcount

            link='http://127.0.0.1:8000/recover_password?key='+key_email+'&email='+email+'&action=reset';

            username='Test'
            current_datetime = datetime.now()
            timestamp=current_datetime.strftime("%d-%b-%y %H:%M:%S")
            filename='test.xlsx'
            stage='Stage1'
            country='India'
            subject = 'Password Recovery - BrandMiner'

            message = f'Dear user,\n\nPlease click on the following link to reset your password.\n\n ---------------------------------------------------------------\n\n '+link+' \n\n Please be sure to copy the entire link into your browser. \n The link will expire after 1 day for security reason.\n If you did not request this forgotten password email, no action is needed, your password will not be reset. However, you may want to log into your account and change your security password as someone may have guessed it. \n\nThanks,\n BrandMiner Team'
            # message.attach_file('/Chile_Stage2_V3.xlsx')
            # message.attach('Chile_Stage2_V3.xlsx', 'Hi Team', 'Chile_Stage2_V3.xlsx')
            email_from = 'helpdesk@brand-scapes.com'
            # recipient = ['pranit.dudhane@brand-scapes.com','mihir.pawar@brand-scapes.com']
            recipient = ['pranit.dudhane@brand-scapes.com']
            html_message='<p>Dear user,</p><p>Please click on the following link to reset your password.</p><p>Thanks,</p><p>BrandScapes Team</p>'
            res = send_mail( subject, message, email_from, recipient)
            if(res!=1):
                responseValue = {
                    "code": 400,
                    "status": "Error",
                    "Message": "Mailer Error",
                }
              
            else:
                responseValue = {
                    "code": 200,
                    "status": "Success",
                    "Message":"An email has been sent to you with instructions on how to reset your password.",
                }
        else:
            responseValue = {
                "code": 400,
                "status": "Error",
                "Message": "Your email id is not valid",
            }

        return JsonResponse(responseValue, safe=False)


def recover_password_view(request):
    return render(request,'recover_password.html',{'title':'recover_password_view'})


def change_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass2']
        hashed_password = make_password(password)
        update_password = " UPDATE auth_user SET password = '"+str(hashed_password)+"' WHERE email = '"+str(email)+"' "

        cursor = connection.cursor()
        cursor.execute(update_password)
        rowcount = cursor.rowcount
        # print('check_mail_id',rowcount)
        # exit('exit')
        if(rowcount > 0):
 
            query = "DELETE FROM password_reset_temp WHERE email='"+str(email)+"' "
            cursor = connection.cursor()
            cursor.execute(query)

            responseValue = {
                "code": 200,
                "status": "Success",
                "Message":"Congratulations! Your password has been updated successfully.",
            }
        else:
            responseValue = {
                "code": 400,
                "status": "Error",
                "Message": "Your password is not updated",
            }

        return JsonResponse(responseValue, safe=False)



def check_change_password_url_valid(request):
    if request.method == 'POST':
        email = request.POST['email']
        key_type = request.POST['key']
        select_ct = "Select * from password_reset_temp where email='"+str(email)+"' and key_tem='"+str(key_type)+"'"
        print('select_ct',select_ct)
        # exit('exit')
        cursor = connection.cursor()
        cursor.execute(select_ct)
        rows1 = cursor.fetchone()
        print('check_mail_id',rows1)
        if rows1 is not None:
 
            responseValue = {
                "code": 200,
                "status": "Success",
                "Message":"page is valid",
            }
        else:
            responseValue = {
                "code": 400,
                "status": "Error",
                "Message": "page is not valid",
            }

        return JsonResponse(responseValue, safe=False)

######################################################################################
######################################################################################
# User login code started here

def user(request):
    if request.session.has_key('is_logged'):
        username1 = request.user.username
        return render(request,'user.html',{'username':username1})
    return redirect(settings.HOMEPAGE_REDIRECT_URL)



def display_users_data(request):
    if (request.method == 'POST'):
        username1 = request.user.username
        
    return redirect(settings.HOMEPAGE_REDIRECT_URL)
# User login code end here
######################################################################################
######################################################################################

# backup landingpage
# def landingpage(request):
#     loginemail = request.GET.get('email')
#     loginpassword = 'test'
   
#     # print('##########################################################')
#     # print('email',loginemail)
#     # print('##########################################################')
#     if request.session.has_key('is_logged'):
#         username1 = request.user.username
#         return render(request,'landingpage.html',{'username':username1})
#     else:
#         # Check if the email parameter is missing or empty
#         if not loginemail:
#             return render(request, '404.html', status=404)

#         # Perform further validation if needed
#         if '@' not in loginemail:
#             return render(request, '404.html', status=404)
#         # Check if the email exists in the table
#         try:
#             # Check if the loginemail exists in the table
#             with connection.cursor() as cursor:
#                 cursor.execute("SELECT EXISTS(SELECT 1 FROM auth_user WHERE email=%s)", [loginemail])
#                 exists = cursor.fetchone()[0]
            
#             if exists:
#                 # Email exists in the table
#                 # Handle the case where the email is present
#                 username1 = request.user.username
#                 UserModel = get_user_model()
#                 user1 = UserModel.objects.get(email=loginemail)
#                 user = authenticate(username=user1, password=loginpassword)
#                 if user.is_active:
#                     dj_login(request, user,backend='django.contrib.auth.backends.ModelBackend')
#                     request.session['is_logged']= True
#                     return render(request,'landingpage.html',{'username':username1})
#                 else:
#                     return render(request, '404.html', status=404)
#             else:
#                 # Email does not exist in the table
#                 # Render the custom 404 page
#                 return render(request, '404.html', status=404)
        
#         except Exception as e:
#             # Log the exception or handle it as needed
#             return render(request, '500.html', status=500)



# def landingpage(request):
#     loginemail = request.GET.get('email')
#     loginpassword = 'test'

#     if request.session.get('is_logged'):
#         username1 = request.user.username
#         return render(request, 'landingpage.html', {'username': username1})
    
#     if not loginemail or '@' not in loginemail:
#         return render(request, '404.html', status=303)

#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT EXISTS(SELECT 1 FROM auth_user WHERE email=%s)", [loginemail])
#             exists = cursor.fetchone()[0]
        
#         if exists:
#             UserModel = get_user_model()
#             try:
#                 user1 = UserModel.objects.get(email=loginemail)
#             except UserModel.DoesNotExist:
#                 return render(request, '404.html', status=303)
            
#             user = authenticate(username=user1.username, password=loginpassword)
#             if user and user.is_active:
#                 dj_login(request, user)
#                 request.session['is_logged'] = True
#                 return render(request, 'landingpage.html', {'username': username1})
#             else:
#                 return render(request, '404.html', status=303)
#         else:
#             return render(request, '404.html', status=303)

#     except Exception as e:
#         # Optionally log the exception
#         return render(request, '500.html', status=500)


logger = logging.getLogger(__name__)

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


# def landingpage(request):
#     loginemail = request.GET.get('email')
#     # loginpassword = 'test'
#     loginpassword =  'Bc$!T00l@2024'

# def landingpage(request):
#     loginemail = request.GET.get('email')
#     loginpassword = 'test'
    # loginpassword =  'Bc$!T00l@2024'

#     # print('loginemail---> 9000',loginemail)
    
#     if request.session.get('is_logged'):
#         username1 = request.user.username
#         print('setp 1')
#         return render(request, 'landingpage.html', {'username': username1})
#     if not loginemail or not is_valid_email(loginemail):
#         return render(request, '404.html', status=404)
#         print('setp 2')

#     try:
#         print('setp 3')
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT EXISTS(SELECT 1 FROM auth_user WHERE email=%s)", [loginemail])
#             exists = cursor.fetchone()[0]
        
#         if exists:
#             print('setp 4')
#             UserModel = get_user_model()
#             try:
#                 user1 = UserModel.objects.get(email=loginemail)
#             except UserModel.DoesNotExist:
#                 return render(request, '404.html', status=404)
            
#             user = authenticate(username=user1.username, password=loginpassword)
#             if user and user.is_active:
#                 dj_login(request, user)
#                 request.session['is_logged'] = True
#                 username1 = request.user.username
#                 return render(request, 'landingpage.html', {'username': username1})
#             else:
#                 return render(request, '404.html', status=404)
#         else:
#             return render(request, '404.html', status=404)

#     except Exception as e:
#         logger.error(f"Error in landingpage view: {e}")
#         return render(request, '500.html', status=500)

# Api testing code start

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer

@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"id": user.id, "username": user.username}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


############################################################################
############################################################################
# # user_authentication  API start 
# views.py
from django.contrib.auth.models import User  # Use Django's built-in User model
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import UserAuthentication
import uuid
from django.shortcuts import get_object_or_404

# 1)FIRST API CALL
# url : http://127.0.0.1:8000/api/authenticate/
# API Request
# {"email":"mihir.pawar@brand-scapes.com"}

@api_view(['POST'])
def authenticate_user(request):
    email = request.data.get('email')

    if not email:
        return Response({'error': 'Email is required','code':404}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Check if the email exists in the auth_user table using the User model
        user = User.objects.get(email=email)
        
        # Remove existing entries for the user in the user_authentication table
        UserAuthentication.objects.filter(user=user).delete()

        # Create a token (could use uuid for simplicity)
        token = str(uuid.uuid4())

        # Store data in UserAuthentication
        UserAuthentication.objects.create(user_id=user.id, email=email, token=token)

        return Response({'user_id': user.id, 'email': email, 'token': token}, status=status.HTTP_201_CREATED)

    except User.DoesNotExist:
        return Response({'error': 'User not found','code':404}, status=status.HTTP_404_NOT_FOUND)



# 2)SECOND API CALL
# URL : http://127.0.0.1:8000/api/verify-token-and-login/
# API Request for token
# {
#     "user_id": 1,
#     "token": "token"
# }
@api_view(['POST'])
def verify_token_and_login(request):
    user_id = request.data.get('user_id')
    token = request.data.get('token')

    if not user_id or not token:
        # return Response({'error': 'Both user_id and token are required'}, status=status.HTTP_400_BAD_REQUEST)
        return redirect(settings.BASE_REDIRECT_URL+'useraction')

    try:
        # This will raise a 404 if the user_id and token combination doesn't exist
        auth_entry = get_object_or_404(UserAuthentication, user_id=user_id, token=token)
        print('auth_entry-->',auth_entry)
        # Pass the email to the login function for validation
        email = auth_entry.email

        # Call the login function with the email
        # login_response = test_function(request, email=email)
        # login_response = landingpage_logic(request, email=email)
        login_response=landingpage_logic(request, email=email)
        # Assuming the login function uses the request object

        # Return the response from the login function
        return login_response
        # return HttpResponseRedirect(reverse('landingpage'))

    except UserAuthentication.DoesNotExist:
        return redirect(settings.BASE_REDIRECT_URL+'useraction')
        # return Response({'error': 'Invalid user_id or token'}, status=status.HTTP_404_NOT_FOUND)

# @login_required(login_url=settings.HOMEPAGE_REDIRECT_URL)
def landingpage(request):
    print('landingpage call')
    if request.session.get('is_logged'):
        print('Sept is_logged 1')
        username1 = request.user.username
        return render(request, 'landingpage.html', {'username': username1})
    else:
        return redirect(settings.HOMEPAGE_REDIRECT_URL)

def landingpage_logic(request, email=None):
    # Try to find the user based on the email provided
    if request.session.get('is_logged'):
        print('Sept is_logged 1')
        username1 = request.user.username
        # return render(request, 'landingpage.html', {'username': username1})
        return redirect(settings.BASE_REDIRECT_URL+'landingpage/')
    else:
        try:
            print('Sept try is_logged 2')
            # Validate the user based on email
            user = User.objects.get(email=email)

            # Perform any additional login logic (like checking if user is active, etc.)
            if user.is_active:
                # Return success response if user is active
                # return Response({'message': 'Login successful', 'user_id': user.id, 'email': user.email}, status=status.HTTP_200_OK)
                print('Sept try if is_logged 2')
                print('email Sept try if is_logged 2',email)
                username1 = request.user.username
                UserModel = get_user_model()
                user1 = UserModel.objects.get(email=email)
                loginpassword =  'test'
                # loginpassword =  'Bc$!T00l@2024'
                print('username1-->',user1)
                user = authenticate(username=user1, password=loginpassword)
                if user and user.is_active:
                    dj_login(request, user)
                    request.session['is_logged'] = True
                    username1 = request.user.username
                    print('if condition 647 username1-->',username1)
                    # return render(request, 'landingpage.html', {'username': username1})
                    # return HttpResponseRedirect(reverse('landingpage/'))
                    # return HttpResponseRedirect('landingpage/')
                    # return redirect(settings.BASE_REDIRECT_URL+'landingpage/')
                    # return HttpResponseRedirect(reverse('landingpage'))
                    return Response({'message': 'Login successful', 'user_id': user.id, 'email': user.email}, status=status.HTTP_200_OK)
                else:
                    print('else condition 647 username1-->',username1)
                    return redirect(settings.BASE_REDIRECT_URL+'user_action')
            else:
                # If the user is not active, return an error response
                # return Response({'error': 'User account is inactive'}, status=status.HTTP_403_FORBIDDEN)
                print('Sept try else is_logged 2')
                # return render(request, '500.html', status=500)
                return redirect(settings.BASE_REDIRECT_URL+'user_action')

        except User.DoesNotExist:
            # If no user with the given email exists, return an error response
            # return Response({'error': 'Invalid email or user not found'}, status=status.HTTP_404_NOT_FOUND)
            print('Sept except is_logged 2')
            # return render(request, '404.html', status=404)
            return redirect(settings.BASE_REDIRECT_URL+'useraction')

def test_function(request, email):
    print('request',request)
    print('login test function call successfully')
    data = {
                "code": 200,
                "status": "successfully",
                "Message": "login successfully",
            }

    return JsonResponse(data, safe=False)
    
# # user_authentication API end
############################################################################
############################################################################
