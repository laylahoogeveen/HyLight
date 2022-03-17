from .models import Profile
from django.contrib.auth.models import User
from .forms import ChangeAvailability

def add_form(request):
   context = {
      'availability_form': ChangeAvailability(request.POST),
   }
   return context