from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('reviews/', views.show_my_reviews, name='show_my_reviews'),
  path('profile/', views.profile, name="profile"),
  path('accounts/signup/', views.signup, name='signup'),
  path('profile/<int:user_id>/add_user_photo/', views.add_user_photo, name='add_user_photo'),
  path('profile/<int:user_id>/edit_profile/', views.edit_profile, name='edit_profile'),
  path('reviews/<int:review_id>/', views.review_detail, name='review_detail'),
  path('reviews/<int:review_id>/add_comment/', views.add_comment, name='add_comment'),
]

