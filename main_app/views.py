from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# ref: https://stackoverflow.com/questions/21405895/datepickerwidget-in-createview
from django.contrib.admin.widgets import AdminDateWidget
from .models import Game_jam, Role, Dev_log, Thread
from .forms import RoleForm, DevLogForm
from django.urls import reverse

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
  return render(req, 'role.html' ,{'roles': roles, 'role_form': role_form, 'game_jam':game_jam_id})

def add_role(request, game_jam_id):
  form = RoleForm(request.POST)
  if form.is_valid():
      new_role = form.save(commit=False)
      new_role.game_jam_id = game_jam_id
      new_role.open = True
      new_role.save()
  return redirect('all-roles', game_jam_id=game_jam_id)

class RoleDelete(DeleteView):
  model = Role

# ref: https://stackoverflow.com/questions/68882385/django-deleteview-how-to-pass-a-parameter-to-use-for-success-url
  def get_success_url(self):
    return reverse('all-roles', kwargs={'game_jam_id': self.object.game_jam_id}
    )
  
class RoleUpdate(UpdateView):
  model = Role
  fields = ['open']
  def get_success_url(self):
    return reverse('game-jam-details', kwargs={'game_jam_id': self.object.game_jam_id}
  )

# dev logs
def dev_logs(req, game_jam_id):
  dev_logs = Dev_log.objects.filter(game_jam=game_jam_id)
  return render(req, 'dev-logs.html' ,{'dev_logs': dev_logs, 'game_jam':game_jam_id})

def show_dev_log_form(req, game_jam_id):
  dev_log_form = DevLogForm()
  return render(req, 'dev-log-form.html', {'dev_log_form': dev_log_form, 'game_jam':game_jam_id})

def add_dev_log(req, game_jam_id):
  form = DevLogForm(req.POST, req.FILES)
  if form.is_valid():
    new_dev_log = form.save(commit=False)
    new_dev_log.game_jam = Game_jam.objects.get(id=game_jam_id)
    new_dev_log.save()
  return redirect('dev-logs', game_jam_id=game_jam_id)

def dev_log_details(req, game_jam_id, dev_log_id):
  dev_log = Dev_log.objects.get(id=dev_log_id)
  return render(req, 'dev-log-details.html', {'game_jam_id':game_jam_id, 'dev_log':dev_log})

class DevLogUpdate(UpdateView):
  model = Dev_log
  fields = ['title', 'images', 'description']
  def get_success_url(self):
    return reverse('dev-log-details', kwargs={'game_jam_id': self.object.game_jam_id, 'dev_log_id':self.object.id}
  )

class DevLogDelete(DeleteView):
  model = Dev_log
  def get_success_url(self):
    return reverse('dev-logs', kwargs={'game_jam_id': self.object.game_jam_id}
  )

# threads
def threads(req):
  threads = Thread.objects.all()
  return render(req, 'threads.html', {'threads':threads})

class ThreadCreate(CreateView):
  model = Thread
  fields = '__all__'
  
  def get_form(self, form_class=None):
    form = super(ThreadCreate, self).get_form(form_class)
    form.fields['date'].widget = AdminDateWidget(attrs={'type': 'date'})
    return form

def thread_details(req, thread_id):
  thread = Thread.objects.get(id=thread_id)
  return render(req, 'thread-details.html', {'thread':thread})

class ThreadUpdate(UpdateView):
  model = Thread
  fields = '__all__'

class ThreadDelete(DeleteView):
  model = Thread
  success_url = '/threads/'

def users(req):
  return render(req, 'users.html')

def profile(req):
  return render(req, 'profile.html')