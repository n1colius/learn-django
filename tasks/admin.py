"""
Admin Panel Configuration

=== LARAVEL COMPARISON ===
Django has a BUILT-IN admin panel — this is a HUGE advantage over Laravel.
Laravel needs third-party packages like Nova ($$$) or Filament.
Django gives you a full admin panel for FREE just by registering your models.

Visit /admin/ after running the server to see it.
Login with the superuser account you'll create.

This file configures HOW your models appear in the admin panel.
"""

from django.contrib import admin
from .models import Project, Task, Comment


# ============================================================
# Simple registration (minimum setup):
#     admin.site.register(Project)
# That one line gives you full CRUD in the admin panel!
#
# But we can customize it with ModelAdmin classes:
# ============================================================


class TaskInline(admin.TabularInline):
    """
    Show tasks INSIDE the project admin page (inline editing).
    Like being able to edit related models on the same page.
    No Laravel equivalent — this is unique to Django admin.
    """
    model = Task
    extra = 1  # Show 1 empty row for adding new tasks
    fields = ['title', 'status', 'priority', 'assigned_to', 'due_date']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Customize how Project appears in the admin panel.
    """
    list_display = ['name', 'owner', 'created_at', 'task_count']
    # list_display = columns shown in the list view

    list_filter = ['created_at', 'owner']
    # list_filter = sidebar filters (like search filters)

    search_fields = ['name', 'description']
    # search_fields = which fields are searchable

    inlines = [TaskInline]
    # Show tasks inline when editing a project

    def task_count(self, obj):
        """Custom column — shows number of tasks in each project."""
        return obj.tasks.count()
    task_count.short_description = 'Tasks'


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'status', 'priority', 'assigned_to', 'due_date']
    list_filter = ['status', 'priority', 'project']
    search_fields = ['title', 'description']
    list_editable = ['status', 'priority']  # Edit these directly from the list view!
    date_hierarchy = 'created_at'  # Date-based navigation at the top


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'author', 'created_at']
    list_filter = ['created_at', 'author']
