from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # ADD THIS LINE
from django.conf.urls.static import static  # ADD THIS LINE IF MISSING
from ingredient.views import (
    ingredientView, searchView, get_ingredientId, get_match_recipe,
    signup, login_view, logout_view, profile,
    home, recipes, recipe_detail, toggle_favorite,
    my_favorites, my_recipes, add_review, add_rating,
    shopping_list, add_to_shopping_list, toggle_shopping_item, clear_shopping_list,
    delete_shopping_item, add_manual_shopping_item
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
    path('shopping-list/<int:item_id>/delete/', delete_shopping_item, name='delete_shopping_item'),
    path('shopping-list/add-manual/', add_manual_shopping_item, name='add_manual_shopping_item'),
    path('shopping-list/clear/', clear_shopping_list, name='clear_shopping_list'),
    
    # API endpoints (legacy)
    path('api/ingredient_id/<ingredientName>', get_ingredientId),
    path('api/match_recipe/', get_match_recipe),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
