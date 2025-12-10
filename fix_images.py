from ingredient.models import Recipe

print("Checking recipe images...")
print("-" * 60)

for recipe in Recipe.objects.all():
    image_value = recipe.image
    image_str = str(image_value) if image_value else "None"
    print(f"{recipe.id}. {recipe.title[:30]:<30} | Image: {image_str}")

print("\n" + "=" * 60)
print("\nFixing image paths for static images...")
print("-" * 60)

# Map of recipe IDs to their static image filenames
static_images = {
    1: 'ugali.png',
    2: 'nyama_choma.png', 
    3: 'chapati.png',
    4: 'beans.png',
    5: 'pilau.png',
    # Recipe 6 (pancakes) might have an uploaded image or needs one
}

for recipe_id, filename in static_images.items():
    try:
        recipe = Recipe.objects.get(id=recipe_id)
        recipe.image = filename
        recipe.save()
        print(f"✓ Recipe {recipe_id}: Set image to '{filename}'")
    except Recipe.DoesNotExist:
        print(f"✗ Recipe {recipe_id} not found")

print("\nDone!")
