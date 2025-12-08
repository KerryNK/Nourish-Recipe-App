from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from .models import ingredientItem, recipeItem, Recipe, Favorite, Rating, Review, ShoppingList
from .forms import SignupForm, LoginForm, UserProfileForm, ReviewForm, RatingForm
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from decimal import Decimal

#view for ingredient page
def ingredientView(request):
    all_ingredients = ingredientItem.objects.all()
    return render(request, 'ingredient.html', {'all_ingredients': all_ingredients})

#view for search recipe page
def searchView(request, ingredientId):
    all_recipes= recipeItem.objects.all()
    ingredientObject = ingredientItem.objects.get(id = ingredientId)
    payload = [ingredientObject.name]
    list_recipes = []
    for i in range(0, len(all_recipes)):
      names = []
      ingredients = all_recipes[i].list_ingredient.all()
      for j in range(0, len(ingredients)):
        names.append(ingredients[j].name)
      if set(payload).issubset(set(names)):
        list_recipes.append({'name': all_recipes[i].name,
        'ingredients': all_recipes[i].ingredients.split('#'),
        'directions': all_recipes[i].directions.split('#'),
        'img_url': all_recipes[i].img_url})
    return render(request, 'searchRecipe.html',
    {'ingredientObject': ingredientObject,
    'all_recipes': all_recipes,
    'list_recipes' : list_recipes})

#get ingredient id
def get_ingredientId(request, ingredientName):
  if request.method == 'GET':
    try:
        ingredientId = ingredientItem.objects.get(name = ingredientName).id
        response = json.dumps([{'ingredientId': ingredientId}])
    except:
        response = json.dumps([{'Error': 'No id with that name'}])
  return HttpResponse(response, content_type='text/json')

#get match recipes by list of ingredients
@csrf_exempt
def get_match_recipe(request):
  if request.method == 'POST':
    payload = json.loads(request.body).get('listIngredient')
    try:
      all_recipes = recipeItem.objects.all()
      response = []
      for i in range(0, len(all_recipes)):
        names = []
        ingredients = all_recipes[i].list_ingredient.all()
        for j in range(0, len(ingredients)):
          names.append(ingredients[j].name)
        if set(payload).issubset(set(names)):
          response.append({'name': all_recipes[i].name,
          'ingredients': all_recipes[i].ingredients.split('#'),
          'directions': all_recipes[i].directions.split('#'),
          'img_url': all_recipes[i].img_url})
      response = json.dumps(response)
    except:
      response = json.dumps([{'Error': 'No id with that name'}])
  return HttpResponse(response, content_type='text/json')


# ============ AUTHENTICATION VIEWS ============

def signup(request):
  """User registration view"""
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      messages.success(request, f'Welcome, {user.username}! Your account has been created.')
      return redirect('home')
  else:
    form = SignupForm()
  
  return render(request, 'auth/signup.html', {'form': form})


