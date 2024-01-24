from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from EventManagementSystem import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from . tokens import generate_token
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

# Create your views here.
#cretaing function for home page
def home(request):
    return render(request, "LoginAuthentication/index.html")  #rendering html page

def register(request):
    if request.method == "POST":   #using POST method
        username = request.POST['username']    #name tag used in register page
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        #checking user validation
        if User.objects.filter(username=username):
            messages.error(request, "Sorry, the username is already taken! Please try different username for your account.")
            return redirect('home')
        
        # if User.objects.filter(email=email).exists():
        #     messages.error(request, "Sorry, the email you entered is already registered!!")
        #     return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 15 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Password mismatch. Please make sure both passwords match and try again.")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')

       #creating user object in models
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")


      #sending simple Welcome Email
        subject = "Welcome to VenueVistaIn Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"        
        from_email = settings.EMAIL_HOST_USER

       #to whom email can be send 
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)


        # Email Address Confirmation Email
        current_site = get_current_site(request)    #whether it is working on local host or deployed in it will take the domain of the website
        email_subject = "Confirm your Email @ venuevista - login"  #writing the email subject
        message2 = render_to_string('email_confirmation.html',{
            
            #passing dictionary which contains the setting keys and values for the user
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
          email_subject,
          message2,
          settings.EMAIL_HOST_USER,
          [myuser.email],
        )
        email.fail_silently = True
        email.send()
         
        return redirect('login')  #redirect to login page after creating account
        
    return render(request, "LoginAuthentication/register.html")  #rendering html page



def user_login(request , backend=None):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        #To authenticate the users with the username and password passed by user
        user_param = authenticate(username=username, password=pass1)

        #checking for the correct info
        if user_param is not None:
            auth_login(request, user_param)
            fname = user_param.first_name
            messages.success(request, "Logged In Sucessfully!!")
            return render(request, "loginAuthentication/index.html",{'fname':fname,'done':1})   #using dictionary with the keyname fname
        else:
            messages.error(request, "Wrong Credentials!!")

            #redirect to homepage if the passed credentials are incorrect
            return redirect('home')
    return render(request, "LoginAuthentication/login.html")  #rendering html page



#creating the function in order to activate the account of the user
def activate(request,uidb64,token):
    try:
        #decoding the special tokens and checking that whether this token was given to the particular user or not
        uid = force_str(urlsafe_base64_decode(uidb64))
        #creating user object
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

#validate whether my user is not none and check token
    if myuser is not None and generate_token.check_token(myuser,token):
        print("Valid activation attempt for user:", myuser.username)
        #account cann't be activate through signup only they have to confirmation link
        #after processing all the correct credentials then only this will activate the account 
        myuser.is_active = True
       
        myuser.save()
        auth_login(request, myuser)
        messages.success(request, "Your Account has been activated!!")
        return render(request,'loginAuthentication/index.html',{'done':1})
    else:
        print("Invalid activation attempt")
        return render(request,'activation_failed.html')


def logOut(request):
   logout(request)
   messages.success(request, "logged Out Succeessfully")
   return redirect ('home')


def dashboard(req):
    return render(req, 'loginAuthentication/index.html')



# #making function for authentication
# def signup(request):
#     if request.method == "POST":   #using POST method
#         username = request.POST['username']    #name tag
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']
        
        
#         if User.objects.filter(username=username):
#             messages.error(request, "Username already exist! Please try some other username.")
#             return redirect('home')
        
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email Already Registered!!")
#             return redirect('home')
        
#         if len(username)>20:
#             messages.error(request, "Username must be under 20 charcters!!")
#             return redirect('home')
        
#         if pass1 != pass2:
#             messages.error(request, "Passwords didn't matched!!")
#             return redirect('home')
        
#         if not username.isalnum():
#             messages.error(request, "Username must be Alpha-Numeric!!")
#             return redirect('home')
        
#         #creating a user object
#         myuser = User.objects.create_user(username, email, pass1)
#         myuser.first_name = fname
#         myuser.last_name = lname
#         myuser.is_active = False
#         myuser.save()
#         messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
#         # Welcome Email
#         subject = "Welcome to GFG- Django Login!!"
#         message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nAnubhav Madhav"        
#         from_email = settings.EMAIL_HOST_USER
#         to_list = [myuser.email]
#         send_mail(subject, message, from_email, to_list, fail_silently=True)
        
#         # Email Address Confirmation Email
#         current_site = get_current_site(request)
#         email_subject = "Confirm your Email @ GFG - Django Login!!"
#         message2 = render_to_string('email_confirmation.html',{
            
#             'name': myuser.first_name,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
#             'token': generate_token.make_token(myuser)
#         })
#         email = EmailMessage(
#         email_subject,
#         message2,
#         settings.EMAIL_HOST_USER,
#         [myuser.email],
#         )
#         email.fail_silently = True
#         email.send()
        
#         #after register directly redirect to login page
#         return redirect('login')
        
#     return render(request, "LoginAuthentication/signup.html")
# def activate(request,uidb64,token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         myuser = User.objects.get(pk=uid)
#     except (TypeError,ValueError,OverflowError,User.DoesNotExist):
#         myuser = None

#     if myuser is not None and generate_token.check_token(myuser,token):
#         myuser.is_active = True
#         # user.profile.signup_confirmation = True
#         myuser.save()
#         login(request,myuser)
#         messages.success(request, "Your Account has been activated!!")
#         return redirect('signin')
#     else:
#         return render(request,'activation_failed.html')
    

# def login(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         pass1 = request.POST['pass1']
        
#         user = authenticate(username=username, password=pass1)
        
#         if user is not None:
#             login(request, user)
#             fname = user.first_name
#             # messages.success(request, "Logged In Sucessfully!!")
#             return render(request, "authentication/index.html",{"fname":fname})
#         else:
#             messages.error(request, "Bad Credentials!!")
#             return redirect('home')
#     return render(request, "LoginAuthentication/login.html")

# def logout(request):
#     logout(request)
#     messages.success(request, "Logged Out Successfully!!")
#     return redirect('home')
   