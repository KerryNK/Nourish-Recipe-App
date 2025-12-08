from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ingredient.models import Ingredient, Recipe, RecipeIngredient, RecipeStep


class Command(BaseCommand):
    help = 'Seed the database with sample East African recipes'
    
    def handle(self, *args, **options):
        self.stdout.write('🌾 Creating sample recipes...')
        
        # Create a demo user if it doesn't exist
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@nourish.local',
                'first_name': 'Demo',
                'last_name': 'User',
                'is_staff': False
            }
        )
        if created:
            demo_user.set_password('demo123')
            demo_user.save()
            self.stdout.write('✅ Created demo user (demo/demo123)')
        
        # Create Ingredients
        ingredients_data = [
            ('Ugali Flour', 'grain'),
            ('Sukuma Wiki', 'vegetable'),
            ('Tomatoes', 'vegetable'),
            ('Onions', 'vegetable'),
            ('Garlic', 'vegetable'),
            ('Ginger', 'vegetable'),
            ('Oil', 'oil'),
            ('Salt', 'spice'),
            ('Black Pepper', 'spice'),
            ('Cumin', 'spice'),
            ('Turmeric', 'spice'),
            ('Pilau Rice', 'grain'),
            ('Beans', 'protein'),
            ('Lentils', 'protein'),
            ('Chapati Flour', 'grain'),
            ('Eggs', 'protein'),
            ('Milk', 'dairy'),
            ('Coconut Milk', 'dairy'),
            ('Beef', 'protein'),
            ('Chicken', 'protein'),
            ('Nyama Choma Spice', 'spice'),
            ('Coriander', 'spice'),
            ('Chillies', 'vegetable'),
            ('Bell Peppers', 'vegetable'),
            ('Carrots', 'vegetable'),
            ('Potatoes', 'vegetable'),
            ('Avocados', 'fruit'),
            ('Bananas', 'fruit'),
            ('Maize', 'grain'),
        ]
        
        ingredients = {}
        for name, category in ingredients_data:
            ingredient, _ = Ingredient.objects.get_or_create(
                name=name,
                defaults={'category': category}
            )
            ingredients[name] = ingredient
        
        self.stdout.write(f'✅ Created {len(ingredients)} ingredients')
        
        # Recipe 1: Ugali & Sukuma Wiki
        recipe1, created = Recipe.objects.get_or_create(
            title='Ugali & Sukuma Wiki',
            defaults={
                'description': 'A classic East African staple meal combining maize porridge with sautéed collard greens.',
                'prep_time': 10,
                'cook_time': 25,
                'servings': 4,
                'difficulty': 'easy',
                'category': 'dinner',
                'image': 'https://via.placeholder.com/400x300?text=Ugali+Sukuma+Wiki',
                'created_by': demo_user,
                'is_published': True,
            }
        )
        
        if created:
            recipe1_ingredients = [
                (ingredients['Ugali Flour'], 4, 'cup', ''),
                (ingredients['Sukuma Wiki'], 500, 'g', 'chopped'),
                (ingredients['Tomatoes'], 3, 'piece', 'chopped'),
                (ingredients['Onions'], 2, 'piece', 'diced'),
                (ingredients['Garlic'], 3, 'clove', 'minced'),
                (ingredients['Oil'], 3, 'tbsp', ''),
                (ingredients['Salt'], 1, 'tsp', ''),
                (ingredients['Black Pepper'], 0.5, 'tsp', ''),
            ]
            
            for ingredient, amount, unit, notes in recipe1_ingredients:
                RecipeIngredient.objects.create(
                    recipe=recipe1,
                    ingredient=ingredient,
                    amount=amount,
                    unit=unit,
                    notes=notes
                )
            
            recipe1_steps = [
                'Boil 4 cups of water in a large pot.',
                'Slowly pour in the ugali flour while stirring to avoid lumps.',
                'Stir continuously for 20 minutes until thick and paste-like.',
                'In a separate pan, heat oil and sauté onions and garlic.',
                'Add chopped tomatoes and cook for 5 minutes.',
                'Add sukuma wiki and cook for 10 minutes until tender.',
                'Season with salt and black pepper.',
                'Serve the ugali on a platter with sukuma wiki on the side.',
            ]
            
            for order, instruction in enumerate(recipe1_steps, 1):
                RecipeStep.objects.create(
                    recipe=recipe1,
                    order=order,
                    instruction=instruction,
                    time_minutes=None
                )
        
        # Recipe 2: Nyama Choma
        recipe2, created = Recipe.objects.get_or_create(
            title='Nyama Choma (Grilled Meat)',
            defaults={
                'description': 'Seasoned and grilled meat strips - a beloved East African BBQ dish.',
                'prep_time': 30,
                'cook_time': 20,
                'servings': 4,
                'difficulty': 'medium',
                'category': 'dinner',
                'image': 'https://via.placeholder.com/400x300?text=Nyama+Choma',
                'created_by': demo_user,
                'is_published': True,
            }
        )
        
        if created:
            recipe2_ingredients = [
                (ingredients['Beef'], 800, 'g', 'cut into chunks'),
                (ingredients['Oil'], 3, 'tbsp', ''),
                (ingredients['Onions'], 2, 'piece', ''),
                (ingredients['Garlic'], 4, 'clove', 'minced'),
                (ingredients['Cumin'], 1, 'tsp', ''),
                (ingredients['Black Pepper'], 1, 'tsp', ''),
                (ingredients['Salt'], 1.5, 'tsp', ''),
                (ingredients['Chillies'], 2, 'piece', 'chopped'),
            ]
            
            for ingredient, amount, unit, notes in recipe2_ingredients:
                RecipeIngredient.objects.create(
                    recipe=recipe2,
                    ingredient=ingredient,
                    amount=amount,
                    unit=unit,
                    notes=notes
                )
            
            recipe2_steps = [
                'Cut beef into uniform chunks.',
                'Mix cumin, black pepper, salt, and minced garlic.',
                'Coat beef pieces with the spice mixture.',
                'Thread beef onto skewers.',
                'Heat grill or charcoal fire to high temperature.',
                'Grill skewers for 15-20 minutes, turning occasionally.',
                'Meat should be charred outside and cooked inside.',
                'Serve hot with onion and chili accompaniments.',
            ]
            
            for order, instruction in enumerate(recipe2_steps, 1):
                RecipeStep.objects.create(
                    recipe=recipe2,
                    order=order,
                    instruction=instruction,
                    time_minutes=None
                )
        
        # Recipe 3: Chapati
        recipe3, created = Recipe.objects.get_or_create(
            title='Chapati (Flatbread)',
            defaults={
                'description': 'Soft, flaky Indian-East African flatbread that\'s perfect with any meal.',
                'prep_time': 15,
                'cook_time': 30,
                'servings': 6,
                'difficulty': 'easy',
                'category': 'breakfast',
                'image': 'https://via.placeholder.com/400x300?text=Chapati',
                'created_by': demo_user,
                'is_published': True,
            }
        )
        
        if created:
            recipe3_ingredients = [
                (ingredients.get('Chapati Flour'), 3, 'cup', ''),
                # Water is omitted from ingredients list (use approximate water when cooking)
                (ingredients.get('Oil'), 2, 'tbsp', ''),
                (ingredients.get('Salt'), 0.5, 'tsp', ''),
            ]
            
            for ingredient, amount, unit, notes in recipe3_ingredients:
                try:
                    RecipeIngredient.objects.create(
                        recipe=recipe3,
                        ingredient=ingredient,
                        amount=amount,
                        unit=unit,
                        notes=notes
                    )
                except:
                    pass
            
            recipe3_steps = [
                'Mix flour and salt in a large bowl.',
                'Add water gradually and knead until you get a soft dough.',
                'Let dough rest for 15 minutes.',
                'Divide dough into 6 equal portions.',
                'Roll each portion into a thin circle.',
                'Heat oil in a skillet over medium heat.',
                'Place chapati in skillet and cook for 30 seconds per side.',
                'Press gently with a cloth to make it puff up.',
                'Serve hot with curries or stews.',
            ]
            
            for order, instruction in enumerate(recipe3_steps, 1):
                RecipeStep.objects.create(
                    recipe=recipe3,
                    order=order,
                    instruction=instruction,
                    time_minutes=None
                )
        
        # Recipe 4: Beans & Lentils Stew
        recipe4, created = Recipe.objects.get_or_create(
            title='Beans & Lentils Stew',
            defaults={
                'description': 'Nutritious and hearty vegetarian stew loaded with protein-rich legumes.',
                'prep_time': 20,
                'cook_time': 60,
                'servings': 6,
                'difficulty': 'medium',
                'category': 'lunch',
                'image': 'https://via.placeholder.com/400x300?text=Beans+Stew',
                'created_by': demo_user,
                'is_published': True,
            }
        )
        
        if created:
            recipe4_ingredients = [
                (ingredients['Beans'], 2, 'cup', 'dried, soaked'),
                (ingredients['Lentils'], 1, 'cup', 'dried'),
                (ingredients['Tomatoes'], 4, 'piece', 'chopped'),
                (ingredients['Onions'], 3, 'piece', 'diced'),
                (ingredients['Garlic'], 4, 'clove', 'minced'),
                (ingredients['Carrots'], 2, 'piece', 'chopped'),
                (ingredients['Oil'], 3, 'tbsp', ''),
                (ingredients['Cumin'], 1, 'tsp', ''),
                (ingredients['Turmeric'], 0.5, 'tsp', ''),
                (ingredients['Salt'], 1, 'tsp', ''),
            ]
            
            for ingredient, amount, unit, notes in recipe4_ingredients:
                RecipeIngredient.objects.create(
                    recipe=recipe4,
                    ingredient=ingredient,
                    amount=amount,
                    unit=unit,
                    notes=notes
                )
            
            recipe4_steps = [
                'Soak beans overnight and rinse.',
                'Heat oil and sauté onions, garlic, and carrots.',
                'Add tomatoes and cook for 5 minutes.',
                'Add beans and lentils with 6 cups of water.',
                'Add cumin, turmeric, and salt.',
                'Bring to a boil, then simmer for 45-60 minutes.',
                'Stir occasionally until beans and lentils are tender.',
                'Adjust seasoning to taste.',
                'Serve hot with rice or ugali.',
            ]
            
            for order, instruction in enumerate(recipe4_steps, 1):
                RecipeStep.objects.create(
                    recipe=recipe4,
                    order=order,
                    instruction=instruction,
                    time_minutes=None
                )
        
        # Recipe 5: Pilau (Spiced Rice)
        recipe5, created = Recipe.objects.get_or_create(
            title='Pilau (Spiced Rice)',
            defaults={
                'description': 'Fragrant and flavorful rice dish seasoned with aromatic spices.',
                'prep_time': 15,
                'cook_time': 30,
                'servings': 6,
                'difficulty': 'easy',
                'category': 'dinner',
                'image': 'https://via.placeholder.com/400x300?text=Pilau',
                'created_by': demo_user,
                'is_published': True,
            }
        )
        
        if created:
            recipe5_ingredients = [
                (ingredients['Pilau Rice'], 2, 'cup', 'long grain'),
                (ingredients['Onions'], 2, 'piece', 'diced'),
                (ingredients['Garlic'], 3, 'clove', 'minced'),
                (ingredients['Cumin'], 1, 'tsp', ''),
                (ingredients['Coriander'], 1, 'tsp', ''),
                (ingredients['Oil'], 3, 'tbsp', ''),
                (ingredients['Salt'], 1, 'tsp', ''),
                (ingredients['Black Pepper'], 0.5, 'tsp', ''),
            ]
            
            for ingredient, amount, unit, notes in recipe5_ingredients:
                RecipeIngredient.objects.create(
                    recipe=recipe5,
                    ingredient=ingredient,
                    amount=amount,
                    unit=unit,
                    notes=notes
                )
            
            recipe5_steps = [
                'Wash rice and set aside.',
                'Heat oil in a heavy-bottomed pot.',
                'Add diced onions and sauté until golden.',
                'Add garlic, cumin, and coriander. Cook for 1 minute.',
                'Add rice and stir to coat with oil.',
                'Pour 4 cups of water and bring to a boil.',
                'Reduce heat, cover, and simmer for 20 minutes.',
                'Once water is absorbed and rice is tender, serve.',
            ]
            
            for order, instruction in enumerate(recipe5_steps, 1):
                RecipeStep.objects.create(
                    recipe=recipe5,
                    order=order,
                    instruction=instruction,
                    time_minutes=None
                )
        
        self.stdout.write(self.style.SUCCESS('✅ Successfully created 5 sample recipes!'))
        self.stdout.write(self.style.SUCCESS('✅ Sample recipes are now visible at http://localhost:8000/recipes/'))
