from django.contrib.auth.models import User
from ingredient.models import Recipe, Favorite

print("Checking favorites...")
print("-" * 60)

# Check all favorites
favorites = Favorite.objects.all()
print(f"Total favorites in database: {favorites.count()}")
print()

if favorites.exists():
    print("Current favorites:")
    for fav in favorites:
        print(f"  - {fav.user.username} favorited '{fav.recipe.title}'")
else:
    print("No favorites found in the database.")

print("\n" + "=" * 60)
print("\nChecking by user:")
for user in User.objects.all():
    user_favs = Favorite.objects.filter(user=user)
    if user_favs.exists():
        print(f"\n{user.username}:")
        for fav in user_favs:
            print(f"  - {fav.recipe.title}")
