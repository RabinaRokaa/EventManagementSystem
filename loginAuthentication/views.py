from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
# from django.contrib.auth import user as auth_user
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
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView , PasswordResetConfirmView
from Venues.models import Venues  # Import your models
from profiles.models import profiles  # Import your models
from decoration.models import decoration   # Import your models
from django.views.decorators.http import require_GET
from photographer.models import photographer  # Import your models
from django.shortcuts import render
from booking.models import booking
from chat.models import Message
from decbooking.models import decbooking
from photographerbooking.models import photographerbooking
from django.contrib.auth.decorators import login_required

# Create your views here.
#cretaing function for home page
def home(request):
    return render(request, "LoginAuthentication/index.html")  #rendering html page

def register(request):
    if request.method == "POST":   #using POST method
        username = request.POST['username']    #name tag used in register page
        
        fname = request.POST['fname']
        lname = request.POST['lname']
        # phoneno = request.POST['phoneno']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # Check if the 'is_superuser' checkbox is checked in the form
        is_superuser = request.POST.get('is_superuser', False)

       

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
        
        # if len(phoneno)>15:
        #     messages.error(request, "Username must be under 10 charcters!!")
        #     return redirect('home')
        
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
 #checking for superuser
        if is_superuser:
            myuser.is_superuser = True
            myuser.save()

            # Create a profile for the user
       #profiles.objects.create(user=myuser)

      #sending simple Welcome Email
        subject = "Welcome to VenueVistaIn Login!!"
        message = "Hi, " + myuser.first_name + "!! \n" + "\nThank you for visiting our website.\n We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\nRabina Roka"        
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

def user_login(request, backend=None):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        # To authenticate the users with the username and password passed by the user
        user_param = authenticate(username=username, password=pass1)

        # Checking for the correct info
        if user_param is not None:
            auth_login(request, user_param)
            fname = user_param.first_name
            messages.success(request, "Logged In Successfully!!")

            # For admin login to redirect to the admin panel after login
            if user_param.is_superuser:
                return redirect('loginAuthentication:adminpanel')
            else:
                print("hello")
                return redirect(f"/userdashboard/?fname={fname}&done=1")   # Using dictionary with the keyname fname
                   # Using dictionary with the keyname fname
        else:
            messages.error(request, "Wrong Credentials!!")

            # Redirect to the homepage if the passed credentials are incorrect
            return redirect('loginAuthentication:home')

    return render(request, "LoginAuthentication/login.html")  # Rendering HTML page while logging in through normal username and password


# def user_login(request , backend=None):
#     if request.method == 'POST':
#         username = request.POST['username']
#         pass1 = request.POST['pass1']
        
#         #To authenticate the users with the username and password passed by user
#         user_param = authenticate(username=username, password=pass1)

#         #checking for the correct info
#         if user_param is not None:
#             auth_login(request, user_param)
#             fname = user_param.first_name
#             messages.success(request, "Logged In Sucessfully!!")

#       #for admin login to redirect admin panel after login
#             if user_param.is_superuser:
#                 return redirect('adminpanel')
#             else:  
#                 print("hello")
#                 return render(request, "LoginAuthentication/userdashboard.html",{'fname':fname,'done':1})   #using dictionary with the keyname fname
#         else:
#             messages.error(request, "Wrong Credentials!!")

#             #redirect to homepage if the passed credentials are incorrect
#             return redirect('home')
#     return render(request, "LoginAuthentication/login.html")  #rendering html page



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
        messages.success(request, "Your Account has been activated!!Now, you can login")
        return render(request,'loginAuthentication/login.html',{'done':1})
    else:
        print("Invalid activation attempt")
        return render(request,'activation_failed.html')


class PasswordResetCustomView(PasswordResetView):
    template_name = 'loginAuthentication/password_reset_form.html'
    email_template_name = 'loginAuthentication/password_reset_email.html'
    subject_template_name = 'loginAuthentication/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    success_message = "We've emailed you instructions for setting your password. If an account exists with the email you entered, you should receive them shortly. If you don't receive an email, please make sure you've entered the address you registered with and check your spam folder."

class PasswordResetConfirmCustomView(PasswordResetConfirmView):
    template_name = 'loginAuthentication/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')


def logOut(request):
   logout(request)
   messages.success(request, "logged Out Succeessfully")
   return redirect ('home')


# def dashboard(req):
#     return render(req, 'loginAuthentication/index.html')

def landingpage(req):
    return render(req, 'loginAuthentication/landingpage.html')

def organizerpanel(req):
    return render(req, 'loginAuthentication/organizerpanel.html')

