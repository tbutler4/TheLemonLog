from django.shortcuts import render
from main_app.models import Review

# Define the home view
def home(request):
  reviews = Review.objects.all()
  return render(request, 'home.html', {'reviews':reviews})