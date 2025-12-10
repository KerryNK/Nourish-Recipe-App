from django.contrib.auth.models import User
from ingredient.models import Recipe

# Assign different creators to recipes for variety
assignments = [
    (1, 'demo'),       # Ugali & Sukuma Wiki - Demo User
    (2, 'Keryy'),      # Nyama Choma - Kerry Koech
    (3, 'testuser123'), # Chapati - testuser123
    (4, 'favtest'),    # Beans & Lentils Stew - favtest
    (5, 'shoptest'),   # Pilau - shoptest
    (6, 'Keryy'),      # Pancakes - Kerry Koech (keep as is)
]

print("Assigning different creators to recipes...")
print("-" * 50)

for recipe_id, username in assignments:
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        user = User.objects.get(username=username)
        recipe.created_by = user
        recipe.save()
        creator_name = user.get_full_name() or user.username
        print(f"✓ Recipe {recipe_id}: '{recipe.title}' → {creator_name}")
    except Recipe.DoesNotExist:
        print(f"✗ Recipe {recipe_id} not found")
    except User.DoesNotExist:
        print(f"✗ User '{username}' not found")

print("\n" + "=" * 50)
print("Done! Now recipes have different creators.")
print("\nYou can also add full names to users:")
print("user = User.objects.get(username='testuser123')")
print("user.first_name = 'Test'")
print("user.last_name = 'User'")
print("user.save()")
