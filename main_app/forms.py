from django import forms
from .models import Role, Dev_log, Comment, Participant

class RoleForm(forms.ModelForm):
  class Meta:
    model = Role
    fields = ['name']

class DevLogForm(forms.ModelForm):
  class Meta:
    model = Dev_log
    fields = ['title', 'images', 'description']

class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields= ['description', 'images']