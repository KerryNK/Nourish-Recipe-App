# Recipe APP

<img  width="500" src="https://i.imgur.com/OMgebh0.png">

Recipe App is a django web app that allow user to search recipes by ingredients. There are two ways to search recipes. 1. On home page(ingredient page), user can select `one` ingredient to search recipes by clicking on the ingredient card. 2. On recipes page, user can search recipes by input `multiple` ingredients' name.  

## Built With
- Web framework [Django](https://www.djangoproject.com/) (version 2.1) for this project
- Open source toolkit [Bootstrap](https://getbootstrap.com/) for fontend 
- Bootstrap [Tokenfield](http://sliptree.github.io/bootstrap-tokenfield/) for fontend 
- [JQuery UI](https://jqueryui.com/) for fontend 

## Getting started
```
git clone https://github.com/sumin3/Recipe-Django-App.git
```
```
cd Recipe-Django-App
```
Install python3 with [brew](https://brew.sh/) for Mac
```
brew install python3
```
Install pipenv to create virtual environment for python. (`brew` should install `pip3` for you when you install python3.)
```
pip3 install pipenv
```
Use pipenv to install django which version is 2.1
```
pipenv install django==2.1
```
Go to your virtual environment. You need to in this virtual environment to be able to use the particular version of django that you install. 
```
pipenv shell
```
run the django server. 
```
python manage.py runserver
```
Once you press `Enter`, you should see a message like this below:
```
Performing system checks...

System check identified no issues (0 silenced).
June 27, 2019 - 18:49:40
Django version 2.1, using settings 'django_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
Copy the `url` http://127.0.0.1:8000/ above to your browser to see the Demo.

#### API
Make sure your `url` for `POST` method in file [tokenfield.js](https://github.com/sumin3/Recipe-Django-App/blob/master/static/scripts/tokenfield.js) line `32` and your browser `url` are the same. (In this case, the url should be http://127.0.0.1:8000/)

## Database
- recipeItem and ingredientItem models both defined in file [models.py](https://github.com/sumin3/Recipe-Django-App/blob/master/ingredient/models.py)


Go to your virtual environment.
```
pipenv shell
```
Inorder to interact with the models, we need to go to python shell.
```
python manage.py shell
```
Import the models 
```
>>> from ingredient.models import recipeItem
>>> from ingredient.models import ingredientItem
```
- To get all the object in the model
```
>>> recipeItem.objects.all()
```
```
>>> ingredientItem.objects.all()
```
- To get one object of the model
```
recipeItem.objects.all()[index number]

>>> recipeItem.objects.all()[0] //get the first object
```
- To get the value of the object. (`name` is one filed of the recipeItem model. You can change it to different fileds) Want to know what fileds you can use?  look at the model file [models.py](https://github.com/sumin3/Recipe-Django-App/blob/master/ingredient/models.py) 
```
>>> recipeItem.objects.all()[0].name
```
- To add new ingredient
```
>>> i1 = ingredientItem(name="potato", property="vegetable", img_url="image-url-link")
```
Save it!
```
>>> i1.save()
```
- To add new recipe (use `#` to separate the ingredients and steps)
```
>>> r1 = recipeItem(name="recipe-name", ingredients="ingredient1#ingredient2#ingredient3", directions="step1#step2#step3", img_url="image-url-link")
>>> r1.save()
```
# 🌿 Nourish by Kerry

### A Smart Recipe, Meal Planning & Nutrition Web App

Nourish by Kerry is a modern, user-friendly recipe and meal-planning web application built with Python, Django, and Bootstrap. It helps users discover recipes, build personal collections, plan meals, track ingredients, and auto-generate grocery lists.

Designed for clarity and speed, Nourish focuses on a clean responsive UI and practical features that make home cooking easier.

---

## ✨ Core Features

- Smart Recipe Search: search by ingredients, name, or category; filter by time, difficulty, diet, or cost.
- Personal Recipe Manager: add, edit, and delete recipes; upload images; add ingredients and step-by-step instructions.
- Diet Filters: vegetarian, vegan, high-protein, keto, low-cost options.
- Meal Planner: assign recipes to days and create weekly plans.
- Auto-Generated Grocery Lists: combine ingredient quantities from selected recipes and download or view on mobile.
- Responsive UI (Bootstrap): fast and mobile-friendly.

---

## 🛠️ Tech Stack

- Backend: Python 3 + Django
- Frontend: HTML, CSS, Bootstrap
- Templates: Django templates
- Database: SQLite for development (PostgreSQL recommended for production)

---

## 🚀 Quick Install (Linux / Ubuntu)

1. Clone the repo:

```bash
git clone https://github.com/yourusername/nourish-by-kerry.git
cd nourish-by-kerry
```

2. Create & activate a virtualenv:

```bash
python3 -m venv env
source env/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run migrations and start the dev server:

```bash
python manage.py migrate
python manage.py runserver
```

Open your browser at `http://127.0.0.1:8000/`.

---

## 📦 Future Roadmap

- User accounts & profiles (done)
- Enhanced meal planner & nutrition breakdown
- Shopping list export (CSV/print)
- Premium features and AI recipe suggestions

---

## 👩‍💻 Author

Kerry Koech — student & developer passionate about food tech and digital wellness.

---

## 📄 License

MIT License

---

If you want, I can also help with: creating a logo, building a landing page, adding CI, or committing and opening a PR with this README.