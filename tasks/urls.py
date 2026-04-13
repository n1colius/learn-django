"""
Task URL routes

=== LARAVEL COMPARISON ===
This is like Laravel's routes/web.php (but scoped to the 'tasks' app).

Laravel:
    Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
    Route::resource('projects', ProjectController::class);

Django:
    path('dashboard/', views.dashboard, name='dashboard'),
    path('projects/', views.project_list, name='project_list'),

Key differences:
- Laravel uses Route:: prefix, Django uses path()
- Laravel: {project} for URL params, Django: <int:pk>/
- Both support route naming: ->name('x') vs name='x'
- Django doesn't have Route::resource() — you define each route manually
  (or use ViewSets in Django REST Framework for APIs)
"""

from django.urls import path
from . import views

# app_name is like Laravel's Route::group(['as' => 'tasks.'], ...)
# It lets you namespace URLs to avoid naming conflicts between apps

urlpatterns = [
    # Dashboard — the home page after login
    # Like: Route::get('/dashboard', [DashboardController::class, 'index'])->name('dashboard');
    path('dashboard/', views.dashboard, name='dashboard'),

    # ── Project routes ──────────────────────────────────────
    # Like: Route::resource('projects', ProjectController::class);
    # But defined explicitly so you can see each one:

    # INDEX  — List all projects
    path('projects/', views.project_list, name='project_list'),

    # CREATE — Show form + handle submission
    path('projects/create/', views.project_create, name='project_create'),

    # SHOW   — View single project with its tasks
    # <int:pk> = Like {project} in Laravel routes (but explicitly typed as integer)
    path('projects/<int:pk>/', views.project_detail, name='project_detail'),

    # EDIT   — Edit form + handle update
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),

    # DELETE — Confirm + handle deletion
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),

    # ── Task routes (nested under project for create) ───────
    # Like: Route::resource('projects.tasks', TaskController::class);

    # CREATE task within a project
    path('projects/<int:project_pk>/tasks/create/', views.task_create, name='task_create'),

    # SHOW single task
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),

    # EDIT task
    path('tasks/<int:pk>/edit/', views.task_edit, name='task_edit'),

    # DELETE task
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),

    # Quick status update (like a PATCH route)
    path('tasks/<int:pk>/status/', views.task_update_status, name='task_update_status'),

    # ── Search ──────────────────────────────────────────────
    path('search/', views.search, name='search'),

    # Redirect root URL to dashboard
    path('', views.dashboard, name='home'),
]
