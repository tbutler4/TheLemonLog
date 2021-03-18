import uuid
import boto3
import os
from django.shortcuts import render
from django.contrib.auth.models import User
from main_app.models import Review, Comment, UserPhoto
from main_app.forms import CommentForm

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
  photos = UserPhoto.objects.all()
  review = Review.objects.get(id=review_id)
  try:
    comments = Comment.objects.get(review_id= review_id)
  except: 
    comments = []
  comment_form = CommentForm()
  return render(request, 'comments_reviews/review_detail.html', {'review':review, 'comment_form':comment_form})


