import uuid
import boto3
import os
from django.shortcuts import render, redirect
from main_app.models import Review
from main_app.forms import CommentForm, NewReviewForm
from django.contrib.auth.decorators import login_required

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
# Reviews Routes
#######################################
def review_detail(request, review_id):
  review = Review.objects.get(id=review_id)
  comment_form = CommentForm()
  return render(request, 'reviews/review_detail.html', {'review':review, 'comment_form':comment_form})

@login_required
def new_review(request):
  review_form = NewReviewForm(request.POST or None)
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
  if request.POST and review_form.is_valid():
    review = review_form.save(commit=False)
    review.user_id = request.user.id
    review.photo = url
    review.save()
    return redirect('home')
  else:
    return render(request, 'reviews/new_review.html', {'review_form':review_form})

