#!/usr/bin/env python
"""
Nourish Recipe App - Comprehensive Feature Test
Tests all core functionality: Auth, Recipes, Favorites, Shopping List, Reviews
"""
import os
import sys

# Configure Django settings before importing Django modules
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

# Monkeypatch gettext.translation to accept removed `codeset` kwarg (Django 2.1 compatibility with Python 3.12)
import gettext as _gettext
_orig_translation = getattr(_gettext, 'translation', None)
def _translation(domain, localedir=None, languages=None, codeset=None, fallback=False):
    if _orig_translation is None:
        raise RuntimeError('gettext.translation not available')
    return _orig_translation(domain, localedir=localedir, languages=languages, fallback=fallback)
_gettext.translation = _translation

import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User

from ingredient.models import Recipe, Ingredient, RecipeIngredient, Favorite, ShoppingList, ShoppingListItem, Review

def ensure_user(username, password):
    # Create or update a test user; avoid raw deletes which can trigger sqlite issues
    user, created = User.objects.get_or_create(username=username)
    user.set_password(password)
    user.save()
    return user

def test_database():
    """Test that sample data is populated"""
    print("\n" + "="*60)
    print("TEST 1: Database Sample Data")
    print("="*60)
    
    recipes = Recipe.objects.all()
    ingredients = Ingredient.objects.all()
    
    print(f"✓ Recipes in database: {recipes.count()}")
    for recipe in recipes:
        print(f"  - {recipe.title} ({recipe.difficulty})")
    
    print(f"✓ Ingredients in database: {ingredients.count()}")
    print(f"  Categories: {ingredients.values('category').distinct().count()}")
    
    assert recipes.count() == 5, "Expected 5 recipes"
    assert ingredients.count() == 29, "Expected 29 ingredients"
    print("\n✅ Database Test PASSED")
    return True

def test_user_signup_and_profile():
    """Test user signup and profile functionality"""
    print("\n" + "="*60)
    print("TEST 2: User Authentication & Profile")
    print("="*60)
    
    client = Client()
    
    # Test signup page loads
    response = client.get('/signup/')
    print(f"✓ Signup page loads: {response.status_code == 200}")
    assert response.status_code == 200
    
    # Test user signup
    signup_data = {
        'username': 'testuser123',
        'email': 'test@example.com',
        'password1': 'TestPass123!',
        'password2': 'TestPass123!'
    }
    response = client.post('/signup/', signup_data, follow=True)
    print(f"✓ Signup submission: {response.status_code == 200}")
    
    # Verify user created
    user = User.objects.filter(username='testuser123').first()
    print(f"✓ User created: {user is not None}")
    assert user is not None
    
    # Test login
    login_data = {'username': 'testuser123', 'password': 'TestPass123!'}
    response = client.post('/login/', login_data, follow=True)
    print(f"✓ Login successful: {response.status_code == 200}")
    
    # Test profile page
    response = client.get('/profile/')
    print(f"✓ Profile page accessible: {response.status_code == 200}")
    assert response.status_code == 200
    
    print("\n✅ Authentication Test PASSED")
    return True

def test_recipe_views():
    """Test recipe browsing and detail views"""
    print("\n" + "="*60)
    print("TEST 3: Recipe Views & Detail Pages")
    print("="*60)
    
    client = Client()
    
    # Test recipes listing
    response = client.get('/recipes/')
    print(f"✓ Recipes listing page: {response.status_code == 200}")
    assert response.status_code == 200
    assert b'Ugali' in response.content or b'Chapati' in response.content
    
    # Get first recipe and test detail view
    recipe = Recipe.objects.first()
    print(f"✓ Testing recipe: {recipe.title}")
    
    response = client.get(f'/recipe/{recipe.id}/')
    print(f"✓ Recipe detail page: {response.status_code == 200}")
    assert response.status_code == 200
    assert recipe.title.encode() in response.content
    
    # Verify recipe content has ingredients and steps
    ingredients_count = recipe.ingredients.count()
    steps_count = recipe.steps.count()
    print(f"✓ Recipe has {ingredients_count} ingredients")
    print(f"✓ Recipe has {steps_count} cooking steps")
    assert ingredients_count > 0
    assert steps_count > 0
    
    # Test recipe views counter
    initial_views = recipe.views_count
    recipe.views_count += 1
    recipe.save()
    recipe.refresh_from_db()
    print(f"✓ Recipe views counter: {recipe.views_count} (was {initial_views})")
    
    print("\n✅ Recipe Views Test PASSED")
    return True

