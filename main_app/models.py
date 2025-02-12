from django.db import models
from django.urls import reverse
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
  start_date = models.DateField()
  end_date = models.DateField()

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
  date = models.DateField()
  images = models.ImageField()
  description = models.TextField()
  # links
  # user id
  def __str__(self):
    return self.title

class Thread(models.Model):
  title = models.CharField(max_length=200)
  date = models.DateField()
  images = models.ImageField()
  description = models.TextField()
  # likes
  open = models.BooleanField()

  def __str__(self):
    return self.title

class Comment(models.Model):
  description = models.TextField()
  date = models.DateField()
  images = models.ImageField()
  likes = models.IntegerField(default=0)
  # user id
  solution = models.BooleanField()
  # thread id