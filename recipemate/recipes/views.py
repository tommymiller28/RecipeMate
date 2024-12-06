from django.shortcuts import render, redirect, get_object_or_404
from .models import Recipe
from .forms import RecipeForm, RatingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg



#Home page
def home(request):
    return render(request, 'recipes/home.html')


# views.py
from django.db.models import Q

@login_required
def recipe_list(request):
    query = request.GET.get('q')
    if query:
        recipes = Recipe.objects.filter(
            Q(title__icontains=query) | Q(category__icontains=query)
        )
    else:
        recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes, 'query': query})





def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    comments = recipe.ratings.filter(comment__isnull=False)  # Ratings with comments
    average_rating = recipe.ratings.aggregate(Avg('rating')).get('rating__avg') or 0

    if request.method == "POST":
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.save(commit=False)
            rating.recipe = recipe
            rating.user = request.user
            rating.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        rating_form = RatingForm()

    return render(request, 'recipes/recipe_detail.html', {
        'recipe': recipe,
        'comments': comments,
        'rating_form': rating_form,
        'average_rating': average_rating,
    })



# This view will display a form for users to create a new recipe

@login_required
def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect('my_recipes')
    else:
        form = RecipeForm()
    return render(request, 'recipes/recipe_form.html', {'form': form})





# This view will load an existing recipe in the form and allow updates

@login_required
def recipe_edit(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return redirect('recipe_list')  # Prevent editing others' recipes
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)
        if form.is_valid():
            form.save()
            return redirect('recipe_detail', pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)
    return render(request, 'recipes/recipe_form.html', {'form': form})





# This view will confirm and delete a recipe

@login_required
def recipe_delete(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.author != request.user:
        return redirect('recipe_list')  # Prevent deleting others' recipes
    if request.method == "POST":
        recipe.delete()
        return redirect('recipe_list')
    return render(request, 'recipes/recipe_confirm_delete.html', {'recipe': recipe})





# This view will handle user registration

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in immediately after registration
            return redirect('recipe_list')
    else:
        form = UserCreationForm()
    return render(request, 'recipes/register.html', {'form': form})




# Define a my_recipes view in recipes/views.py that filters recipes by the logged-in user.


@login_required
def my_recipes(request):
    # Filter recipes only created by the logged-in user
    recipes = Recipe.objects.filter(author=request.user)
    
    # Search functionality (if search query exists)
    query = request.GET.get('q')
    if query:
        recipes = recipes.filter(title__icontains=query)
    
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes, 'query': query})

