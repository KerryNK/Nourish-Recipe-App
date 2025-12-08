# 🌿 Nourish Recipe App — Strategic Feature Roadmap

**Current Status:** Django MVP with ingredient search and recipe display  
**Target:** Full-featured recipe platform with personalization and community

---

## 📊 Feature Prioritization Matrix

### **PHASE 1: MVP FOUNDATION (WEEKS 1-2)**
Core features that make the app *actually usable*.

#### **P1.1 — Refactor Data Models** ✅ CRITICAL
**Current Problem:** Models use `TextField` with `#` delimiters for structured data. This is fragile and doesn't scale.

**Solution:**
```python
# Better structure:
class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    prep_time = models.IntegerField(help_text="minutes")
    cook_time = models.IntegerField(help_text="minutes")
    servings = models.IntegerField(default=4)
    difficulty = models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')])
    category = models.CharField(choices=[...])  # Breakfast, Lunch, Dinner, Dessert
    image = models.ImageField(upload_to='recipes/')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(choices=[('g', 'grams'), ('ml', 'milliliters'), ('tbsp', 'tablespoons'), ...])

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)
    category = models.CharField(choices=[...])  # Vegetables, Spices, Proteins, etc.

class RecipeStep(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps')
    order = models.IntegerField()
    instruction = models.TextField()
    time_minutes = models.IntegerField(null=True)  # Optional: time for this step
```

**Why:** Enables filtering, scaling, nutritional tracking, and future features.

---

#### **P1.2 — User Authentication** ✅ CRITICAL
**What:** Signup → Login → User Profile

**Scope:**
- Django's built-in `User` model (no custom auth)
- Email + password registration
- Login/logout views
- Password reset (email)
- User profile page

**Files to create:**
- `ingredient/forms.py` — SignupForm, LoginForm
- `ingredient/views.py` — signup, login, logout, profile views
- `templates/auth/` — signup.html, login.html, profile.html
- `templates/base.html` — navbar with user menu

**Why Critical:**
Users must be authenticated to save favorites, post recipes, leave reviews.

---

#### **P1.3 — Recipe Detail View** ✅ CRITICAL
**Current:** You have a search results page, but no dedicated recipe detail page.

**What to build:**
- URL: `/recipe/<recipe-id>/`
- Display: title, image, prep/cook time, servings, difficulty, ingredients, steps
- Sections: ratings, reviews, comments
- Actions: Save to favorites, Share, Print

**Why Critical:**
Recipe detail is the heart of the app UX.

---

### **PHASE 2: PERSONALIZATION (WEEKS 3-4)**
Features that make users *come back*.

#### **P2.1 — Favorites / Bookmarks** ⭐
**Model:**
```python
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'recipe')
```

**UI:**
- Heart icon (or star) on recipe cards
- Click to save/unsave
- `/my-favorites/` page to view saved recipes

**Why:** Low effort, high stickiness. People return to find recipes they saved.

---

#### **P2.2 — Ratings & Reviews** ⭐
**Models:**
```python
class Rating(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # 1-5 stars
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('recipe', 'user')

class Review(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    helpful_count = models.IntegerField(default=0)
```

**UI:**
- Star rating on recipe detail page
- Submit review form (logged-in users only)
- Display average rating
- List of reviews below recipe

**Why:** Social proof. Reviews drive engagement and help users discover recipes.

---

#### **P2.3 — Shopping List Generator** ⭐⭐⭐
**This is a KILLER feature.** Most people use recipe apps to plan meals and buy groceries.

**What:**
- Click "Add to Shopping List" on any recipe
- Consolidate ingredients from multiple recipes
- Mark items as purchased
- Export/print list

**Model:**
```python
class ShoppingList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ShoppingListItem(models.Model):
    list = models.ForeignKey(ShoppingList, on_delete=models.CASCADE, related_name='items')
    ingredient = models.CharField(max_length=255)  # name (not FK to Ingredient, for flexibility)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(max_length=50)
    is_purchased = models.BooleanField(default=False)
    from_recipe = models.ForeignKey(Recipe, null=True, on_delete=models.SET_NULL)
```

**UI:**
- `/shopping-list/` page
- Checkboxes to mark items purchased
- Search to add items manually
- Clear list button

**Why:** Converts recipe viewers into *active planners*. High value.

---

### **PHASE 3: DISCOVERY & ENGAGEMENT (WEEKS 5-6)**

#### **P3.1 — Advanced Search & Filters** ⭐⭐
**Current:** Search by single ingredient. Too limiting.

**Enhance to:**
- Multi-ingredient search (all must be present)
- Filter by:
  - Category (breakfast, lunch, dinner, dessert)
  - Difficulty (easy, medium, hard)
  - Prep time (under 15 min, 15-30, 30-60, 1+ hour)
  - Dietary type (vegetarian, vegan, keto, gluten-free) — requires new `Recipe.dietary_tags` field
- Sort by:
  - Newest
  - Highest rated
  - Most saved
  - Quickest to cook

**Why:** Better UX. Users get recipes that match their needs.

---

#### **P3.2 — Recipe Serving Scaler** ⭐⭐
**What:**
- On recipe detail page: input box "Adjust servings"
- JavaScript updates all ingredient amounts in real-time

