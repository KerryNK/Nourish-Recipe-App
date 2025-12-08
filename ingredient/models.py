from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

# ============ LEGACY MODELS (Keep for backward compatibility) ============
class ingredientItem(models.Model):
  name = models.TextField()
  property = models.TextField()
  img_url = models.TextField()

class recipeItem(models.Model):
  name = models.TextField()
  ingredients = models.TextField()
  directions = models.TextField()
  img_url = models.TextField()
  list_ingredient = models.ManyToManyField(ingredientItem)


# ============ NEW MODELS (Proper structure) ============

class Ingredient(models.Model):
  """Improved ingredient model with categories"""
  CATEGORIES = [
      ('vegetable', 'Vegetables'),
      ('fruit', 'Fruits'),
      ('grain', 'Grains'),
      ('protein', 'Proteins'),
      ('dairy', 'Dairy'),
      ('spice', 'Spices'),
      ('oil', 'Oils & Condiments'),
      ('other', 'Other'),
  ]
  
  name = models.CharField(max_length=255, unique=True)
  category = models.CharField(max_length=50, choices=CATEGORIES, default='other')
  img_url = models.URLField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return self.name
  
  class Meta:
    ordering = ['name']


class Recipe(models.Model):
  """Improved recipe model with proper fields"""
  DIFFICULTY_CHOICES = [
      ('easy', 'Easy'),
      ('medium', 'Medium'),
      ('hard', 'Hard'),
  ]
  
  CATEGORY_CHOICES = [
      ('breakfast', 'Breakfast'),
      ('lunch', 'Lunch'),
      ('dinner', 'Dinner'),
      ('snack', 'Snack'),
      ('dessert', 'Dessert'),
      ('beverage', 'Beverage'),
      ('other', 'Other'),
  ]
  
  title = models.CharField(max_length=255)
  description = models.TextField(blank=True)
  prep_time = models.IntegerField(default=15, help_text="minutes")
  cook_time = models.IntegerField(default=30, help_text="minutes")
  servings = models.IntegerField(default=4)
  difficulty = models.CharField(max_length=50, choices=DIFFICULTY_CHOICES, default='medium')
  category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='other')
  image = models.URLField(blank=True)  # Using URL for now, can switch to ImageField later
  created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  is_published = models.BooleanField(default=True)
  views_count = models.IntegerField(default=0)
  
  def __str__(self):
    return self.title
  
  def average_rating(self):
    """Calculate average rating from ratings"""
    ratings = self.ratings.all()
    if ratings.count() == 0:
      return 0
    return sum([r.score for r in ratings]) / ratings.count()
  
  class Meta:
    ordering = ['-created_at']


class RecipeIngredient(models.Model):
  """Junction table for Recipe-Ingredient with amount and unit"""
  UNIT_CHOICES = [
      ('g', 'grams'),
      ('kg', 'kilograms'),
      ('ml', 'milliliters'),
      ('l', 'liters'),
      ('tbsp', 'tablespoons'),
      ('tsp', 'teaspoons'),
      ('cup', 'cups'),
      ('piece', 'pieces'),
      ('whole', 'whole'),
      ('pinch', 'pinches'),
      ('dash', 'dashes'),
  ]
  
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
  ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
  amount = models.DecimalField(max_digits=8, decimal_places=2)
  unit = models.CharField(max_length=50, choices=UNIT_CHOICES)
  notes = models.CharField(max_length=255, blank=True)  # e.g., "chopped", "minced"
  
  def __str__(self):
    return f"{self.amount} {self.unit} {self.ingredient.name} for {self.recipe.title}"
  
  class Meta:
    ordering = ['id']


class RecipeStep(models.Model):
  """Ordered cooking steps for recipes"""
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
  order = models.IntegerField()
  instruction = models.TextField()
  time_minutes = models.IntegerField(null=True, blank=True, help_text="Time for this step (optional)")
  
  def __str__(self):
    return f"Step {self.order}: {self.recipe.title}"
  
  class Meta:
    ordering = ['order']
    unique_together = ('recipe', 'order')


class Favorite(models.Model):
  """User's favorite recipes"""
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_recipes')
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorited_by')
  saved_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.user.username} saved {self.recipe.title}"
  
  class Meta:
    unique_together = ('user', 'recipe')
    ordering = ['-saved_at']


class Rating(models.Model):
  """User ratings for recipes (1-5 stars)"""
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  score = models.IntegerField(
      validators=[MinValueValidator(1), MaxValueValidator(5)],
      help_text="1-5 stars"
  )
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.user.username} rated {self.recipe.title} {self.score} stars"
  
  class Meta:
    unique_together = ('recipe', 'user')
    ordering = ['-created_at']


class Review(models.Model):
  """User reviews for recipes"""
  recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  title = models.CharField(max_length=255)
  text = models.TextField()
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  helpful_count = models.IntegerField(default=0)
  
  def __str__(self):
    return f"Review by {self.user.username}: {self.title}"
  
  class Meta:
    ordering = ['-created_at']


class ShoppingList(models.Model):
  """User's shopping list"""
  user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shopping_list')
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"Shopping list for {self.user.username}"


class ShoppingListItem(models.Model):
  """Items in shopping list"""
  shopping_list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
  ingredient_name = models.CharField(max_length=255)
  amount = models.DecimalField(max_digits=8, decimal_places=2)
  unit = models.CharField(max_length=50)
  is_purchased = models.BooleanField(default=False)
  from_recipe = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.SET_NULL)
  created_at = models.DateTimeField(auto_now_add=True)
  
  def __str__(self):
    return f"{self.amount} {self.unit} {self.ingredient_name}"
  
  class Meta:
    ordering = ['is_purchased', '-created_at']


class IngredientPrice(models.Model):
  """Kenyan market prices for ingredients"""
  MARKET_CHOICES = [
      ('nairobi', 'Nairobi'),
      ('eldoret', 'Eldoret'),
      ('kisumu', 'Kisumu'),
      ('mombasa', 'Mombasa'),
      ('nakuru', 'Nakuru'),
      ('average', 'Kenya Average'),
  ]
  
  ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE, related_name='prices')
  unit = models.CharField(max_length=50)
  price_kes = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price in KES")
  market = models.CharField(max_length=50, choices=MARKET_CHOICES, default='average')
  updated_at = models.DateTimeField(auto_now=True)
  notes = models.CharField(max_length=255, blank=True)
  
  def __str__(self):
    return f"{self.ingredient.name} - {self.price_kes} KES per {self.unit} ({self.market})"
  
  class Meta:
    unique_together = ('ingredient', 'unit', 'market')
    ordering = ['ingredient', 'market']