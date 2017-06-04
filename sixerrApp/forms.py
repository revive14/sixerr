from django.forms import ModelForm
from sixerrApp.models import Gig

class GigForm(ModelForm):
    class Meta:
        model = Gig
        fields = ['title','category','description','photo','price','status']
