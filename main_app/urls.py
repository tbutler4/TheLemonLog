from django.urls import path
from . import views


urlpatterns = [
  path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/', views.login_redirect, name='login_redirect'),
  path('profile/<int:user_id>/', views.profile, name="profile"),
  path('profile/edit_profile/', views.edit_profile, name='edit_profile'),
  path('profile/add_user_photo/', views.add_user_photo, name='add_user_photo'),
  path('profile/reviews/', views.show_my_reviews, name='show_my_reviews'),
  path('reviews/new_review/', views.new_review, name='new_review'),
  path('reviews/<int:review_id>/', views.review_detail, name='review_detail'),
  path('reviews/<int:review_id>/edit_review', views.edit_review, name='edit_review'),
  path('reviews/<int:review_id>/delete_review', views.delete_review, name='delete_review'),
  path('reviews/<int:review_id>/add_comment/', views.add_comment, name='add_comment'),
  path('reviews/<int:review_id>/edit_comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
  path('reviews/<int:review_id>/delete_comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]

