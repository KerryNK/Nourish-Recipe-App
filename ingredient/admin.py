from django.contrib import admin
from .models import (
    ingredientItem, recipeItem, Ingredient, Recipe, RecipeIngredient, 
    RecipeStep, Favorite, Rating, Review, ShoppingList, ShoppingListItem,
    IngredientPrice
)


# ============ LEGACY MODELS ============
@admin.register(ingredientItem)
class IngredientItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'property')
    search_fields = ('name',)


@admin.register(recipeItem)
class RecipeItemAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


# ============ NEW MODELS ============

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    fields = ('ingredient', 'amount', 'unit', 'notes')


class RecipeStepInline(admin.TabularInline):
    model = RecipeStep
    extra = 1
    fields = ('order', 'instruction', 'time_minutes')
    ordering = ('order',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'created_by', 'is_published', 'views_count', 'created_at')
    list_filter = ('category', 'difficulty', 'is_published', 'created_at')
    search_fields = ('title', 'description')
    list_editable = ('is_published',)
    readonly_fields = ('views_count', 'created_at', 'updated_at')
    inlines = [RecipeIngredientInline, RecipeStepInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image', 'created_by')
        }),
        ('Recipe Details', {
            'fields': ('category', 'difficulty', 'prep_time', 'cook_time', 'servings')
        }),
        ('Publishing', {
            'fields': ('is_published', 'views_count', 'created_at', 'updated_at')
        }),
    )
    
    actions = ['publish_recipes', 'unpublish_recipes']
    
    def publish_recipes(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f'{updated} recipe(s) published successfully.')
    publish_recipes.short_description = 'Publish selected recipes'
    
    def unpublish_recipes(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f'{updated} recipe(s) unpublished successfully.')
    unpublish_recipes.short_description = 'Unpublish selected recipes'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'recipe__title')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('recipe__title', 'user__username')


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'user', 'title', 'created_at', 'helpful_count')
    list_filter = ('created_at',)
    search_fields = ('recipe__title', 'user__username', 'title', 'text')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at', 'updated_at')
    search_fields = ('user__username',)


@admin.register(ShoppingListItem)
class ShoppingListItemAdmin(admin.ModelAdmin):
    list_display = ('ingredient_name', 'amount', 'unit', 'is_purchased', 'shopping_list')
    list_filter = ('is_purchased', 'unit')
    search_fields = ('ingredient_name',)


@admin.register(IngredientPrice)
class IngredientPriceAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'price_kes', 'unit', 'market', 'updated_at')
    list_filter = ('market', 'updated_at')
    search_fields = ('ingredient__name',)
