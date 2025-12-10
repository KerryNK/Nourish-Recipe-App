from django.contrib.auth.models import User
from ingredient.models import Recipe

# Check current recipe creators
print("Current recipes and their creators:")
print("-" * 50)
for recipe in Recipe.objects.all():
    creator = recipe.created_by.username if recipe.created_by else "No creator"
    print(f"{recipe.id}. {recipe.title[:30]:<30} - By: {creator}")

print("\n" + "=" * 50)
print("Available users:")
print("-" * 50)
for user in User.objects.all():
    full_name = user.get_full_name() or "No full name"
    print(f"{user.id}. {user.username:<15} - {full_name}")

print("\n" + "=" * 50)
print("\nTo assign different creators to recipes, run:")
print("recipe = Recipe.objects.get(id=RECIPE_ID)")
print("user = User.objects.get(username='USERNAME')")
print("recipe.created_by = user")
print("recipe.save()")
