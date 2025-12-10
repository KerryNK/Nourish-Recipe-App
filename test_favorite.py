from django.contrib.auth.models import User
from ingredient.models import Recipe, Favorite

# Get or create the ciarrai user
try:
    user = User.objects.get(username='ciarrai')
    print(f"Found user: {user.username}")
except User.DoesNotExist:
    print("User 'ciarrai' not found. Available users:")
    for u in User.objects.all():
        print(f"  - {u.username}")
    exit()

# Get a recipe to favorite
recipe = Recipe.objects.first()
print(f"Recipe to favorite: {recipe.title}")

# Create a favorite
favorite, created = Favorite.objects.get_or_create(user=user, recipe=recipe)

if created:
    print(f"✓ Created new favorite for {user.username}: {recipe.title}")
else:
    print(f"✓ Favorite already exists for {user.username}: {recipe.title}")

# Check all favorites for this user
print(f"\nAll favorites for {user.username}:")
user_favorites = Favorite.objects.filter(user=user)
for fav in user_favorites:
    print(f"  - {fav.recipe.title}")
