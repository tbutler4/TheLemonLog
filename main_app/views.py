from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import UserPhoto, Review
from django.contrib.auth.models import User
import uuid
import boto3
from .forms import EditUserForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'lemonlog-tc'

# Add the following import
from django.http import HttpResponse


# Define the home view
def home(request):
  reviews = Review.objects.all()
  return render(request, 'home.html', {'reviews':reviews})

@login_required
def profile(request):
  return render(request, 'profile.html')

def add_user_photo(request, user_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      s3 = boto3.client('s3')
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      # just in case something goes wrong
      try:
          s3.upload_fileobj(photo_file, BUCKET, key)
          # build the full url string
          url = f"{S3_BASE_URL}{BUCKET}/{key}"
          # we can assign to cat_id or cat (if you have a cat object)
          photo = Photo(url=url, user_id=user_id)
          photo.save()
      except:
          print('An error occurred uploading file to S3')
  return redirect('profile', user_id=user_id)

def edit_profile(request, user_id):
  user = User.objects.get(id=user_id)
  user_form = EditUserForm(request.POST or None, instance = user)
  if request.POST and user_form.is_valid():
    user_form.save()
    return redirect('profile')
  else:
    return render(request, 'edit.html', {'user':user, 'user_form': user_form})

def show_reviews(request):
  reviews = Review.objects.filter(user=request.user)
  print(reviews)
  return render(request, 'review.html', {'reviews':reviews})
  

def signup(request):
  error_message =''
  if request.method=="POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('profile')
    else:
      error_message = 'Invalid sign up - try again'

  form = UserCreationForm()
  context = {'form':form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)