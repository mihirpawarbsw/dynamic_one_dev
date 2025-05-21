
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

# Create your views here.
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
            return redirect('/')

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
                return redirect('/')
        else:
            # print('123')
            messages.error(request, 'Invalid email and password')
            return redirect('/')
    return render(request,'index.html',{'title':'index'})


# def landingpage(request):
#     # if request.session.has_key('is_logged'):
#     #     username1 = request.user.username
#     #     return render(request,'landingpage.html',{'username':username1})
#     # return redirect('/')
def landingpage(request):
    # Retrieve the email from query parameters
    login_email = request.GET.get('email')
    
    # Check if the user is already logged in
    if request.session.get('is_logged'):
        username = request.user.username
        return render(request, 'landingpage.html', {'username': username})
    else:
        # Handle missing or invalid email
        if not login_email or '@' not in login_email:
            return render(request, '404.html', status=404)
        else:
            # Check if the email exists in the database
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT EXISTS(SELECT 1 FROM auth_user WHERE email=%s)", [login_email])
                    exists = cursor.fetchone()[0]

                if exists:
                    UserModel = get_user_model()
                    user = get_object_or_404(UserModel, email=login_email)
                    
                    # Authenticate the user (password is hardcoded for simplicity)
                    # Ideally, the password should be securely handled
                    # user = authenticate(username=user.username, password='test')
                    user = authenticate(username=user.username, password='Bc$!T00l@2024')
                    
                    if user and user.is_active:
                        dj_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                        request.session['is_logged'] = True
                        return render(request, 'landingpage.html', {'username': user.username})
                    else:
                        return render(request, '404.html', status=404)
                else:
                    return render(request, '404.html', status=404)

            except Exception as e:
                # Optionally log the exception
                return render(request, '500.html', status=500)

@login_required(login_url='/')
def logout(request):
    del request.session['is_logged']
    del_logout(request)
    return redirect('/')


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
    return redirect('/')



def display_users_data(request):
    if (request.method == 'POST'):
        username1 = request.user.username
        
    return redirect('/')
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

#     # Check if the email parameter is missing or empty
#     if not loginemail:
#         return render(request, '404.html', status=404)

#     # Perform further validation if needed
#     if '@' not in loginemail:
#         return render(request, '404.html', status=404)
#     # Check if the email exists in the table
#     try:
#         # Check if the loginemail exists in the table
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT EXISTS(SELECT 1 FROM auth_user WHERE email=%s)", [loginemail])
#             exists = cursor.fetchone()[0]
        
#         if exists:
#             # Email exists in the table
#             # Handle the case where the email is present
#             username1 = request.user.username
#             UserModel = get_user_model()
#             user1 = UserModel.objects.get(email=loginemail)
#             # user = authenticate(username=user1, password=loginpassword)
#             user = authenticate(username=user1, password=loginpassword)
#             if user.is_active:
#                 dj_login(request, user,backend='django.contrib.auth.backends.ModelBackend')
#                 request.session['is_logged']= True
#                 return render(request,'landingpage.html',{'username':username1})
#             else:
#                 return render(request, '404.html', status=404)
#         else:
#             # Email does not exist in the table
#             # Render the custom 404 page
#             return render(request, '404.html', status=404)
    
#     except Exception as e:
#         # Log the exception or handle it as needed
#         return render(request, '500.html', status=500)