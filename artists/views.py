'''
    Django Imports
'''

from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.http import HttpResponse, Http404
from django.views import View
from django.views.defaults import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.files.base import ContentFile
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
'''
    End Django Imports
'''


'''
    Form Imports
'''

from .forms import Profile as ArtistProfileForm
from .forms import Contact as ArtistContactsForm

'''
    End form imports
'''

'''Model Imports
'''
from .models import Artist as Profile
from .models import Contact
from utils.models import *
from events.models import *

class CreateProfile(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/auth'
    def test_func(self):
        try:
            a = Profile.objects.get(user_profile=self.request.user.profile)
            return False
        except Exception as e:
            return True

    def get(self, request):
        template = 'main/artists/create-profile.html'
        meta = {
            'description':'Create you profile here as an artist to get increase you fanbase and also reach potential clients for booking!',
            'og':{
                'title':'Create Artist Profile',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Create you profile here as an artist to get increase you fanbase and also reach potential clients for booking!',
                'image': ''
            },
            'twitter':{
                'card':'EntHub artist promotions.',
                'title':'Create Artist Profile',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Create you profile here as an artist to get increase you fanbase and also reach potential clients for booking!',
                'image': ''
            }
        }
        context = {
            'meta':meta,
            'form':ArtistProfileForm(),
        }
        return HttpResponse(render(request, template,context))
    
    def post(self, request):
        if 'create_artist_profile' in request.POST:
            form = ArtistProfileForm(request.POST)
            if form.is_valid():
                stage_name = form.cleaned_data['stage_name']
                alias = form.cleaned_data['alias']
                genre = form.cleaned_data['genre']
                bio = form.cleaned_data['bio']
                dob = form.cleaned_data['dob']
                website = form.cleaned_data['website']
                artist_profile = Profile.objects.create(
                    user_profile=request.user.profile,
                    stage_name=stage_name,
                    alias=alias,
                    genre = Genre.objects.get(pk=genre),
                    bio = bio,
                    dob = dob,
                    website=website
                    )
                artist_profile.save()
                messages.success(request, 'Profile Created Successfully. Goto view my profile to view and edit your profile.')
                return redirect(reverse('artists:view-my-profile'))
            else:
                messages.error(request, 'There was something with the information you just supplied. Try again.')
                template = 'main/artists/create-profile.html'
                context = {
                    'form':form,
                }
                return HttpResponse(render(request, template,context))
        else:
            pass

class Index(View):
    def get(self, request):
        template = 'main/artists/index.html'
        meta = {
            'description':'Browse artist profiles, their contact information and get in touch with hundreds of artists in Zimbabwe!',
            'og':{
                'title':'Browse the Artist directory',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Browse artist profiles, their contact information and get in touch with hundreds of artists in Zimbabwe!',
                'image': ''
            },
            'twitter':{
                'card':'Zimbabwe\'s Biggest Artist directory.',
                'title':'Browse the Artist directory',
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':'Browse artist profiles, their contact information and get in touch with hundreds of artists in Zimbabwe!',
                'image': ''
            }
        }
      
       
     
        artist_list = None

        if request.GET.get('query') is not None and request.GET.get('genre') is not None and request.GET.get('genre') != 'Any Genre':
            artist_list = Profile.objects.filter(stage_name__icontains=request.GET.get('query'), genre=Genre.objects.get(name=request.GET.get('genre')))

        elif request.GET.get('query') is None and request.GET.get('genre') is not None:
            artist_list = Profile.objects.filter(genre=Genre.objects.get(name=request.GET.get('genre')))
        elif request.GET.get('query') is not None and (request.GET.get('genre') is None or request.GET.get('genre') =='Any Genre'):
            artist_list = Profile.objects.filter(stage_name__icontains=request.GET.get('query'))
        else:
            artist_list = Profile.objects.all().order_by('stage_name')

        paginator = Paginator(artist_list, 9)
        page=request.GET.get('page', 1)

        artists = paginator.get_page(page)
        # Get the index of the current page
        index = artists.number - 1  # edited to something easier without index
        # This value is maximum index of your pages, so the last page - 1
        max_index = len(paginator.page_range)
        # You want a range of 7, so lets calculate where to slice the list
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index - 3 else max_index
        # Get our new page range. In the latest versions of Django page_range returns 
        # an iterator. Thus pass it to list, to make our slice possible again.
        page_range = list(paginator.page_range)[start_index:end_index]
        context = {
            'meta':meta,
            'page_range':page_range,
            'genres':Genre.objects.all(),
            'artists':artists
        }
        return HttpResponse(render(request, template, context))

class ViewArtist(View):
    def get(self, request, id, slug=""):
        artist_id = id
        artist = get_object_or_404(Profile, id=artist_id)
        template = 'main/artists/view.html'
        meta = {
            'description': artist.bio or None,
            'keywords':str(artist.stage_name)+','+str(artist.genre) +', artist, zimbabwe artists, '+str(artist.alias) or None +', Book an Artist',
            'og':{
                'title':artist.stage_name,
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':artist.bio or None,
                'image': artist.user_profile.avatar.url or None,
            },
            'twitter':{
                'card':'View {}\'s Profile'.format(artist.stage_name),
                'title':artist.stage_name,
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':artist.bio or None,
                'image': artist.user_profile.avatar.url or None,
            }
        }
        context = {
            'meta':meta,
            'featured_artists': Profile.objects.all().exclude(id=artist.id),
            'featured_events': Event.objects.all()[:5],
            'artist':artist
        }
        return HttpResponse(render(request, template, context))
class MyProfile(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/auth'
    def test_func(self):
        return self.request.user.profile.artist

    def get(self, request):
        template = 'main/artists/my-profile.html'
        initial = {
            'stage_name': request.user.profile.artist.stage_name,
            'alias':request.user.profile.artist.alias,
            'genre':[request.user.profile.artist.genre.id, request.user.profile.artist.genre],
            'bio':request.user.profile.artist.bio,
            'dob':request.user.profile.artist.dob,
            'website':request.user.profile.artist.website
        }
        meta = {
            'description': artist.bio or None,
            'og':{
                'title':artist.stage_name,
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':artist.bio or None,
                'image': artist.user_profile.avatar.url or None,
            },
            'twitter':{
                'card':'Manage your artist Profile'.format(artist.stage_name),
                'title':artist.stage_name,
                'url':str(get_current_site(request))+request.path,
                'type':'website',
                'description':artist.bio or None,
                'image': artist.user_profile.avatar.url or None,
            }
        }
        context = {
            'meta':meta,
            'ProfileForm':ArtistProfileForm(initial=initial)
        }
        return HttpResponse(render(request, template,context))
    
    def post(self, request):
        if 'update_profile' in request.POST:
            form = ArtistProfileForm(request.POST)
            if form.is_valid():
                artist = Profile.objects.get(user_profile=request.user.profile)

                stage_name = form.cleaned_data.get('stage_name')
                alias = form.cleaned_data.get('alias')
                genre = form.cleaned_data.get('genre')
                bio = form.cleaned_data.get('bio')
                dob = form.cleaned_data.get('dob')
                website = form.cleaned_data.get('website')
                if request.user.profile.artist.stage_name != stage_name:
                    artist.stage_name = stage_name
                
                if request.user.profile.artist.alias != alias:
                    artist.alias = alias
                
                if request.user.profile.artist.genre != genre:
                    artist.genre = Genre.objects.get(id=genre)
                
                if request.user.profile.artist.bio != bio:
                    artist.bio = bio

                if request.user.profile.artist.dob != dob:
                    artist.dob = dob

                if request.user.profile.artist.website != website:
                    artist.website = website
                
                artist.save()
                messages.success(request, 'Your profile has been updated successfully')
                return redirect(reverse('artists:view-my-profile'))
            else:
                template = 'main/artists/my-profile.html'
                messages.error(request, 'Action failed. Invalid input. Please check and try again.')
                context = {
                    'ProfileForm':form
                }
                return HttpResponse(render(request, template,context))
        else:
            pass

class Contacts(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/auth'
    def test_func(self):
        return self.request.user.profile.artist

    def get(self, request):
        template = 'main/artists/my-contacts.html'
        context = {
            'ContactForm':ArtistContactsForm()
        }
        return HttpResponse(render(request, template,context))

    def post(self, request):
        if 'person' and 'purpose' and 'phone' and 'email' in request.POST:
            form = ArtistContactsForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Contact saved successfully.')
                con = Contact.objects.create(
                    artist=request.user.profile.artist,
                    person=form.cleaned_data.get('person'),
                    purpose=form.cleaned_data.get('purpose'),
                    phone=form.cleaned_data.get('phone'),
                    email=form.cleaned_data.get('email'),
                    )
                con.save()
                template = 'main/artists/my-contacts.html'
                context = {
                    
                    'ContactForm':ArtistContactsForm(),
                }
                return HttpResponse(render(request, template,context))
            else:
                messages.error(request, 'Invalid input. Check and try again.')
                template = 'main/artists/my-contacts.html'
                context = {
                    'ContactForm':form,
                }
                return HttpResponse(render(request, template,context))


class DeleteContact(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/auth'
    def test_func(self):
        return self.request.user.profile.artist

    def get(self, request, contact_id):
        contact = get_object_or_404(Contact, pk=contact_id)
        # return HttpResponse(str(contact.artist.id) )
        if str(contact.artist.id) != str(request.user.profile.artist.id):
            raise (Http404)
        else:
            if contact.delete():
                return redirect(reverse('artists:my-contacts'))
                

class EditContact(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = '/auth'
    def test_func(self):
        return self.request.user.profile.artist

    def get(self, request, contact_id):
        contact = get_object_or_404(Contact, id=contact_id)
        if contact.artist != request.user.profile.artist:
            raise (Http404)
        else:
            template = 'main/artists/edit-contact.html'
            initial = {
                'person': contact.person,
                'purpose':contact.purpose,
                'phone':contact.phone,
                'email':contact.email,
                'whatsapp': contact.whatsapp
            }
            context = {
                'ContactForm': ArtistContactsForm(initial=initial),
            }
            return HttpResponse(render(request, template, context))
    
    def post(self, request, contact_id):
        if 'update_contact' in request.POST:
            form = ArtistContactsForm(request.POST)
            if form.is_valid():
                contact = get_object_or_404(Contact, id=contact_id)
                if contact.artist != request.user.profile.artist:
                    #to change to 403
                    raise (Http404)
                else:
                    person = form.cleaned_data.get('person')
                    purpose = form.cleaned_data.get('purpose')
                    phone = form.cleaned_data.get('phone')
                    email = form.cleaned_data.get('email')
                    whatsapp = form.cleaned_data.get('whatsapp')

                    if contact.person != person:
                        contact.person = person
                        contact.save()
                        messages.success(request, 'Contact detail:Person successfully updated.')
                    
                    if contact.purpose != purpose:
                        contact.purpose = purpose
                        contact.save()
                        messages.success(request, 'Contact detail:Purpose successfully updated.')
                    
                    if contact.phone != phone:
                        contact.phone = phone
                        contact.save()
                        messages.success(request, 'Contact detail:Phone successfully updated.')
                    
                    if contact.email != email:
                        contact.email = email
                        contact.save()
                        messages.success(request, 'Contact detail:Email successfully updated.')
                    
                    if whatsapp:
                        contact.whatsapp = True
                        contact.save()
                    else:
                        contact.whatsapp = False
                        contact.save()
                        
                    messages.success(request, "Contact Info Updated Successfully.")
                    return redirect(reverse('artists:edit-contact',args=(contact.id,)))
            else:
                template = 'main/artists/edit-contact.html'
                context = {
                    'ContactForm': form,
                }
                messages.error(request, 'There is something wrong with your input. Check and try again.')
                return HttpResponse(render(request, template, context))
        else:
            raise(Http404)