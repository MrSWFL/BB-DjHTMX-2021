# films/views.py
from django.http.response import HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model

from films.models import Film
from films.forms import RegisterForm

# Create your views here.
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
    
class FilmList(ListView):
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
    
def add_film(request):
    name  = request.POST.get('filename')        # Get the film name the user typed in.
    film = Film.objects.create(name=name)       # Create a Film object with the film name.
    request.user.films.add(film)                # Add the film to the user's list

    # Return an HTML template with all the user's films used by the partial "film-list.html".
    films = request.user.films.all()             # Get all the user's files from DB.
    return render(request, 'partials/film-list.html', {'films' : films})