import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from main_app.models import UserPhoto, Review, Comment
from main_app.forms import EditUserForm, UserForm

#######################################
# Amazon AWS info
#######################################
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'lemonlog-tc'

s3 = boto3.client(
  's3',
  aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
  aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
)

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
  reviews = Review.objects.all()
  comments = Comment.objects.all()
  user = User.objects.get(id=user_id)
  my_dict = {}
  for comment in comments:
    if request.user.id == comment.user_id:
      review_product = comment.review.product
      comment_review_id = comment.review.id
      comment_text = comment.comment_text
      if review_product not in my_dict:
        my_dict.update({review_product: {'comments': [comment_text]}})
      else:
        my_dict[review_product]['comments'].append(comment_text)
      if 'comment_review_id' not in my_dict[review_product]:
        my_dict[review_product].update({'comment_review_id': comment_review_id})
  print(my_dict)
  try:
    photo = UserPhoto.objects.get(user=user)
  except: 
    photo = UserPhoto(url='https://lemonlog-tc.s3-us-west-1.amazonaws.com/lemon.png', user=request.user)
  return render(request, 'user/profile.html', {'photo':photo, 'user':user, 'my_dict': my_dict})

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
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      # need a unique "key" for S3 / needs image file extension too
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      # just in case something goes wrong
      try:
          s3.upload_fileobj(photo_file, BUCKET, key)
          # build the full url string
          url = f"{S3_BASE_URL}{BUCKET}/{key}"
      except:
          print('An error occurred uploading file to S3')
      try:
        photo = UserPhoto.objects.get(user=request.user)
      except:
        photo= UserPhoto(url=url, user=request.user)
      photo.url = url
      photo.save()
  return redirect('profile', request.user.id)
