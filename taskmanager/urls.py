"""
URL configuration for taskmanager project.

=== LARAVEL COMPARISON ===
This file is like Laravel's routes/web.php — the MAIN route file.
- Laravel: Route::get('/dashboard', [DashboardController::class, 'index']);
- Django:  path('dashboard/', views.dashboard, name='dashboard')

Django uses include() to pull in routes from each app,
similar to Laravel's Route::group() or route files.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Built-in admin panel — visit /admin/ to see it
    # Laravel equivalent: Would be like Laravel Nova or Filament
    path('admin/', admin.site.urls),

    # Include all routes from the 'accounts' app
    # Like: Route::prefix('accounts')->group(base_path('routes/accounts.php'));
    path('accounts/', include('accounts.urls')),

    # Include all routes from the 'tasks' app (our main app)
    # The empty string '' means these routes start from root /
    path('', include('tasks.urls')),
]