def login_view(request):
  """User login view"""
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    form = LoginForm(request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      
      # Try login with username, if fails try email
      user = authenticate(request, username=username, password=password)
      if not user:
        try:
          user_obj = User.objects.get(email=username)
          user = authenticate(request, username=user_obj.username, password=password)
        except User.DoesNotExist:
          pass
      
      if user:
        login(request, user)
        messages.success(request, f'Welcome back, {user.username}!')
        return redirect('home')
      else:
        messages.error(request, 'Invalid username/email or password.')
  else:
    form = LoginForm()
  
  return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
  """User logout view"""
  logout(request)
  messages.success(request, 'You have been logged out.')
  return redirect('home')


@login_required(login_url='login')
def profile(request):
  """User profile view"""
  if request.method == 'POST':
    form = UserProfileForm(request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, 'Your profile has been updated.')
      return redirect('profile')
  else:
    form = UserProfileForm(instance=request.user)
  
  return render(request, 'auth/profile.html', {'form': form})


# ============ RECIPE DETAIL & FAVORITES ============

def home(request):
  """Home page - list all recipes"""
  recipes = Recipe.objects.filter(is_published=True)[:12]
  return render(request, 'index.html', {'recipes': recipes})


def recipes(request):
  """All recipes page"""
  recipes = Recipe.objects.filter(is_published=True)
  return render(request, 'recipes.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
  """Recipe detail page"""
  recipe = get_object_or_404(Recipe, id=recipe_id)
  
  # Increment view count
  recipe.views_count += 1
  recipe.save(update_fields=['views_count'])
  
  # Get average rating
  avg_rating = recipe.ratings.aggregate(Avg('score'))['score__avg'] or 0
  
  # Get user's rating if logged in
  user_rating = None
  is_favorited = False
  if request.user.is_authenticated:
    user_rating = recipe.ratings.filter(user=request.user).first()
    is_favorited = Favorite.objects.filter(user=request.user, recipe=recipe).exists()
  
  context = {
    'recipe': recipe,
    'avg_rating': round(avg_rating, 1) if avg_rating else 0,
    'user_rating': user_rating,
    'is_favorited': is_favorited,
    'reviews': recipe.reviews.all(),
  }
  
  return render(request, 'recipe_detail.html', context)


@login_required(login_url='login')
def toggle_favorite(request, recipe_id):
  """Toggle favorite status for a recipe (AJAX)"""
  recipe = get_object_or_404(Recipe, id=recipe_id)
  
  favorite, created = Favorite.objects.get_or_create(user=request.user, recipe=recipe)
  
  if not created:
    favorite.delete()
    is_favorited = False
    message = 'Recipe removed from favorites'
  else:
    is_favorited = True
    message = 'Recipe added to favorites'
  
  return JsonResponse({'is_favorited': is_favorited, 'message': message})


@login_required(login_url='login')
def my_favorites(request):
  """User's favorite recipes"""
  favorites = Favorite.objects.filter(user=request.user).select_related('recipe')
  recipes = [fav.recipe for fav in favorites]
  return render(request, 'my_favorites.html', {'recipes': recipes})


@login_required(login_url='login')
def my_recipes(request):
  """User's submitted recipes"""
  recipes = Recipe.objects.filter(created_by=request.user)
  return render(request, 'my_recipes.html', {'recipes': recipes})


@login_required(login_url='login')
def add_review(request, recipe_id):
  """Add a review to a recipe"""
  recipe = get_object_or_404(Recipe, id=recipe_id)
  
  if request.method == 'POST':
    form = ReviewForm(request.POST)
    if form.is_valid():
      review = form.save(commit=False)
      review.recipe = recipe
      review.user = request.user
      review.save()
      messages.success(request, 'Your review has been posted!')
      return redirect('recipe_detail', recipe_id=recipe_id)
  else:
    form = ReviewForm()
  
  return render(request, 'add_review.html', {'form': form, 'recipe': recipe})


@login_required(login_url='login')
def add_rating(request, recipe_id):
  """Add a rating to a recipe (AJAX)"""
  recipe = get_object_or_404(Recipe, id=recipe_id)
  
  if request.method == 'POST':
    score = request.POST.get('score')
    if score:
      rating, created = Rating.objects.update_or_create(
        user=request.user,
        recipe=recipe,
        defaults={'score': int(score)}
      )
      messages.success(request, f'Rating updated to {score} stars!')
      return redirect('recipe_detail', recipe_id=recipe_id)
  
  return redirect('recipe_detail', recipe_id=recipe_id)


# ============ SHOPPING LIST ============

@login_required(login_url='login')
def shopping_list(request):
  """User's shopping list"""
  shopping_list, created = ShoppingList.objects.get_or_create(user=request.user)
  items = shopping_list.items.all()
  return render(request, 'shopping_list.html', {'shopping_list': shopping_list, 'items': items})


@login_required(login_url='login')
def add_to_shopping_list(request, recipe_id):
  """Add recipe ingredients to shopping list"""
  recipe = get_object_or_404(Recipe, id=recipe_id)
  shopping_list, created = ShoppingList.objects.get_or_create(user=request.user)
  
  for ingredient in recipe.ingredients.all():
    shopping_list.items.create(
      ingredient_name=ingredient.ingredient.name,
      amount=ingredient.amount,
      unit=ingredient.unit,
      from_recipe=recipe
    )
  
  messages.success(request, f'Ingredients from "{recipe.title}" added to your shopping list!')
  return redirect('shopping_list')


@login_required(login_url='login')
def toggle_shopping_item(request, item_id):
  """Toggle purchased status of shopping list item (AJAX)"""
  from .models import ShoppingListItem
  item = get_object_or_404(ShoppingListItem, id=item_id, shopping_list__user=request.user)
  
  item.is_purchased = not item.is_purchased
  item.save()
  
  return JsonResponse({'is_purchased': item.is_purchased})


@login_required(login_url='login')
def clear_shopping_list(request):
  """Clear user's shopping list"""
  shopping_list = get_object_or_404(ShoppingList, user=request.user)
  shopping_list.items.all().delete()
  messages.success(request, 'Shopping list cleared.')
  return redirect('shopping_list')
