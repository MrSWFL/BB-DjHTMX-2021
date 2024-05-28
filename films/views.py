# films/views.py
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from films.models import Film
from films.forms import RegisterForm

# Create your views here.
# custom 404 view
def custom_404(request, exception):
    return render(request, '404.html', status=404)

class IndexView(TemplateView):
    template_name = 'index.html'
    
class Login(LoginView):
    template_name = 'registration/login.html'

class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()  # save the user
        return super().form_valid(form)
    
class FilmList(LoginRequiredMixin, ListView):

    template_name = 'films.html'
    model = Film
    context_object_name = 'films'

    def get_queryset(self):
        user = self.request.user
        return user.films.all()

def check_username(request):
    username = request.POST.get("username")
    if get_user_model().objects.filter(username=username).exists():

        msg3 = """
            <div id='username-error' class='h1'>
                <span class="badge text-bg-error">This username already exists!</span>
            </div>
        """

        msg2 = """
            <div class="alert alert-danger" role="alert">
                This username already exists!
            </div>
        """

        msg1 = """
            <div id='username-error' class='error h1'>This username already exists!</div>
        """
        return HttpResponse(msg1)
    
    else:
        msg3 = """
            <div id='username-error' class='h1'>
                <span class="badge text-bg-error">This username is available!</span>
            </div>
        """
                
        msg2 = """
            <div class="alert alert-info" role="alert">
                This username is available
            </div>
        """

        msg1 = """
            <div id='username-error' class='h1'>
                This username is available!
            </div>
        """
        return HttpResponse(msg1)

@login_required    
def add_film(request):
    name = request.POST.get('filmname')         # Get the film name the user typed in.
    film = Film.objects.get_or_create(name=name)[0]       # Create a Film object with the film name.
    request.user.films.add(film)                # Add the film to the user's list

    # Return an HTML template with all the user's films used by the partial "film-list.html".
    films = request.user.films.all()             # Get all the user's files from DB.

    messages.success(request, f"Added {name} to list of films")
    return render(request, 'partials/film-list.html', {'films' : films})

@login_required
@require_http_methods(['DELETE'])
def delete_film(request, pk):
    # Remove the film from the user's list.
    request.user.films.remove(pk)
    
    # Return the HTML fragment with the list of user's films.
    films = request.user.films.all()             # Get all the user's files from DB.
    return render(request, 'partials/film-list.html', {'films' : films})

def search_film(request):
    search_text = request.POST.get('search_string')

    # Get the list of films currently in the user's list. DON'T show these in the search results.
    userfilms = request.user.films.all()

    # Look for a film containing the case insensitive string AND not already in the user's list.
    results = Film.objects.filter(name__icontains=search_text).exclude(name__in=userfilms.values_list('name', flat=True))
    context = {'results' : results}
    return render(request, 'partials/search-results.html', context)

def clear(request):
    return HttpResponse("")