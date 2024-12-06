# This allows us to easily handle forms for creating and updating recipes

from django import forms
from .models import Recipe, Comment, Rating

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'ingredients', 'instructions', 'image', 'category']




# Comment Form

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']



# Rating Form

from django import forms
from .models import Rating

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating', 'comment']  # Allow users to rate and comment