**Example:**
- Recipe serves 4, user wants 8 → all amounts double
- Work with standard units (g, ml, cups, tbsp, tsp)

**Why:** Practical. People always adjust servings. Makes your app more useful.

---

### **PHASE 4: COMMUNITY & CONTENT (WEEKS 7-8)**

#### **P4.1 — User-Generated Recipes** ⭐
**Currently missing:** Users can't submit recipes!

**What:**
- Form to create/edit recipe (logged-in users only)
- Upload recipe image
- Add ingredients with amounts/units
- Add steps with optional time estimates
- Save as draft (don't publish immediately)
- Submit for review

**Admin Panel:**
- Approve/reject submitted recipes
- Edit before publishing

**Why:** You become a platform, not just a recipe database. Exponential content growth.

---

#### **P4.2 — Social Sharing** ⭐
**What:**
- Share buttons: Facebook, X (Twitter), Pinterest, Email
- Generate nice "Open Graph" preview (recipe image + title)

**Libraries:**
- Use `django-social-django` or just plain URLs to share endpoints

**Why:** Free marketing. Users share recipes → friends discover your app.

---

### **PHASE 5: "NOURISH-SPECIFIC" FEATURES (Future)**

#### **P5.1 — Recipe Costing (Kenyan Market Prices)** ⭐⭐⭐ DIFFERENTIATION
**Why this is powerful:** No other recipe app does this. You'd own a niche.

**Implementation:**
```python
class IngredientPrice(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    unit = models.CharField(max_length=50)
    price_kes = models.DecimalField(max_digits=8, decimal_places=2)  # Kenya Shilling
    market = models.CharField(choices=[('nairobi', 'Nairobi'), ('eldoret', 'Eldoret'), ...])
    updated_at = models.DateTimeField(auto_now=True)

# On recipe detail: show "Estimated cost: KES 350" per serving
```

**Challenge:** Maintaining price data. Partner with local markets or crowdsource.

---

#### **P5.2 — Dietary Modes (Smart Recommendation)** ⭐⭐⭐ DIFFERENTIATION
**Modes:**
- Weight loss (low-calorie, high-protein)
- Budget meals (low-cost)
- Fast meals (under 30 minutes)
- Clean eating (whole foods, no processed)
- High protein (fitness-focused)

**Implementation:**
- Add tags to recipes
- Filter recipes by selected mode on homepage

---

#### **P5.3 — Meal Planner Calendar** ⭐⭐
**What:**
- 7-day view (Mon-Sun)
- 3 slots per day (breakfast, lunch, dinner)
- Drag-drop recipes into slots
- Auto-generates shopping list from selected recipes

**Why:** Sticky feature. People plan their whole week and come back daily.

---

#### **P5.4 — Voice Cooking Mode** ⭐ ACCESSIBILITY
**What:**
- Button to switch to "cooking mode"
- Larger text, bigger buttons
- Tap "Next Step" to advance through instructions
- Optional: text-to-speech for hands-free cooking

**Why:** Accessibility feature. Stands out vs competitors.

---

## 🎨 UI/UX Priorities

### **Phase 1 (Immediate)**
- [ ] Responsive navbar with user menu
- [ ] Clean recipe detail page (mobile-first design)
- [ ] Login/signup pages (simple, trust-building)

### **Phase 2**
- [ ] Favorites button (heart icon)
- [ ] Reviews section with star ratings
- [ ] Shopping list page (clean, printable)

### **Phase 3**
- [ ] Advanced search/filter sidebar
- [ ] Serving size adjuster
- [ ] Better recipe card design (image, rating, time badges)

---

## 🔧 Technical Debt to Address

1. **Image uploads:** Currently using `img_url` (string). Switch to Django's `ImageField` + local storage (or AWS S3).
2. **API responses:** JSON responses are fragile. Add proper serialization (Django REST Framework optional, or better JSON responses).
3. **CSS/JS:** Refactor static files. Consider Bootstrap 5 for modern, responsive UI.
4. **Database:** Migrate from splitting strings (`#`) to proper relationships.

---

## 📈 Success Metrics

Track these to know if features are working:

| Metric | Target |
|--------|--------|
| User registrations | 50+ in first month |
| Recipe views/day | 100+ |
| Saved recipes/user | 5+ average |
| Return rate (DAU/MAU) | 30%+ |
| Recipe submissions/month | 10+ |

---

## 🚀 Recommended Implementation Order

1. **Week 1:** Refactor models + user auth
2. **Week 2:** Recipe detail page + favorites
3. **Week 3:** Ratings/reviews + shopping list
4. **Week 4:** Advanced search + serving scaler
5. **Week 5+:** User recipes + social + costing

---

## 🎯 "Why This Matters for Nourish"

You're building a recipe app. **Don't be basic.** Here's why each feature matters:

- **Authentication:** Enables all personalization. Without it, you're just a website.
- **Favorites:** Makes people return (stickiness).
- **Reviews:** Social proof. Drives engagement & trust.
- **Shopping List:** Solves a *real problem*. People use your app weekly.
- **Advanced Search:** Prevents frustration. Users find what they need fast.
- **User Recipes:** Turns you into a *platform*. Content grows automatically.
- **Recipe Costing:** **Your differentiator.** No other app in Kenya does this.

---

**Ready to build?** Pick one feature and I'll implement it end-to-end (model → view → template → tests).
