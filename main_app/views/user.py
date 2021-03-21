import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main_app.models import UserPhoto, Review 
from main_app.forms import EditUserForm, UserForm
from .aws_settings import S3_BASE_URL, BUCKET, s3, photo_file_extensions


#######################################
# User Sign Up/ Profile-related routes
#######################################
def signup(request):
  error_message =''
  if request.method=="POST":
    form = UserForm(request.POST)
    if form.is_valid():
      user = form.save()
      photo = UserPhoto(url='https://lemonlog-tc.s3-us-west-1.amazonaws.com/lemon.png', user=user)
      photo.save()
      login(request, user)
      return redirect('profile', request.user.id)
    else:
      print(form.error_messages)
      error_message = 'Invalid sign up - try again'
  form = UserForm()
  context = {'form':form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def profile(request, user_id):
  user = User.objects.get(id=user_id)
  try:
    photo = UserPhoto.objects.get(user=user)
  except: 
    photo = UserPhoto(url='https://lemonlog-tc.s3-us-west-1.amazonaws.com/lemon.png', user=request.user)
  return render(request, 'user/profile.html', {'photo':photo, 'user':user})

@login_required
def edit_profile(request):
  user_form = EditUserForm(request.POST or None, instance = request.user)
  if request.POST and user_form.is_valid():
    user_form.save()
    return redirect('profile', request.user.id)
  else:
    return render(request, 'user/edit.html', {'user_form': user_form})

@login_required
def show_my_reviews(request):
  reviews = Review.objects.filter(user=request.user)
  return render(request, 'user/user_review.html', {'reviews':reviews})

@login_required
def add_user_photo(request):
  error_message = 'Error uploading user photo, please try again'
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
          s3.upload_fileobj(photo_file, BUCKET, key)
          url = f"{S3_BASE_URL}{BUCKET}/{key}"
      except:
          error_message = 'An error occurred uploading file to remote server, please try again'
      try:
        photo = UserPhoto.objects.get(user=request.user)
      except:
        photo= UserPhoto(url=url, user=request.user)
      photo.url = url
      photo.save()
  return redirect('profile', request.user.id), {"error":error_message}
