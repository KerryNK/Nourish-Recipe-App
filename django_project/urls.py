from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ingredient import views as ingredient_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Include all URLs from the ingredient app
    path('', include('ingredient.urls')),

    # Home & Recipes
    path('', ingredient_views.home, name='home'),
    path('recipes/', ingredient_views.recipes, name='recipes'),
    path('recipe/<int:recipe_id>/', ingredient_views.recipe_detail, name='recipe_detail'),
    
    # Legacy ingredient search (keep for compatibility)
    path('ingredients/', ingredient_views.ingredientView),
    path('search/<int:ingredientId>/', ingredient_views.searchView),
    
    # Authentication
    path('signup/', ingredient_views.signup, name='signup'),
    path('login/', ingredient_views.login_view, name='login'),
    path('logout/', ingredient_views.logout_view, name='logout'),
    path('profile/', ingredient_views.profile, name='profile'),
    
    # Favorites
    path('favorites/', ingredient_views.my_favorites, name='my_favorites'),
    path('recipe/<int:recipe_id>/favorite/', ingredient_views.toggle_favorite, name='toggle_favorite'),
    
    # Recipes
    path('my-recipes/', ingredient_views.my_recipes, name='my_recipes'),
    path('community/', ingredient_views.community, name='community'),
    path('recipe/add/', ingredient_views.create_recipe, name='create_recipe'),
    path('recipe/<int:recipe_id>/edit/', ingredient_views.edit_recipe, name='edit_recipe'),
    
    # Comments & Likes
    path('recipe/<int:recipe_id>/comment/', ingredient_views.add_comment, name='add_comment'),
    path('recipe/<int:recipe_id>/like/', ingredient_views.toggle_like, name='toggle_like'),
    
    # Reviews & Ratings
    path('recipe/<int:recipe_id>/review/', ingredient_views.add_review, name='add_review'),
    path('recipe/<int:recipe_id>/rating/', ingredient_views.add_rating, name='add_rating'),
    
    # Shopping List
    path('shopping-list/', ingredient_views.shopping_list, name='shopping_list'),
    path('recipe/<int:recipe_id>/add-to-list/', ingredient_views.add_to_shopping_list, name='add_to_shopping_list'),
    path('shopping-list/<int:item_id>/toggle/', ingredient_views.toggle_shopping_item, name='toggle_shopping_item'),
    path('shopping-list/<int:item_id>/delete/', ingredient_views.delete_shopping_item, name='delete_shopping_item'),
    path('shopping-list/add-manual/', ingredient_views.add_manual_shopping_item, name='add_manual_shopping_item'),
    path('shopping-list/clear/', ingredient_views.clear_shopping_list, name='clear_shopping_list'),
    
    # API endpoints (legacy)
    path('api/ingredient_id/<ingredientName>', ingredient_views.get_ingredientId),
    path('api/match_recipe/', ingredient_views.get_match_recipe),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
