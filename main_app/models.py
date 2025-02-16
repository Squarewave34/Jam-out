from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
# refs:
  # ImageField: https://www.geeksforgeeks.org/imagefield-django-models/

GENRE = (
  ('ac', 'Action game'),
  ('pl', 'Platform game'),
  ('sh', 'Shooter game'),
  ('fi', 'Fighting game'),
  ('st', 'Stealth game'),
  ('sr', 'Survival game'),
  ('rh', 'Rhythm game'),
  ('br', 'Battle Royale game'),
  ('ad', 'Adventure game'),
  ('srhr', 'Survival Horror game'),
  ('tx', 'Text Adventure game'),
  ('gr', 'Graphic Adventure game'),
  ('vn', 'Visual Novel game'),
  ('im', 'Interactive Movie game'),
  ('pz', 'Puzzle game'),
  ('ph', 'Physics game'),
  ('pr', 'Programming game'),
  ('pzpl', 'Puzzle Platform game'),
  ('ex', 'Exploration game'),
  ('hi', 'Hidden Object game'),
  ('ti', 'Tile Matching game'),
  ('rp', 'Role Play game'),
  ('arpg', 'Action Role Play game'),
  ('crpg', 'Computer Role Play game'),
  ('mmorpg', 'Massively Multiplayer Online Role Playing games'),
  ('rg', 'Roguelikes game'),
  ('trpg', 'Tactical Role Play game'),
  ('srpg', 'Sandbox Role Play game'),
  ('drpg', 'Dungeon Role Play game'),
  ('mr', 'Monster Tamer game'),
  ('sm', 'Simulation game'),
  ('cms', 'Construction and Management Simulation game'),
  ('ls', 'Life Simulation game'),
  ('vs', 'Vehicle Simulation game'),
  ('stg', 'Strategy game'),
  ('4x', '4X game'),
  ('ar', 'Artillery game'),
  ('au', 'Auto Battler game'),
  ('moba', 'Multiplayer Online Battle Arena game'),
  ('rts', 'Real-time Strategy game'),
  ('rtt', 'Real-time Tactics game'),
  ('td', 'Tower Defense game'),
  ('tbs', 'Turn-based Strategy game'),
  ('tbt','Turn-based Tactics game'),
  ('wr', 'War game'),
  ('gs','Grand Strategy War game'),
  ('sp', 'Sports game'),
  ('rc', 'Racing'),
  ('cm', 'Competitive'),
  ('sf', 'Sports-based Fighting game'),
  ('mmo', 'Massively Multiplayer Online game'),
  ('bo', 'Board game '),
  ('cd', 'Card game'),
  ('ps', 'Parental Simulator game'),
  ('ca', 'Casino game'),
  ('dcc', 'Digital Collectible Card game'),
  ('tr', 'Therapeutic game'),
  ('gch', 'Gacha game'),
  ('hr', 'Horror game'),
  ('id', 'Idle game'),
  ('pa', 'Party game'),
  ('pht', 'Photography game'),
  ('sod', 'Social Deduction game'),
  ('tv', 'Trivia game'),
  ('tp', 'Typing game'),
  ('art', 'Art game'),
  ('cs', 'Casual game'),
  ('ed', 'Educational game'),
  ('exr', 'Exercise game'),
  ('sd', 'Sandbox game'),
  ('cr', 'Creative game'),
  ('op', 'Open World game')
)

STATUS = (
  ('o', 'On going'),
  ('c', 'Completed')
)


PARTICIPANTS_STATUS = (
  ('n', 'not accepted'),
  ('a', 'accepted')
)

# Create your models here.
class Game_jam(models.Model):
  name = models.CharField(max_length=200)
  hosting = models.CharField(max_length=100)
  description = models.TextField()
  Game_genre = models.CharField(max_length=100, choices=GENRE, default=GENRE[0][0])
  application_duration = models.DateField()
  monetization = models.BooleanField()
  status = models.CharField(max_length=1, choices=STATUS, default=STATUS[0][0])
  technology = models.TextField()
  # game 
  # ref: https://stackoverflow.com/questions/2029295/django-datefield-default-options
  start_date = models.DateField(default=date.today)
  end_date = models.DateField()
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return reverse('game-jam-details', kwargs={'game_jam_id': self.id})

class Role(models.Model):
  name = models.CharField(max_length=50)
  open = models.BooleanField()
  game_jam = models.ForeignKey(Game_jam, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

class Dev_log(models.Model):
  title = models.CharField(max_length=200)
  date = models.DateField(("Date"), default=date.today)
  images = models.ImageField(blank=True)
  description = models.TextField()
  game_jam = models.ForeignKey(Game_jam, on_delete=models.CASCADE)
  # links
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  def __str__(self):
    return self.title

class Thread(models.Model):
  title = models.CharField(max_length=200)
  date = models.DateField(("Date"), default=date.today)
  images = models.ImageField(blank=True)
  description = models.TextField()
  # likes
  open = models.BooleanField(default=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse('thread-details', kwargs={'thread_id': self.id})


class Comment(models.Model):
  description = models.TextField()
  date = models.DateField(("Date"), default=date.today)
  # https://stackoverflow.com/questions/7341066/can-i-make-an-admin-field-not-required-in-django-without-creating-a-form
  images = models.ImageField(blank=True)
  likes = models.IntegerField(default=0)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  solution = models.BooleanField(default=False)
  thread = models.ForeignKey(Thread, on_delete=models.CASCADE)

class Participant(models.Model):
  role = models.ForeignKey(Role, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  game_jam = models.ForeignKey(Game_jam, on_delete=models.CASCADE)
  status = models.CharField(max_length=1, choices=PARTICIPANTS_STATUS, default=PARTICIPANTS_STATUS[0][0])

  def __str__(self):
    return f"{self.user} applied to be a(n) {self.role} to your game_jam {self.game_jam}"

