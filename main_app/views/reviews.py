import uuid
import boto3
import os
from django.shortcuts import render, redirect
from main_app.models import Review
from main_app.forms import CommentForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .aws_settings import S3_BASE_URL, BUCKET, s3, photo_file_extensions

#######################################
# Reviews Routes
#######################################
def review_detail(request, review_id):
  review = Review.objects.get(id=review_id)
  comment_form = CommentForm()
  context = {
    'review':review, 
    'comment_form':comment_form
  }
  return render(request, 'reviews/review-detail.html', context)

@login_required
def new_review(request):
  review_form = ReviewForm(request.POST or None)
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
      if photo_file.name[photo_file.name.rfind('.'):] not in photo_file_extensions:
            messages.error(request, 'Unsupported image file. Please try reuploading in the following formats: .png, .jpg, .jpeg, .webp')
            return redirect('edit_review', review_id)
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
          s3.upload_fileobj(photo_file, BUCKET, key)
          url = f"{S3_BASE_URL}{BUCKET}/{key}"
      except:
          messages.error(request, 'An error occurred uploading file to S3, please try again')
          return redirect('edit_review', review_id)
  if request.POST and review_form.is_valid():
    review = review_form.save(commit=False)
    review.user_id = request.user.id
    review.photo = url
    review.save()
    return redirect('home')
  else:
    return render(request, 'reviews/new-review.html', {'review_form':review_form})

@login_required
def edit_review(request, review_id):
  review = Review.objects.get(id=review_id)
  url = review.photo
  if request.user.id == review.user.id or request.user.is_superuser:
    review_form = ReviewForm(request.POST or None, instance = review)
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
      #  previuosly f photo_file.name[photo_file.name.rfind('.'):] not in photo_file_extensions:
        # if photo_file not in photo_file_extensions:
        #   print(photo_file)
        #   messages.error(request, 'Unsupported image file. Please try reuploading in the following formats: .png, .jpg, .jpeg, .webp')
        #   return redirect('edit_review', review_id)
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
        except:
            messages.error(request, 'An error occurred uploading file to S3, please try again')
            return redirect('edit_review', review_id)
    if request.POST and review_form.is_valid():
      review = review_form.save(commit=False)
      review.photo = url
      review.save()
      return redirect('review_detail', review_id)
    else:
      return render(request, 'reviews/edit-review.html', {'review_form':review_form, 'review':review})
  else:
    messages.error(request, 'You are not authorized to edit this review!')
    return redirect('review_detail', review_id)

@login_required
def delete_review(request, review_id):
  Review.objects.get(id=review_id).delete()
  return redirect('home')