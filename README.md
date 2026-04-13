# Django Task Manager - Learning Project

A complete **Company Task Management System** built with Django, designed specifically for **PHP Laravel developers** who want to learn Django quickly through hands-on code.

Every file in this project is heavily commented with Laravel equivalents so you can map your existing knowledge directly to Django concepts.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Project Structure](#project-structure)
3. [Laravel vs Django - The Big Picture](#laravel-vs-django---the-big-picture)
4. [Command Cheat Sheet](#command-cheat-sheet)
5. [Concept-by-Concept Guide](#concept-by-concept-guide)
   - [Settings (config)](#1-settings--configuration)
   - [Models (Eloquent)](#2-models--database)
   - [Migrations](#3-migrations)
   - [URLs/Routing](#4-urls--routing)
   - [Views/Controllers](#5-views--controllers)
   - [Templates (Blade)](#6-templates--blade-equivalent)
   - [Forms (Validation)](#7-forms--validation)
   - [Authentication](#8-authentication)
   - [Admin Panel](#9-admin-panel)
   - [Static Files](#10-static-files)
   - [ORM Queries](#11-orm-queries--eloquent-equivalent)
6. [Features Included](#features-included)
7. [Exercises to Try](#exercises-to-try)
8. [Common Gotchas](#common-gotchas)
9. [Where to Go Next](#where-to-go-next)

---

## Quick Start

```bash
# 1. Install Django (if not already installed)
pip install django

# 2. Run database migrations (like: php artisan migrate)
python manage.py migrate

# 3. Create a superuser for the admin panel (like: php artisan make:admin)
python manage.py createsuperuser

# 4. Start the development server (like: php artisan serve)
python manage.py runserver

# 5. Open your browser
#    Main app:    http://127.0.0.1:8000/
#    Admin panel: http://127.0.0.1:8000/admin/
```

### Pre-loaded Demo Account

A demo account is already set up with sample data:

- **Username:** `admin`
- **Password:** `admin123`
- Includes 3 projects and 10 tasks so you can explore immediately.

---

## Project Structure

```
learn-django/
│
├── manage.py                    # Like Laravel's "artisan" CLI tool
├── db.sqlite3                   # SQLite database file
│
├── taskmanager/                 # PROJECT CONFIG (like Laravel's config/ + routes/)
│   ├── __init__.py              # Makes this a Python package (ignore for now)
│   ├── settings.py              # Like .env + config/app.php + config/database.php
│   ├── urls.py                  # Like routes/web.php (the MAIN route file)
│   ├── wsgi.py                  # Server entry point (like public/index.php)
│   └── asgi.py                  # Async server entry point
│
├── tasks/                       # APP: Task management (like a Laravel module)
│   ├── __init__.py
│   ├── models.py                # Eloquent Models + Migration definitions
│   ├── views.py                 # Controllers (yes, Django calls them "views")
│   ├── urls.py                  # Route definitions for this app
│   ├── forms.py                 # Form Request classes (validation)
│   ├── admin.py                 # Admin panel configuration
│   ├── apps.py                  # App configuration (auto-generated)
│   └── migrations/              # Migration files (auto-generated)
│       └── 0001_initial.py
│
├── accounts/                    # APP: User auth & profiles
│   ├── models.py                # Profile model (extends User)
│   ├── views.py                 # Register, profile controllers
│   ├── urls.py                  # Auth routes
│   ├── forms.py                 # Registration & profile forms
│   ├── admin.py                 # Admin config for profiles
│   └── migrations/
│
├── templates/                   # Like resources/views/ in Laravel
│   ├── base.html                # Like layouts/app.blade.php
│   ├── accounts/
│   │   ├── login.html           # Like auth/login.blade.php
│   │   ├── register.html        # Like auth/register.blade.php
│   │   └── profile.html
│   └── tasks/
│       ├── dashboard.html
│       ├── project_list.html
│       ├── project_detail.html
│       ├── project_form.html    # Used for both create AND edit
│       ├── project_confirm_delete.html
│       ├── task_detail.html
│       ├── task_form.html
│       ├── task_confirm_delete.html
│       └── search.html
│
└── static/                      # Like public/ in Laravel
    └── css/
        └── style.css
```

### Key Naming Difference

| Concept | Laravel Term | Django Term |
|---------|-------------|-------------|
| Business logic handler | **Controller** | **View** |
| HTML template | **View** (Blade) | **Template** |

This is the #1 source of confusion. In Django, what Laravel calls a "controller" is called a "view", and what Laravel calls a "view" is called a "template".

---

## Laravel vs Django - The Big Picture

| Aspect | Laravel | Django |
|--------|---------|--------|
| Language | PHP | Python |
| ORM | Eloquent | Django ORM |
| Template Engine | Blade | Django Template Language (DTL) |
| CLI Tool | `php artisan` | `python manage.py` |
| Routing | `routes/web.php` | `urls.py` (in each app) |
| Controllers | `app/Http/Controllers/` | `views.py` (in each app) |
| Models | `app/Models/` | `models.py` (in each app) |
| Migrations | Separate files from models | Auto-generated FROM models |
| Validation | Form Requests / `$request->validate()` | Form classes |
| Auth | Built-in + Breeze/Jetstream | Built-in (simpler) |
| Admin Panel | Nova ($$$) / Filament | **Built-in & FREE** |
| Package Structure | One app, many controllers | Multiple "apps" per project |

### The "App" Concept

In Laravel, you have ONE application with controllers, models, etc. inside it.

In Django, a project contains multiple **apps**. Each app is a self-contained module:

```
Laravel:  ONE project -> many controllers, models
Django:   ONE project -> many APPS -> each app has its own models, views, urls
```

Think of Django apps like Laravel packages that you build yourself. In this project:
- `tasks` app = handles projects, tasks, comments
- `accounts` app = handles user registration, profiles

---

## Command Cheat Sheet

| What you want to do | Laravel | Django |
|---------------------|---------|--------|
| Start dev server | `php artisan serve` | `python manage.py runserver` |
| Interactive console | `php artisan tinker` | `python manage.py shell` |
| Create migration | `php artisan make:migration create_x_table` | `python manage.py makemigrations` |
| Run migrations | `php artisan migrate` | `python manage.py migrate` |
| Rollback migration | `php artisan migrate:rollback` | `python manage.py migrate app_name 0001` |
| Create superuser | *(manual or seeder)* | `python manage.py createsuperuser` |
| Create new app | *(not applicable)* | `python manage.py startapp app_name` |
| Run tests | `php artisan test` | `python manage.py test` |
| Collect static files | `npm run build` | `python manage.py collectstatic` |
| Show all URLs | `php artisan route:list` | `python manage.py show_urls` (needs django-extensions) |
| Check for issues | *(no equivalent)* | `python manage.py check` |
| Database shell | `php artisan db` | `python manage.py dbshell` |

### Quick shell examples (like Tinker)

```bash
python manage.py shell
```

```python
# Inside the shell:
from tasks.models import Project, Task
from django.contrib.auth.models import User

# Get all projects (like Project::all())
Project.objects.all()

# Find by ID (like Project::find(1))
Project.objects.get(pk=1)

# Filter (like Project::where('name', 'like', '%web%')->get())
Project.objects.filter(name__icontains='web')

# Create (like Project::create([...]))
user = User.objects.first()
Project.objects.create(name='Test', owner=user)

# Count (like Project::count())
Task.objects.count()
```

---

## Concept-by-Concept Guide

### 1. Settings / Configuration

**File:** `taskmanager/settings.py`

In Laravel, configuration is split across `.env` and multiple files in `config/`. In Django, it's all in one file: `settings.py`.

| Laravel | Django `settings.py` |
|---------|---------------------|
| `.env` → `APP_KEY` | `SECRET_KEY` |
| `.env` → `APP_DEBUG=true` | `DEBUG = True` |
| `config/app.php` → `'providers'` | `INSTALLED_APPS` |
| `config/database.php` | `DATABASES` |
| `app/Http/Kernel.php` → `$middleware` | `MIDDLEWARE` |
| `config/view.php` → `'paths'` | `TEMPLATES` → `'DIRS'` |
| `config/auth.php` | Various `LOGIN_URL`, `LOGIN_REDIRECT_URL` settings |

**Key thing to remember:** When you create a new app, you MUST add it to `INSTALLED_APPS` or Django won't know about it. It's like adding a service provider in Laravel.

---

### 2. Models / Database

**Files:** `tasks/models.py`, `accounts/models.py`

Django models combine what Laravel keeps separate: the Eloquent model AND the migration schema.

```python
# DJANGO - model AND schema in ONE file
class Task(models.Model):
    title = models.CharField(max_length=200)      # $table->string('title', 200)
    description = models.TextField(blank=True)     # $table->text('description')->nullable()
    project = models.ForeignKey(Project, ...)      # $table->foreignId('project_id')
    created_at = models.DateTimeField(auto_now_add=True)  # $table->timestamps()
```

```php
// LARAVEL - schema in migration, model separate
// Migration:
Schema::create('tasks', function (Blueprint $table) {
    $table->string('title', 200);
    $table->text('description')->nullable();
    $table->foreignId('project_id')->constrained()->cascadeOnDelete();
    $table->timestamps();
});

// Model:
class Task extends Model {
    protected $fillable = ['title', 'description', 'project_id'];
    public function project() { return $this->belongsTo(Project::class); }
}
```

#### Field Type Mapping

| Laravel Migration | Django Model Field |
|---|---|
| `$table->string('name', 200)` | `models.CharField(max_length=200)` |
| `$table->text('body')` | `models.TextField()` |
| `$table->integer('count')` | `models.IntegerField()` |
| `$table->boolean('active')` | `models.BooleanField()` |
| `$table->date('due')` | `models.DateField()` |
| `$table->dateTime('start')` | `models.DateTimeField()` |
| `$table->foreignId('user_id')` | `models.ForeignKey(User, on_delete=...)` |
| `$table->timestamps()` | `auto_now_add=True` + `auto_now=True` |
| `->nullable()` | `null=True, blank=True` |
| `->default('value')` | `default='value'` |

#### Relationship Mapping

| Laravel | Django |
|---------|--------|
| `$this->belongsTo(User::class)` | `models.ForeignKey(User, ...)` |
| `$this->hasMany(Task::class)` | *(automatic via `related_name`)* |
| `$this->hasOne(Profile::class)` | `models.OneToOneField(User, ...)` |
| `$this->belongsToMany(Tag::class)` | `models.ManyToManyField(Tag)` |
| `$user->tasks` | `user.tasks.all()` (using `related_name='tasks'`) |

#### `null=True` vs `blank=True`

This trips up everyone:
- `null=True` = database allows NULL (like `->nullable()` in Laravel)
- `blank=True` = form allows empty (validation level)
- For optional text fields: use `blank=True` only (Django stores empty string, not NULL)
- For optional dates/numbers/FKs: use BOTH `null=True, blank=True`

---

### 3. Migrations

In Laravel, you write migrations manually. In Django, migrations are **auto-generated** from your model changes.

```bash
# Workflow:
# 1. Edit models.py (add/change/remove fields)
# 2. Generate migration (Django detects changes automatically!)
python manage.py makemigrations

# 3. Apply migration to database
python manage.py migrate
```

This is one of Django's biggest advantages: you never write migration files by hand. Change the model, run `makemigrations`, and Django figures out the SQL.

```bash
# See the SQL a migration would run (like --pretend in Laravel)
python manage.py sqlmigrate tasks 0001

# See migration status
python manage.py showmigrations
```

---

### 4. URLs / Routing

**Files:** `taskmanager/urls.py`, `tasks/urls.py`, `accounts/urls.py`

```python
# DJANGO
from django.urls import path
from . import views

urlpatterns = [
    path('projects/', views.project_list, name='project_list'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),
    path('projects/create/', views.project_create, name='project_create'),
]
```

```php
// LARAVEL equivalent
Route::get('/projects', [ProjectController::class, 'index'])->name('project_list');
Route::get('/projects/{id}', [ProjectController::class, 'show'])->name('project_detail');
Route::get('/projects/create', [ProjectController::class, 'create'])->name('project_create');
```

#### Key Differences

| Feature | Laravel | Django |
|---------|---------|--------|
| URL parameters | `{id}` | `<int:pk>` |
| Route naming | `->name('x')` | `name='x'` |
| Route groups | `Route::group(...)` | `include('app.urls')` |
| Generating URLs | `route('project_detail', $id)` | `{% url 'project_detail' pk=id %}` |
| HTTP methods | `Route::get/post/put/delete` | All handled in ONE `path()`, checked in view |
| Resource routes | `Route::resource(...)` | No equivalent (define each route) |

#### URL Parameters

```python
# Django                              # Laravel
path('tasks/<int:pk>/', ...)          # Route::get('/tasks/{id}', ...)
path('users/<str:username>/', ...)    # Route::get('/users/{username}', ...)
path('page/<int:page>/', ...)         # Route::get('/page/{page}', ...)
```

Available converters: `int`, `str`, `slug`, `uuid`, `path`

---

### 5. Views / Controllers

**Files:** `tasks/views.py`, `accounts/views.py`

Django has two styles of views:

#### Function-Based Views (most common for learning)

```python
# DJANGO - Function-Based View
@login_required  # Like ->middleware('auth')
def project_list(request):                        # $request is passed automatically
    projects = request.user.projects.all()         # auth()->user()->projects
    return render(request, 'tasks/project_list.html', {
        'projects': projects,                      # compact('projects')
    })
```

```php
// LARAVEL equivalent
public function index(Request $request) {
    $projects = auth()->user()->projects;
    return view('tasks.project_list', compact('projects'));
}
```

#### Handling GET and POST in one view

In Laravel, you have separate `create()` and `store()` methods. In Django, you typically handle both in one function:

```python
# DJANGO - Create view handles BOTH showing form (GET) and saving (POST)
@login_required
def project_create(request):
    if request.method == 'POST':          # store() in Laravel
        form = ProjectForm(request.POST)  # Like $request->all()
        if form.is_valid():               # Like $request->validate([...])
            project = form.save(commit=False)
            project.owner = request.user
            project.save()
            messages.success(request, 'Created!')  # session()->flash('success', '...')
            return redirect('project_list')         # redirect()->route('project_list')
    else:                                 # create() in Laravel
        form = ProjectForm()

    return render(request, 'tasks/project_form.html', {'form': form})
```

#### Common View Patterns

| Laravel | Django |
|---------|--------|
| `$request->user()` or `auth()->user()` | `request.user` |
| `$request->input('name')` | `request.POST.get('name')` |
| `$request->query('page')` | `request.GET.get('page')` |
| `$request->method()` | `request.method` |
| `abort(404)` | `raise Http404` or `get_object_or_404(...)` |
| `Project::findOrFail($id)` | `get_object_or_404(Project, pk=id)` |
| `return redirect()->route('x')` | `return redirect('x')` |
| `session()->flash('success', '...')` | `messages.success(request, '...')` |

---

### 6. Templates / Blade Equivalent

**Files:** `templates/` directory

Django Template Language (DTL) is simpler than Blade but covers all the basics.

#### Syntax Comparison

| Blade (Laravel) | Django Template |
|-----------------|-----------------|
| `@extends('layouts.app')` | `{% extends 'base.html' %}` |
| `@section('content')` | `{% block content %}` |
| `@endsection` | `{% endblock %}` |
| `@yield('content')` | `{% block content %}{% endblock %}` |
| `@include('partials.nav')` | `{% include 'partials/nav.html' %}` |
| `{{ $variable }}` | `{{ variable }}` (no $ sign!) |
| `{!! $rawHtml !!}` | `{{ html\|safe }}` |
| `@if($condition)` | `{% if condition %}` |
| `@elseif($x)` | `{% elif x %}` |
| `@else` | `{% else %}` |
| `@endif` | `{% endif %}` |
| `@foreach($items as $item)` | `{% for item in items %}` |
| `@endforeach` | `{% endfor %}` |
| `@empty` | `{% empty %}` (inside for loop) |
| `@csrf` | `{% csrf_token %}` |
| `{{ route('name', $id) }}` | `{% url 'name' pk=id %}` |
| `{{ asset('css/app.css') }}` | `{% static 'css/style.css' %}` |
| `@auth` | `{% if user.is_authenticated %}` |
| `@guest` | `{% if not user.is_authenticated %}` |

#### Template Filters (like PHP/Blade helpers)

Filters use the pipe `|` character:

```
{{ task.created_at|date:"M d, Y" }}       Like Carbon's format('M d, Y')
{{ text|truncatewords:20 }}                Like Str::words($text, 20)
{{ task.created_at|timesince }}            Like Carbon's diffForHumans()
{{ items|length }}                         Like count($items)
{{ name|default:"Unknown" }}              Like $name ?? 'Unknown'
{{ text|linebreaks }}                      Like nl2br()
{{ count|pluralize }}                      Adds "s" if count != 1
{{ text|upper }}                           Like strtoupper()
{{ text|lower }}                           Like strtolower()
{{ html_content|safe }}                    Like {!! !!} in Blade (trust raw HTML)
```

#### for Loop Special Variables

Django's `{% for %}` loop gives you a `forloop` variable (like `$loop` in Blade):

```
{% for item in items %}
    {{ forloop.counter }}      Like $loop->iteration (1-based)
    {{ forloop.counter0 }}     Like $loop->index (0-based)
    {{ forloop.first }}        Like $loop->first
    {{ forloop.last }}         Like $loop->last
{% empty %}
    No items found.            Like @forelse ... @empty
{% endfor %}
```

---

### 7. Forms / Validation

**Files:** `tasks/forms.py`, `accounts/forms.py`

Django Forms = Laravel Form Requests + validation logic combined.

```python
# DJANGO - ModelForm (auto-generates fields from model)
class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']   # Like $fillable in Laravel
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }
```

```php
// LARAVEL equivalent
class StoreProjectRequest extends FormRequest {
    public function rules() {
        return [
            'name' => 'required|string|max:200',
            'description' => 'nullable|string',
        ];
    }
}
```

#### How validation works

```python
# In the view:
form = ProjectForm(request.POST)  # Bind submitted data to form
if form.is_valid():               # Runs all validation
    form.save()                   # Save to database
# If invalid, form.errors contains all error messages
```

In templates, you can render forms automatically or field-by-field:

```html
<!-- Render entire form at once (quick & dirty) -->
{{ form.as_p }}

<!-- Or render field by field (more control) -->
{% for field in form %}
    <label>{{ field.label }}</label>
    {{ field }}
    {% if field.errors %}
        <span class="error">{{ field.errors.0 }}</span>
    {% endif %}
{% endfor %}
```

---

### 8. Authentication

Django has built-in authentication that's simpler than Laravel's.

| Feature | Laravel | Django |
|---------|---------|--------|
| Login view | Write your own or use Breeze | `LoginView` (built-in, just provide template) |
| Logout | Write your own or use Breeze | `LogoutView` (built-in) |
| Registration | Write your own or use Breeze | Write your own (simple) |
| Check if logged in | `@auth` / `auth()->check()` | `request.user.is_authenticated` |
| Get current user | `auth()->user()` | `request.user` |
| Require login (route) | `->middleware('auth')` | `@login_required` decorator |
| Login redirect | `config/auth.php` | `LOGIN_REDIRECT_URL` in settings |
| Password hashing | `Hash::make()` | Automatic in `UserCreationForm` |

#### The `@login_required` Decorator

```python
from django.contrib.auth.decorators import login_required

@login_required  # If not logged in -> redirect to LOGIN_URL
def dashboard(request):
    # request.user is GUARANTEED to be authenticated here
    ...
```

This is like adding `->middleware('auth')` to a Laravel route.

---

### 9. Admin Panel

**Files:** `tasks/admin.py`, `accounts/admin.py`

This is Django's **killer feature**. You get a full admin CRUD panel for FREE.

Visit `http://127.0.0.1:8000/admin/` and login with your superuser account.

```python
# Minimum setup - just ONE line gives you full CRUD:
admin.site.register(Project)

# Customized setup (what we use in this project):
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority']     # Columns to show
    list_filter = ['status', 'priority']                # Sidebar filters
    search_fields = ['title', 'description']            # Search bar
    list_editable = ['status', 'priority']              # Edit from list view!
```

Laravel equivalent would cost you money (Nova) or require installing a package (Filament). Django gives you this out of the box.

---

### 10. Static Files

**Directory:** `static/css/style.css`

```python
# In settings.py:
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

```html
<!-- In templates: -->
{% load static %}  <!-- Must be at top of template -->
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

| Laravel | Django |
|---------|--------|
| `asset('css/app.css')` | `{% static 'css/style.css' %}` |
| `public/` directory | `static/` directory |
| Vite / Mix for bundling | `collectstatic` for production |

---

### 11. ORM Queries / Eloquent Equivalent

Django's ORM is very similar to Eloquent. Here's a side-by-side comparison:

#### Basic CRUD

```python
# CREATE
# Laravel: Project::create(['name' => 'New', 'owner_id' => 1])
Project.objects.create(name='New', owner=user)

# READ (all)
# Laravel: Project::all()
Project.objects.all()

# READ (find by ID)
# Laravel: Project::find(1) / Project::findOrFail(1)
Project.objects.get(pk=1)

# UPDATE
# Laravel: $project->update(['name' => 'Updated'])
project.name = 'Updated'
project.save()

# DELETE
# Laravel: $project->delete()
project.delete()
```

#### Filtering (WHERE clauses)

```python
# Laravel: Task::where('status', 'done')->get()
Task.objects.filter(status='done')

# Laravel: Task::where('priority', '!=', 'low')->get()
Task.objects.exclude(priority='low')

# Laravel: Task::where('title', 'like', '%search%')->get()
Task.objects.filter(title__icontains='search')

# Laravel: Task::where('due_date', '<', now())->get()
from django.utils import timezone
Task.objects.filter(due_date__lt=timezone.now())

# Laravel: Task::where('status', 'done')->where('priority', 'high')->get()
Task.objects.filter(status='done', priority='high')

# Laravel: Task::where('status', 'done')->orWhere('priority', 'urgent')->get()
from django.db.models import Q
Task.objects.filter(Q(status='done') | Q(priority='urgent'))
```

#### Lookup Suffixes (Django's secret weapon)

Django uses double-underscore suffixes for comparisons:

```python
field__exact = 'x'        # WHERE field = 'x'     (default)
field__iexact = 'x'       # WHERE LOWER(field) = 'x' (case-insensitive)
field__contains = 'x'     # WHERE field LIKE '%x%'
field__icontains = 'x'    # Case-insensitive contains
field__startswith = 'x'   # WHERE field LIKE 'x%'
field__endswith = 'x'     # WHERE field LIKE '%x'
field__gt = 5             # WHERE field > 5
field__gte = 5            # WHERE field >= 5
field__lt = 5             # WHERE field < 5
field__lte = 5            # WHERE field <= 5
field__in = [1, 2, 3]     # WHERE field IN (1, 2, 3)
field__isnull = True       # WHERE field IS NULL
field__range = (1, 10)    # WHERE field BETWEEN 1 AND 10
```

#### Relationships

```python
# Laravel: $user->projects (hasMany)
user.projects.all()                # Uses related_name='projects'

# Laravel: $task->project (belongsTo)
task.project                       # Returns the related Project object
task.project.name                  # Access fields on related model

# Laravel: $project->tasks()->where('status', 'done')->count()
project.tasks.filter(status='done').count()

# Laravel: Project::withCount('tasks')->get()
from django.db.models import Count
Project.objects.annotate(task_count=Count('tasks'))

# Laravel: Task::with('project')->get()  (eager loading)
Task.objects.select_related('project')   # For ForeignKey/OneToOne
Task.objects.prefetch_related('comments') # For reverse FK/M2M
```

#### Aggregation

```python
from django.db.models import Count, Avg, Max, Min, Sum

# Laravel: Task::count()
Task.objects.count()

# Laravel: Task::where('project_id', 1)->avg('priority')
Task.objects.filter(project_id=1).aggregate(Avg('priority'))
```

#### Ordering

```python
# Laravel: Task::orderBy('created_at', 'desc')->get()
Task.objects.order_by('-created_at')    # Prefix "-" means DESC

# Laravel: Task::latest()->get()
Task.objects.order_by('-created_at')

# Laravel: Task::oldest()->first()
Task.objects.order_by('created_at').first()
```

#### Slicing (LIMIT / OFFSET)

```python
# Laravel: Task::take(5)->get()
Task.objects.all()[:5]                  # Python slice = LIMIT 5

# Laravel: Task::skip(10)->take(5)->get()
Task.objects.all()[10:15]               # OFFSET 10 LIMIT 5

# Laravel: Task::first()
Task.objects.first()

# Laravel: Task::latest()->first()
Task.objects.order_by('-created_at').first()
```

---

## Features Included

This project covers the most common patterns you'll need in real-world Django:

- **User Authentication** - Register, login, logout, profile editing
- **CRUD Operations** - Full create/read/update/delete for Projects and Tasks
- **Relationships** - ForeignKey (belongsTo), reverse relations (hasMany), OneToOne
- **Form Handling** - ModelForms with validation, CSRF protection
- **Search** - Full-text search with Q objects (complex queries)
- **Filtering** - Query parameter-based filtering on list views
- **Flash Messages** - Success/error notifications
- **Admin Panel** - Full admin CRUD with customization
- **Template Inheritance** - Base layout with blocks (like Blade layouts)
- **Static Files** - CSS serving
- **Authorization** - Login-required views, owner-based access control

---

## Exercises to Try

Once you've explored the code, try these exercises to deepen your understanding:

### Beginner

1. **Add a new field** - Add a `completed_at` DateTimeField to the Task model. Run `makemigrations` and `migrate`.
2. **Change the admin** - Add `completed_at` to the Task admin's `list_display`.
3. **New template filter** - Display task descriptions with `|truncatewords:10` on the project detail page.

### Intermediate

4. **Add task labels/tags** - Create a `Label` model with a ManyToManyField on Task (like Laravel's `belongsToMany`).
5. **Add pagination** - Use Django's `Paginator` class to paginate the project list (like Laravel's `->paginate(10)`).
6. **Add user assignment dropdown** - Make the "assigned_to" field only show team members.
7. **Add a task count badge** - Show the number of tasks next to each project name in the navbar.

### Advanced

8. **Build a REST API** - Install `djangorestframework` and create API endpoints for tasks (like Laravel's API resources).
9. **Add file attachments** - Use `FileField` to allow file uploads on tasks.
10. **Add email notifications** - Send an email when a task is assigned to someone.
11. **Deploy to production** - Try deploying to Railway, Render, or PythonAnywhere.

---

## Common Gotchas

### 1. "View" means different things
- Laravel: View = HTML template (Blade file)
- Django: View = Controller logic (the function/class that handles the request)

### 2. Forgetting `{% csrf_token %}`
Every POST form needs `{% csrf_token %}`. Without it, you'll get a 403 error. This is like Laravel's `@csrf` but Django is stricter about it.

### 3. Forgetting to add app to `INSTALLED_APPS`
When you create a new app with `startapp`, you MUST add it to `INSTALLED_APPS` in `settings.py`. Otherwise Django won't detect your models or migrations.

### 4. `null=True` vs `blank=True`
- `null=True` = database allows NULL
- `blank=True` = form validation allows empty
- For strings: usually just `blank=True` (Django uses empty string, not NULL)
- For dates/numbers/FK: use both `null=True, blank=True`

### 5. No `$` in template variables
- Laravel: `{{ $project->name }}`
- Django: `{{ project.name }}` (no `$`, use dot not `->`)

### 6. Dot notation for everything in templates
- Object attribute: `{{ project.name }}` (like `$project->name`)
- Dictionary key: `{{ dict.key }}` (like `$dict['key']`)
- Method call: `{{ task.get_status_display }}` (no parentheses!)
- List index: `{{ list.0 }}` (like `$list[0]`)

### 7. Reverse relationships
When you define `ForeignKey(Project, related_name='tasks')` on Task, you can access tasks from the project using `project.tasks.all()`. If you forget `related_name`, Django auto-generates one as `project.task_set.all()`.

### 8. `objects` is the default manager
In Laravel, you call static methods on the model: `Task::where(...)`.
In Django, you go through `objects`: `Task.objects.filter(...)`.
`objects` is like Eloquent's query builder.

---

## Where to Go Next

1. **Django REST Framework** - Build APIs (like Laravel's API Resources)
   ```bash
   pip install djangorestframework
   ```

2. **Django Debug Toolbar** - Like Laravel Debugbar
   ```bash
   pip install django-debug-toolbar
   ```

3. **Celery** - Background jobs (like Laravel Queues)
   ```bash
   pip install celery
   ```

4. **Django Channels** - WebSockets (like Laravel Broadcasting)

5. **Official Django Tutorial** - https://docs.djangoproject.com/en/stable/intro/tutorial01/

6. **Django Documentation** - https://docs.djangoproject.com/en/stable/

---

*This project was built as a learning tool. Every file contains detailed comments comparing Django patterns to their Laravel equivalents. Open any `.py` file and read the comments to understand how things work!*
