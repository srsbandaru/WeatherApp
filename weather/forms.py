from django import forms

class WeatherByCityForm(forms.Form):
    city = forms.CharField(max_length=50)

    