def userdashboard(request):
    venues = Venues.objects.all()  # Fetch venues from the database
    decorations = decoration.objects.all()
    photographers = photographer.objects.all()
    messages = Message.objects.all()

    recent_bookings = None
    user_bookings = None
    decor_bookings = None
    photographerbookings = None
    # messages = None

    if request.user.is_authenticated:
        recent_bookings = booking.objects.filter(User=request.user).order_by('-Date')[:3]  # Fetch recent bookings for the current user
        user_bookings = booking.objects.filter(User=request.user)  # Fetch all booking history for the current user
        decor_bookings = decbooking.objects.filter(User=request.user)  # Fetch all booking history for the current user
        photographerbookings = photographerbooking.objects.filter(User=request.user)  # Fetch all booking history for the current user
        # messages = Message.objects.filter(Q(user=request.user) | Q(messaged_to=request.user))
        filter1=Q(user=request.user) & Q(messaged_to__username='admin')
        filter2=Q(user__username='admin') & Q(messaged_to=request.user)
        messages = Message.objects.filter(filter1 | filter2).order_by('date')

        for message in messages:
            print("ae",message)
        if request.method == 'POST':
        # Get form data
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            # Update user information
            user = request.user
            user.username = username
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            # Return JavaScript alert response
            return HttpResponse('<script>alert("Your profile has been updated successfully!"); window.location.href = "/userdashboard/";</script>')

    context = {
        'venues': venues,
        'decorations': decorations,
        'photographers': photographers,
        'recent_bookings': recent_bookings,
        'user_bookings': user_bookings,
        'decor_bookings':decor_bookings,
        'photographerbookings':photographerbookings,
        'user': request.user,
        'messages': messages,
    }

    return render(request, 'loginAuthentication/userdashboard.html', context)


def userdashboards(req):
    recent_bookings = booking.objects.filter(user=req.user).order_by('-booking_date')[:5] 
    return render(req, 'loginAuthentication/userdashboards.html', {'recent_bookings': recent_bookings})

def adminpanel(req):
    total_bookings=booking.objects.count()
    return render(req, 'loginAuthentication/adminpanel.html',{'total_bookings':total_bookings})

def userlist(request):
    users = User.objects.all()  #fetch users from the database
    return render(request, 'loginAuthentication/user_list.html', {'users': users})
    # return render(req, 'loginAuthentication/userlist.html')


def delete_user(request, id):
    user = get_object_or_404(User, id= id)
    if request.method == 'GET':
        user.delete()
        return redirect('/user_list')  # Redirect to venue list page after delete
    # return render(request, 'loginAuthentication/delete_user.html', {'myuser': user})

 
# pass id attribute from urls
def view_user(request, id):
    # dictionary for initial data with 
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["data"] = User.objects.get(id = id)    
    return render(request, "loginAuthentication/view_user.html", context)


from django.http import JsonResponse
from django.db.models import Q
from Venues.models import Venues
@require_GET
def filter_venues(request):
    venues = Venues.objects.all()
    name_contains_query = request.GET.get('Name_contains')
    location_contains_query = request.GET.get('Location_exact')
    title_or_author_query = request.GET.get('Name_or_Location')
    min_cost = request.GET.get('view_count_min')
    max_cost = request.GET.get('view_count_max')

    if name_contains_query != '' and name_contains_query is not None:
        venues = venues.filter(Name__icontains=name_contains_query)

    if location_contains_query != '' and location_contains_query is not None:
        venues = venues.filter(Location__icontains=location_contains_query)

    if title_or_author_query != '' and title_or_author_query is not None:
        venues = venues.filter(Q(Name__icontains=title_or_author_query) | Q(Location__icontains=title_or_author_query)).distinct()
    
    if min_cost:
        venues = venues.filter(Cost__gte=min_cost)

    if max_cost:
        venues = venues.filter(Cost__lte=max_cost)

    data = [{
        'Name': venue.Name,
        'Location': venue.Location,
        'Description': venue.Description,
        'Cost': venue.Cost,
        'Venue_images': [image.image.url for image in venue.Venue_image.all()],
        'id':venue.id
        
    } for venue in venues]


    # Return JSON response
    return JsonResponse({'venues': data})

#name chanage k sanga change garnye ho tei
def filterform(request):
    venues = Venues.objects.all()
    name_contains_query = request.GET.get('Name_contains')
    location_contains_query = request.GET.get('Location_exact')
    title_or_author_query = request.GET.get('Name_or_Location')
    min_cost = request.GET.get('view_count_min')
    max_cost = request.GET.get('view_count_max')

    if name_contains_query != '' and name_contains_query is not None:
        venues = venues.filter(Name__icontains=name_contains_query)

    if location_contains_query != '' and location_contains_query is not None:
        venues = venues.filter(Location__icontains=location_contains_query)

    if title_or_author_query != '' and title_or_author_query is not None:
        venues = venues.filter(Q(Name__icontains=title_or_author_query) | Q(Location__icontains=title_or_author_query)).distinct()
    
    if min_cost:
        venues = venues.filter(Cost__gte=min_cost)

    if max_cost:
        venues = venues.filter(Cost__lte=max_cost)

    context = {
        'venues': venues,
        'categories':['Marriage','Birthday','Conference','Anniversary']
    }
    return render(request, "venues/filterform.html", context)

# views.py

@login_required
def booking_history(request):
    user_bookings = booking.objects.filter(User=request.user)
    return render(request, "loginAuthentication/booking_history.html", {'user_bookings': user_bookings})


def about_us(request):
    return render(request, "loginAuthentication/Aboutus.html")


def profile(request):
    profile = profiles.objects.get(user=request.user)

    context = {
        "Profile" : profile

    }

    return render(request, "loginAuthentication/editprofile.html" ,context )
