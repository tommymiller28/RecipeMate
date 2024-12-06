from django.urls import path
from . import views

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),  # Recipe list (handles `/recipes/`)
    path('<int:pk>/', views.recipe_detail, name='recipe_detail'),  # Recipe details
    path('create/', views.recipe_create, name='recipe_create'),  # Create recipe
    path('<int:pk>/edit/', views.recipe_edit, name='recipe_edit'),  # Edit recipe
    path('<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),  # Delete recipe
    path('my-recipes/', views.my_recipes, name='my_recipes'),  # User's recipes
]