from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# ref: https://stackoverflow.com/questions/21405895/datepickerwidget-in-createview
from django.contrib.admin.widgets import AdminDateWidget
from .models import Game_jam, Role, Dev_log, Thread, Comment
from .forms import RoleForm, DevLogForm, CommentForm
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

class Home(LoginView):
  template_name = 'home.html'

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('main')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'signup.html', context)

def main(req):
  game_jams_ongoing = Game_jam.objects.filter(status='o')
  game_jams_completed = Game_jam.objects.filter(status='c')
  threads = Thread.objects.all().order_by('-date')[:3]
  return render(req, 'main.html', {'ongoing': game_jams_ongoing, 'completed': game_jams_completed, 'threads': threads})

# game jam
def game_jams(req):
  game_jams = Game_jam.objects.all()
  return render(req, 'game-jams.html', {'game_jams': game_jams})

def game_jam_details(req, game_jam_id):
  game_jam = Game_jam.objects.get(id=game_jam_id)
  return render(req, 'game-jam-details.html', {'game_jam':game_jam, 'request_user':req.user})

class GameJamCreate(LoginRequiredMixin, CreateView):
  model = Game_jam
  fields = ['name', 'hosting', 'description', 'Game_genre', 'application_duration', 'monetization',
            'technology', 'start_date', 'end_date']
  
  def get_form(self, form_class=None):
    form = super(GameJamCreate, self).get_form(form_class)
    form.fields['application_duration'].widget = AdminDateWidget(attrs={'type': 'date'})
    form.fields['start_date'].widget = AdminDateWidget(attrs={'type': 'date'})
    form.fields['end_date'].widget = AdminDateWidget(attrs={'type': 'date'})
    return form
  
  def form_valid(self, form):
    form.instance.user = self.request.user 
    return super().form_valid(form)
  
class GameJamUpdate(LoginRequiredMixin, UpdateView):
  model = Game_jam
  fields = '__all__'

class GameJamDelete(LoginRequiredMixin, DeleteView):
  model = Game_jam
  success_url = '/gameJams/'

# Roles
@login_required
def allRoles(req, game_jam_id):
  # ref https://stackoverflow.com/questions/22063748/django-get-returned-more-than-one-topic
  roles = Role.objects.filter(game_jam=game_jam_id)
  role_form = RoleForm()
  return render(req, 'role.html' ,{'roles': roles, 'role_form': role_form, 'game_jam':game_jam_id})

@login_required
def add_role(request, game_jam_id):
  form = RoleForm(request.POST)
  if form.is_valid():
      new_role = form.save(commit=False)
      new_role.game_jam_id = game_jam_id
      new_role.open = True
      new_role.save()
  return redirect('all-roles', game_jam_id=game_jam_id)

class RoleDelete(LoginRequiredMixin, DeleteView):
  model = Role

# ref: https://stackoverflow.com/questions/68882385/django-deleteview-how-to-pass-a-parameter-to-use-for-success-url
  def get_success_url(self):
    return reverse('all-roles', kwargs={'game_jam_id': self.object.game_jam_id}
    )
  
class RoleUpdate(LoginRequiredMixin, UpdateView):
  model = Role
  fields = ['open']
  def get_success_url(self):
    return reverse('game-jam-details', kwargs={'game_jam_id': self.object.game_jam_id}
  )

# dev logs
def dev_logs(req, game_jam_id):
  dev_logs = Dev_log.objects.filter(game_jam=game_jam_id)
  return render(req, 'dev-logs.html' ,{'dev_logs': dev_logs, 'game_jam':game_jam_id})

@login_required
def show_dev_log_form(req, game_jam_id):
  dev_log_form = DevLogForm()
  return render(req, 'dev-log-form.html', {'dev_log_form': dev_log_form, 'game_jam':game_jam_id})

@login_required
def add_dev_log(req, game_jam_id):
  form = DevLogForm(req.POST, req.FILES)

  if form.is_valid():
    new_dev_log = form.save(commit=False)
    new_dev_log.game_jam = Game_jam.objects.get(id=game_jam_id)
    new_dev_log.user = req.user
    new_dev_log.save()
  return redirect('dev-logs', game_jam_id=game_jam_id)

def dev_log_details(req, game_jam_id, dev_log_id):
  dev_log = Dev_log.objects.get(id=dev_log_id)
  return render(req, 'dev-log-details.html', {'game_jam_id':game_jam_id, 'dev_log':dev_log})

class DevLogUpdate(LoginRequiredMixin, UpdateView):
  model = Dev_log
  fields = ['title', 'images', 'description']
  def get_success_url(self):
    return reverse('dev-log-details', kwargs={'game_jam_id': self.object.game_jam_id, 'dev_log_id':self.object.id}
  )

class DevLogDelete(LoginRequiredMixin, DeleteView):
  model = Dev_log
  def get_success_url(self):
    return reverse('dev-logs', kwargs={'game_jam_id': self.object.game_jam_id}
  )

# threads
def threads(req):
  threads = Thread.objects.all()
  return render(req, 'threads.html', {'threads':threads})

class ThreadCreate(LoginRequiredMixin, CreateView):
  model = Thread
  fields = ['title', 'images', 'description']
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

def thread_details(req, thread_id):
  thread = Thread.objects.get(id=thread_id)
  comments = Comment.objects.filter(thread=thread_id)
  add_comment = CommentForm()
  return render(req, 'thread-details.html', {'thread':thread, 'comments':comments, 'add_comment':add_comment})

class ThreadUpdate(LoginRequiredMixin, UpdateView):
  model = Thread
  fields = '__all__'

class ThreadDelete(LoginRequiredMixin, DeleteView):
  model = Thread
  success_url = '/threads/'

# comment
@login_required
def add_comment(request, thread_id):
  form = CommentForm(request.POST, request.FILES)
  if form.is_valid():
    new_comment = form.save(commit=False)
    new_comment.thread = Thread.objects.get(id=thread_id)
    new_comment.user = request.user
    new_comment.save()
  return redirect('thread-details', thread_id=thread_id)

class CommentUpdate(LoginRequiredMixin, UpdateView):
  model = Comment
  fields = ['solution']

  def get_success_url(self):
    return reverse('thread-details', kwargs={'thread_id': self.object.thread.id}
  )

def users(req):
  return render(req, 'users.html')

def profile(req):
  return render(req, 'profile.html')