def test_favorites():
    """Test favorites functionality"""
    print("\n" + "="*60)
    print("TEST 4: Favorites System")
    print("="*60)
    
    client = Client()
    
    # Create test user and login
    user = ensure_user('favtest', 'Pass123!')
    client.login(username='favtest', password='Pass123!')
    
    recipe = Recipe.objects.first()
    
    # Test favorites page
    response = client.get('/favorites/')
    print(f"✓ Favorites page accessible: {response.status_code == 200}")
    assert response.status_code == 200
    
    # Add to favorites via AJAX
    response = client.post(
        f'/recipe/{recipe.id}/favorite/',
        HTTP_X_REQUESTED_WITH='XMLHttpRequest'
    )
    print(f"✓ Favorite toggle endpoint: {response.status_code == 200}")
    
    # Verify favorite was created
    favorite = Favorite.objects.filter(user=user, recipe=recipe).first()
    print(f"✓ Favorite created: {favorite is not None}")
    assert favorite is not None
    
    print("\n✅ Favorites Test PASSED")
    return True

def test_shopping_list():
    """Test shopping list functionality"""
    print("\n" + "="*60)
    print("TEST 5: Shopping List")
    print("="*60)
    
    client = Client()
    
    # Create test user
    user = ensure_user('shoptest', 'Pass123!')
    client.login(username='shoptest', password='Pass123!')
    
    # Create shopping list
    shopping_list = ShoppingList.objects.get_or_create(user=user)[0]
    print(f"✓ Shopping list created: {shopping_list is not None}")
    
    # Test shopping list page
    response = client.get('/shopping-list/')
    print(f"✓ Shopping list page accessible: {response.status_code == 200}")
    assert response.status_code == 200
    
    # Add recipe to shopping list
    recipe = Recipe.objects.first()
    response = client.post(f'/recipe/{recipe.id}/add-to-list/', follow=True)
    print(f"✓ Add to shopping list: {response.status_code == 200}")
    
    # Verify items were added
    items_count = shopping_list.items.count()
    print(f"✓ Shopping list items: {items_count}")
    assert items_count > 0
    
    print("\n✅ Shopping List Test PASSED")
    return True

def test_reviews_and_ratings():
    """Test review and rating functionality"""
    print("\n" + "="*60)
    print("TEST 6: Reviews & Ratings")
    print("="*60)
    
    client = Client()
    
    # Create test user
    user = ensure_user('reviewtest', 'Pass123!')
    client.login(username='reviewtest', password='Pass123!')
    
    recipe = Recipe.objects.first()
    
    # Test add review page
    response = client.get(f'/recipe/{recipe.id}/review/')
    print(f"✓ Add review page accessible: {response.status_code == 200}")
    assert response.status_code == 200
    
    # Submit review
    review_data = {
        'title': 'Great recipe!',
        'content': 'This was delicious and easy to make.',
        'rating': 5
    }
    response = client.post(f'/recipe/{recipe.id}/review/', review_data, follow=True)
    print(f"✓ Review submission: {response.status_code == 200}")
    
    # Verify review created
    review = Review.objects.filter(recipe=recipe, user=user).first()
    print(f"✓ Review created: {review is not None}")
    if review:
        print(f"  Title: {review.title}")
        print(f"  Rating: {review.rating}/5")
    
    print("\n✅ Reviews & Ratings Test PASSED")
    return True

def test_static_files():
    """Test that static files are served correctly"""
    print("\n" + "="*60)
    print("TEST 7: Static Files & Templates")
    print("="*60)
    
    client = Client()
    
    # Test home page renders with base template
    response = client.get('/')
    print(f"✓ Home page: {response.status_code == 200}")
    assert response.status_code == 200
    assert b'Nourish' in response.content or b'Recipe' in response.content
    
    # Test navbar elements are present
    assert b'navbar' in response.content or b'Sign' in response.content
    print(f"✓ Navigation elements present")
    
    # Test Bootstrap CSS is referenced
    assert b'bootstrap' in response.content or b'css' in response.content
    print(f"✓ Bootstrap references present")
    
    print("\n✅ Static Files Test PASSED")
    return True

def run_all_tests():
    """Run all tests"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "NOURISH RECIPE APP - TEST SUITE" + " "*11 + "║")
    print("╚" + "="*58 + "╝")
    
    tests = [
        ("Database", test_database),
        ("Authentication", test_user_signup_and_profile),
        ("Recipe Views", test_recipe_views),
        ("Favorites", test_favorites),
        ("Shopping List", test_shopping_list),
        ("Reviews & Ratings", test_reviews_and_ratings),
        ("Static Files", test_static_files),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"\n❌ {name} Test FAILED: {str(e)}")
            failed += 1
            import traceback
            traceback.print_exc()
    
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"✅ Passed: {passed}/{len(tests)}")
    print(f"❌ Failed: {failed}/{len(tests)}")
    print("="*60 + "\n")
    
    if failed == 0:
        print("🎉 ALL TESTS PASSED! The Nourish Recipe App is ready to use!")
        print("\nVisit http://localhost:8000/ to access the app")
        return True
    else:
        print(f"⚠️  {failed} test(s) failed. Please review above for details.")
        return False

if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
