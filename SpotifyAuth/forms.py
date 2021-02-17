from django import forms

CHOICES = [    ('short_term', 'Last 4 Weeks'),
    ('medium_term', 'Last 6 Months'),
    ('long_term', 'All Time')]

class Dropdown(forms.Form):
    time_range =  forms.CharField(label="", widget=forms.Select(attrs={'class' : 'form-control'}, choices=CHOICES))