from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Game_jam


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
  
class GameJamUpdate(UpdateView):
  model = Game_jam
  fields = '__all__'

class GameJamDelete(DeleteView):
  model = Game_jam
  success_url = '/gameJams/'


# threads
def threads(req):
  return render(req, 'threads.html')

def users(req):
  return render(req, 'users.html')

def profile(req):
  return render(req, 'profile.html')