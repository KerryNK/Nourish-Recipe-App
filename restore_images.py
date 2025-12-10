from ingredient.models import Recipe

print("Restoring correct image filenames...")
print("-" * 60)

# Map of recipe IDs to their ACTUAL static image filenames
correct_images = {
    1: 'ugaliwiki.png',
    2: 'nyamachoma.png', 
    3: 'chapati.png',
    4: 'lentils.png',
    5: 'pilau.png',
    # Recipe 6 already has the uploaded pancake image
}

for recipe_id, filename in correct_images.items():
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        recipe.image = filename
        recipe.save()
        print(f"✓ Recipe {recipe_id}: '{recipe.title}' → {filename}")
    except Recipe.DoesNotExist:
        print(f"✗ Recipe {recipe_id} not found")

print("\n" + "=" * 60)
print("Done! Images should now display correctly.")
