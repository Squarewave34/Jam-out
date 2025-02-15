from django import forms
from .models import Role, Dev_log

class RoleForm(forms.ModelForm):
  class Meta:
    model = Role
    fields = ['name']

class DevLogForm(forms.ModelForm):
  class Meta:
    model = Dev_log
    fields = ['title', 'date', 'images', 'description']
    widgets = {
      'date': forms.DateInput(
        format=('%Y-%m-%d'),
        attrs={
          'placeholder': 'Select a date',
          'type': 'date'
        }
      ),
    }