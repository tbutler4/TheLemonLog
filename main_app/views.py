import uuid
import boto3
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import UserPhoto, Review, Comment
from django.contrib.auth.models import User
from .forms import EditUserForm, CommentForm
S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'lemonlog-tc'
# Define the home view
def home(request):
  reviews = Review.objects.all()
  return render(request, 'home.html', {'reviews':reviews})
@login_required
def profile(request):
  try:
    photo = UserPhoto.objects.get(user=request.user)
  except: 
    photo = UserPhoto(url='https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg', user=request.user)
  return render(request, 'user/profile.html', {'photo':photo})
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
          photo = UserPhoto.objects.get(user=request.user)
          photo.url = url
          photo.save()
      except:
          print('An error occurred uploading file to S3')
  return redirect('profile')
def edit_profile(request, user_id):
  user = User.objects.get(id=user_id)
  user_form = EditUserForm(request.POST or None, instance = user)
  if request.POST and user_form.is_valid():
    user_form.save()
    return redirect('profile')
  else:
    return render(request, 'user/edit.html', {'user':user, 'user_form': user_form})
def show_my_reviews(request):
  reviews = Review.objects.filter(user=request.user)
  return render(request, 'user/user_review.html', {'reviews':reviews})
def review_detail(request, review_id):
  review = Review.objects.get(id=review_id)
  # try:
  #   comments = Comment.objects.get(review_id= review_id)
  # except: 
  #   comments = []
  comment_form = CommentForm()
  return render(request, 'comments_reviews/review_detail.html', {'review':review, 'comment_form':comment_form })
def add_comment(request, review_id):
  if request.method=="POST":
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
      comment = comment_form.save(commit=False)
      comment.user_id = request.user.id
      comment.review_id = review_id
      comment.save()
  else:
    comment_form=CommentForm()
    return render(request, 'comments_reviews/new_comment.html', {'comment_form':comment_form})
  return redirect('review_detail', review_id)
def signup(request):
  error_message =''
  if request.method=="POST":
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      photo = UserPhoto(url='https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg', user=user)
      photo.save()
      login(request, user)
      return redirect('profile')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form':form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)