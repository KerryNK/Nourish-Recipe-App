"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ingredient.views import (
    ingredientView, searchView, get_ingredientId, get_match_recipe,
    signup, login_view, logout_view, profile,
    home, recipes, recipe_detail, toggle_favorite,
    my_favorites, my_recipes, add_review, add_rating,
    shopping_list, add_to_shopping_list, toggle_shopping_item, clear_shopping_list
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Home & Recipes
    path('', home, name='home'),
    path('recipes/', recipes, name='recipes'),
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
    
    # Legacy ingredient search (keep for compatibility)
    path('ingredients/', ingredientView),
    path('search/<int:ingredientId>/', searchView),
    
    # Authentication
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
    
    # Favorites
    path('favorites/', my_favorites, name='my_favorites'),
    path('recipe/<int:recipe_id>/favorite/', toggle_favorite, name='toggle_favorite'),
    
    # Recipes
    path('my-recipes/', my_recipes, name='my_recipes'),
    
    # Reviews & Ratings
    path('recipe/<int:recipe_id>/review/', add_review, name='add_review'),
    path('recipe/<int:recipe_id>/rating/', add_rating, name='add_rating'),
    
    # Shopping List
    path('shopping-list/', shopping_list, name='shopping_list'),
    path('recipe/<int:recipe_id>/add-to-list/', add_to_shopping_list, name='add_to_shopping_list'),
    path('shopping-list/<int:item_id>/toggle/', toggle_shopping_item, name='toggle_shopping_item'),
    path('shopping-list/clear/', clear_shopping_list, name='clear_shopping_list'),
    
    # API endpoints (legacy)
    path('api/ingredient_id/<ingredientName>', get_ingredientId),
    path('api/match_recipe/', get_match_recipe),
]
