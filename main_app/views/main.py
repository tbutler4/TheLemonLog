from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from main_app.models import Review

# Define the home view
def home(request):
  reviews = Review.objects.all()
  return render(request, 'main/home.html', {'reviews':reviews})

@login_required
def login_redirect(request):
    user_id = request.user.id
    return redirect('profile', user_id)
  

def about(request):
  return render(request, 'main/about.html')