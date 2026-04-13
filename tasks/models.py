"""
Task Management Models

=== LARAVEL COMPARISON ===
Models in Django = Eloquent Models + Migrations combined in ONE file.

In Laravel:
  - You create a migration: php artisan make:migration create_projects_table
  - You create a model:     php artisan make:model Project
  - They are separate files.

In Django:
  - You define the model here, and Django auto-generates migrations from it.
  - Command: python manage.py makemigrations  (like: php artisan make:migration)
  - Command: python manage.py migrate         (like: php artisan migrate)

=== FIELD TYPE MAPPING (Laravel -> Django) ===
  Laravel                    Django
  -------                    ------
  $table->string('name')     models.CharField(max_length=200)
  $table->text('desc')       models.TextField()
  $table->integer('num')     models.IntegerField()
  $table->boolean('active')  models.BooleanField()
  $table->date('due')        models.DateField()
  $table->dateTime('at')     models.DateTimeField()
  $table->foreignId('x')     models.ForeignKey(Model, on_delete=...)
  $table->timestamps()       auto_now_add=True / auto_now=True
"""

from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    """
    A project that contains multiple tasks.

    Laravel equivalent:
        class Project extends Model {
            protected $fillable = ['name', 'description', 'owner_id'];
            public function owner() { return $this->belongsTo(User::class); }
            public function tasks() { return $this->hasMany(Task::class); }
        }
    """
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)  # blank=True = optional in forms

    # ForeignKey = belongsTo relationship
    # on_delete=models.CASCADE = like Laravel's ->cascadeOnDelete()
    # related_name='projects' = lets you do: user.projects.all() (like $user->projects)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        """Like Laravel's __toString() — controls how model displays as string."""
        return self.name


class Task(models.Model):
    """
    A task that belongs to a project.

    Laravel equivalent:
        class Task extends Model {
            protected $fillable = ['title', 'description', 'status', 'priority', ...];
            public function project() { return $this->belongsTo(Project::class); }
            public function assignedTo() { return $this->belongsTo(User::class); }
        }
    """

    # Choices = Like Laravel Enums or Rule::in() validation
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('review', 'In Review'),
        ('done', 'Done'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='todo')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,  # Don't delete task if user is deleted
        null=True,
        blank=True,
        related_name='assigned_tasks'
    )

    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-priority', 'due_date']

    def __str__(self):
        return self.title

    @property
    def is_overdue(self):
        """
        Computed property — like Laravel Accessor:
            public function getIsOverdueAttribute() { ... }
        Usage in template: {{ task.is_overdue }}
        """
        from django.utils import timezone
        if self.due_date and self.status != 'done':
            return self.due_date < timezone.now().date()
        return False


class Comment(models.Model):
    """Comments on tasks — like Laravel's hasMany relationship."""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.task.title}"
