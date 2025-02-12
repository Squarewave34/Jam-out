from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# ref: https://stackoverflow.com/questions/21405895/datepickerwidget-in-createview
from django.contrib.admin.widgets import AdminDateWidget
from .models import Game_jam, Role
from .forms import RoleForm


def home(req):
  return render(req, 'main.html')

def main(req):
  return render(req, 'main.html')

# game jam
def game_jams(req):
  game_jams = Game_jam.objects.all()
  return render(req, 'game-jams.html', {'game_jams': game_jams})

def game_jam_details(req, game_jam_id):
  game_jam = Game_jam.objects.get(id=game_jam_id)
  return render(req, 'game-jam-details.html', {'game_jam':game_jam})

class GameJamCreate(CreateView):
  model = Game_jam
  fields = ['name', 'hosting', 'description', 'Game_genre', 'application_duration', 'monetization',
            'technology', 'start_date', 'end_date']
  
  def get_form(self, form_class=None):
    form = super(GameJamCreate, self).get_form(form_class)
    form.fields['application_duration'].widget = AdminDateWidget(attrs={'type': 'date'})
    form.fields['start_date'].widget = AdminDateWidget(attrs={'type': 'date'})
    form.fields['end_date'].widget = AdminDateWidget(attrs={'type': 'date'})
    return form
  
class GameJamUpdate(UpdateView):
  model = Game_jam
  fields = '__all__'

class GameJamDelete(DeleteView):
  model = Game_jam
  success_url = '/gameJams/'

# Roles
def allRoles(req, game_jam_id):
  # ref https://stackoverflow.com/questions/22063748/django-get-returned-more-than-one-topic
  roles = Role.objects.filter(game_jam=game_jam_id)
  role_form = RoleForm()
  return render(req, 'role.html' ,{'roles': roles, 'role_form': role_form})

# threads
def threads(req):
  return render(req, 'threads.html')

def users(req):
  return render(req, 'users.html')

def profile(req):
  return render(req, 'profile.html')