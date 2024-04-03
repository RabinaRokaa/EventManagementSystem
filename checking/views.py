from urllib import request
from django.shortcuts import redirect, render ,HttpResponse
from django.views.generic import ListView, FormView, View
from checking.models import Checking
from django.contrib.auth import views as auth_views
from .forms import AvailabilityForm
from checking.booking_functions.availability import check_availability
from django.shortcuts import render, redirect
from django.views.generic import FormView
from .models import Checking
from Venues.models import Venues
from django.urls import reverse
from django.contrib import messages

# Create your views here.
#VENUE VANNEY MODEL MA CATEGORIES PASS GARNU PARYOO KEY AND VALUE KO FORM MA TYO UTA VENUES MODELS MA GARDA HUNCHA KI YEI MODELS MA GARNU PARCHA
def VenuesList(req):
    venues = Venues.objects.all()  #fetch venues from the database
    print('lol')
    event_type = {}
    venue_values = event_type.values()
    print('type:', venue_values)
    venue_list = []

    for venue in venues:
        
        print(venues)
        venue_url = reverse('checking:VenueDetailView', kwargs={'Type' : venue})
        print(venues , venue_url)
        venue_list.append((venues , venue_url))

        event_type[venue.id] = venue.Type

        print('type:', event_type)  #kei print vayenaa
    context= {'venue_list' : venue_list, 'venues': venues, 'event_type': event_type}
    print(venue_list)
    return render(req, 'venues/venues_list.html', {'venues': venues}, context) 

#yo garda code aayooo
      
    
def venues(req):
    venues = Venues.objects.all()  #fetch venues from the database
    print('lol')
    return render(req, 'venues/venues_list.html', {'venues': venues})    

# Create your views here.
class CheckingList(ListView):
    model= Checking

#yo ra explore veues ko herney
    #yo code ley venue ko type handa details page deykhauchaa
class VenueDetailView(View):
    def get(self, request, *args, **kwargs):
        event_type = self.kwargs.get('Type', None)
        form = AvailabilityForm()
        VenuesList = Venues.objects.filter(Type=event_type)
        
        if len(VenuesList) > 0:
           venue = event_type[0]
           #yesma type ki event_type
           event_type = dict(venue.categories).get(venue.Type)
           context = {
              'Type' : event_type,
              'form' : form,
           }
           return render(request, "venues/explorevenue.html", context)
        else:
            return HttpResponse('type doesnot exist')
    

    def POST(self, request, *args, **kwargs):
        event_type = self.kwargs.get('Type', None)
        VenuesList = Venues.objects.filter(Type=event_type)
        form = AvailabilityForm(request.POST)
        
        if form.is_valid():
            data =  form.cleaned_data
            
        available_venues=[]
        for venue in VenuesList:

            if check_availability(venue, data['check_in'], data['check_out']):
               available_venues.append(venue)
               #if there are available venues
        if len(available_venues)>0:
           venue = available_venues[0]
           checking = Checking.objects.create(
               user = self.request.user,
               venue = venue,
               check_in = data['check_in'],
               check_out = data['check_out']
           )
           checking.save()
           return HttpResponse(checking)
        else:
            return HttpResponse('already booked')
  

class BookingView(FormView):
    form_class = AvailabilityForm
    template_name = 'availability_form.html'
    

    # def form_valid(self, form):
    #     data = form.cleaned_data
    #     VenuesList = Venues.objects.filter(event_type =data['categories'])
    #     available_venues=[]
    #     for venue in VenuesList:
    #         if check_availability(venue, data['check_in'], data['check_out']):
    #            available_venues.append(venue)
    #            #if there are available venues
    #     if len(available_venues)>0:
    #        venue = available_venues[0]
    #        checking = Checking.objects.create(
    #            user = self.request.user,
    #            venue = venue,
    #            check_in = data['check_in'],
    #            check_out = data['check_out']
    #        )
    #        checking.save()
    #        return HttpResponse(checking)
    #     else:
    #         return HttpResponse('already booked')
    

    # def form_valid(self, form):
    #     data = form.cleaned_data
    #     categories = data.get('categories')
    #     check_in = data.get('check_in')
    #     check_out = data.get('check_out')

    #     if categories and check_in and check_out:
    #         VenuesList = Venues.objects.filter(event_type=categories)
    #         available_venues = []
    #         for venue in VenuesList:
    #             if check_availability(venue, check_in, check_out):
    #                 available_venues.append(venue)
    #         if available_venues:
    #             venue = available_venues[0]
    #             checking = Checking.objects.create(
    #                 user=self.request.user,
    #                 venue=venue,
    #                 check_in=check_in,
    #                 check_out=check_out
    #             )
    #             # You might want to use redirect instead of HttpResponse
    #             return redirect(self.success_url)
    #         else:
    #             return HttpResponse('Venue already booked.')
    #     else:
    #         # Handle case where form fields are missing
    #         return HttpResponse('Form fields are missing.')

    # def form_valid(self, form):
    #     data = form.cleaned_data
    #     event_type = data.get('event_type')
    #     check_in = data.get('check_in')
    #     check_out = data.get('check_out')

    #     if event_type and check_in and check_out:
    #         venues_list = Venues.objects.filter(event_type=event_type)
    #         available_venues = []

    #         for venue in venues_list:
    #             if check_availability(venue, check_in, check_out):
    #                 available_venues.append(venue)

    #         if available_venues:
    #             venue = available_venues[0]
    #             checking = Checking.objects.create(
    #                 user=self.request.user,
    #                 venue=venue,
    #                 check_in=check_in,
    #                 check_out=check_out
    #             )
    #             # Redirect to success URL after successful booking
    #             return redirect(self.success_url)
    #         else:
    #             return render(self.request, 'availability_form.html', {'form': form, 'error_message': 'Venue already booked.'})
    #     else:
    #         return render(self.request, 'availability_form.html', {'form': form, 'error_message': 'Please fill in all fields.'})

    def form_valid(self, form):
        data = form.cleaned_data
        event_type = data.get('event_type')
        check_in = data.get('check_in')
        check_out = data.get('check_out')

        if event_type and check_in and check_out:
            venues_list = Venues.objects.filter(Type=event_type)
            available_venues = []

            for venue in venues_list:
                if check_availability(venue, check_in, check_out):
                    available_venues.append(venue)

            if available_venues:
                venue = available_venues[0]
                checking = Checking.objects.create(
                    user=self.request.user,
                    venue=venue,
                    check_in=check_in,
                    check_out=check_out
                )
                success_message = f"You have successfully booked {venue} from {check_in} to {check_out}."
                messages.success(self.request, success_message)
                # Redirect to success URL after successful booking
                return redirect(reverse('checking_detail', kwargs={'pk': checking.pk}))

            else:
                return render(self.request, 'availability_form.html', {'form': form, 'error_message': 'Venue already booked.'})
        else:
            return render(self.request, 'availability_form.html', {'form': form, 'error_message': 'Please fill in all fields.'})
        

        #YETA SAMMA GARDA BOOKED YO YO VANNU PARXA