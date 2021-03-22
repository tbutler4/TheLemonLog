import uuid
import boto3
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from main_app.models import UserPhoto, Review, Comment
from main_app.forms import EditUserForm, CommentForm, UserForm
from django.contrib import messages

#######################################
# Comments Routes
#######################################

@login_required
def add_comment(request, review_id):
  comment_form=CommentForm(request.POST or None)
  review = Review.objects.get(id=review_id)
  if request.POST and comment_form.is_valid():
      comment = comment_form.save(commit=False)
      comment.user_id = request.user.id
      comment.review_id = review_id
      comment.save()
      return redirect('review_detail', review_id)
  else:
    messages.error(request, "Something went wrong with commenting, please try again")
    return redirect('review_detail', review_id)

@login_required
def edit_comment(request, review_id, comment_id):
  review = Review.objects.get(id=review_id)
  comment = Comment.objects.get(id=comment_id)
  if comment.user.id == request.user.id:
    comment_form = CommentForm(request.POST or None, instance = comment)
    if request.POST and comment_form.is_valid():
      comment_form.save()
      return redirect('review_detail', review_id=review_id)
    else:
      return render(request, 'comments/edit-comment.html', {'comment_form':comment_form, 'review':review, 'comment':comment})
  else:
    messages.error(request, 'Sorry, you are not authorized to edit this comment')
    return redirect('review_detail', review_id)

@login_required
def delete_comment(request, review_id, comment_id):
  comment = Comment.objects.get(id=comment_id)
  if comment.user.id == request.user.id:
    comment.delete()
  else: 
    messages.error(request, "Sorry, you are not authorized to delete this comment!")
  return redirect('review_detail', review_id=review_id)