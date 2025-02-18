from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# ref: https://stackoverflow.com/questions/21405895/datepickerwidget-in-createview
from django.contrib.admin.widgets import AdminDateWidget
from .models import Game_jam, Role, Dev_log, Thread, Comment, Participant
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

# inbox
@login_required
def inbox(req):
  game_jams = Game_jam.objects.filter(user=req.user)
  applications = Participant.objects.filter(game_jam__in=game_jams)
  applied = Participant.objects.filter(user=req.user)
  return render(req, 'inbox.html', {'applications':applications, 'applied':applied})

@login_required
def game_jam_applications(req, game_jam_id):
  game_jam = Game_jam.objects.get(id=game_jam_id)
  applications = Participant.objects.filter(game_jam=game_jam)
  return render(req, 'game-jam-applications.html', {'applications':applications, 'game_jam':game_jam})

@login_required
def result(req, application_id):
  application = Participant.objects.get(id=application_id)
  return render(req, 'result.html', {'application':application})

# game jam
def game_jams(req):
  game_jams = Game_jam.objects.all()
  return render(req, 'game-jams.html', {'game_jams': game_jams})

# ref: https://stackoverflow.com/questions/37205793/django-values-list-vs-values
@login_required
def game_jam_details(req, game_jam_id):
  game_jam = Game_jam.objects.get(id=game_jam_id)
  participants = Participant.objects.filter(game_jam=game_jam_id)
  applied_roles = Participant.objects.filter(user=req.user).values_list('role', flat=True)
  return render(req, 'game-jam-details.html', {'game_jam':game_jam, 'request_user':req.user, 'participants': participants, 'applied_roles':applied_roles})

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

@login_required
def close_role(req, role_id):
  role_to_close = Role.objects.get(id=role_id)
  closed_role, created = Role.objects.update_or_create(
    id=role_id,
    defaults={'open' : False}
  )
  return redirect('game-jam-details', game_jam_id=role_to_close.game_jam.id)

@login_required
def open_role(req, role_id):
  role_to_open = Role.objects.get(id=role_id)
  open_role, created = Role.objects.update_or_create(
    id=role_id,
    defaults={'open' : True}
  )
  return redirect('game-jam-details', game_jam_id=role_to_open.game_jam.id)

# ref: https://stackoverflow.com/questions/1941212/how-to-use-get-or-create-in-django
@login_required
def apply(req, role_id):
  applied_role = Role.objects.get(id=role_id)
  applied_user = req.user
  applied_game_jam = Game_jam.objects.get(id=applied_role.game_jam.id)
  participant, created = Participant.objects.get_or_create(
    role=applied_role,
    user=applied_user,
    game_jam=applied_game_jam
  )
  return redirect('game-jam-details', game_jam_id=applied_game_jam.id)

@login_required
def approve(req, application_id):
  application = Participant.objects.get(id=application_id)
  # ref https://stackoverflow.com/questions/16329946/django-model-method-create-or-update
  approved_application, created = Participant.objects.update_or_create(
    id=application_id, 
    defaults={'status': 'a'}
  )
  return redirect('game-jam-applications', game_jam_id=application.game_jam.id)

@login_required
def deny(req, application_id):
  application = Participant.objects.get(id=application_id)
  approved_application, created = Participant.objects.update_or_create(
    id=application_id,
    defaults={'status': 'd'}
  )
  return redirect('game-jam-applications', game_jam_id=application.game_jam.id)


# dev logs
def dev_logs(req, game_jam_id):
  dev_logs = Dev_log.objects.filter(game_jam=game_jam_id)
  game_jam = Game_jam.objects.get(id=game_jam_id)
  return render(req, 'dev-logs.html' ,{'dev_logs': dev_logs, 'game_jam':game_jam_id, 'game_jam_name':game_jam})

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
  return render(req, 'dev-log-details.html', {'game_jam_id':game_jam_id, 'dev_log':dev_log, 'request_user': req.user})

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
  return render(req, 'thread-details.html', {'thread':thread, 'comments':comments, 'add_comment':add_comment, 'request_user': req.user})

class ThreadUpdate(LoginRequiredMixin, UpdateView):
  model = Thread
  fields = '__all__'

class ThreadDelete(LoginRequiredMixin, DeleteView):
  model = Thread
  success_url = '/threads/'

def close_thread(req, thread_id):
  thread = Thread.objects.get(id=thread_id)
  closed_thread, created = Thread.objects.update_or_create(
    id=thread_id, 
    defaults={'open': False}
  )
  return redirect('thread-details', thread_id=thread_id)

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

def solution(req, comment_id):
  pick_solution = Comment.objects.get(id=comment_id)
  picked_solution, created = Comment.objects.update_or_create(
    id=comment_id,
    defaults={'solution': True}
  )
  return redirect('thread-details', thread_id=pick_solution.thread.id)

def users(req):
  return render(req, 'users.html')

@login_required
def profile(req):
  return render(req, 'profile.html')