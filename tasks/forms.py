"""
Task Forms

=== LARAVEL COMPARISON ===
Django Forms = Laravel Form Request classes

In Laravel:
    php artisan make:request StoreProjectRequest
    class StoreProjectRequest extends FormRequest {
        public function rules() {
            return ['name' => 'required|max:200', 'description' => 'nullable'];
        }
    }

In Django:
    You create a Form class (or ModelForm for auto-generating from a model).
    ModelForm auto-generates form fields from the model — saves you a lot of work!
    It's like if Laravel could auto-generate validation rules from your migration.
"""

from django import forms
from .models import Project, Task, Comment


class ProjectForm(forms.ModelForm):
    """
    Form for creating/editing Projects.

    ModelForm automatically:
    - Creates form fields from the model fields
    - Handles validation
    - Saves to database

    Laravel equivalent:
        class StoreProjectRequest extends FormRequest {
            public function rules() {
                return [
                    'name' => 'required|string|max:200',
                    'description' => 'nullable|string',
                ];
            }
        }
    """
    class Meta:
        model = Project                    # Which model this form is for
        fields = ['name', 'description']   # Which fields to include (like $fillable)

        # Customize the HTML widgets (like adding CSS classes in Blade forms)
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Project Name'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your project...'
            }),
        }


class TaskForm(forms.ModelForm):
    """
    Form for creating/editing Tasks.

    Laravel equivalent:
        class StoreTaskRequest extends FormRequest {
            public function rules() {
                return [
                    'title' => 'required|string|max:200',
                    'description' => 'nullable|string',
                    'status' => 'required|in:todo,in_progress,review,done',
                    'priority' => 'required|in:low,medium,high,urgent',
                    'assigned_to' => 'nullable|exists:users,id',
                    'due_date' => 'nullable|date',
                ];
            }
        }
    """
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'priority', 'assigned_to', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
            'assigned_to': forms.Select(attrs={'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'  # HTML5 date picker
            }),
        }


class CommentForm(forms.ModelForm):
    """Form for adding comments to tasks."""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Add a comment...'
            }),
        }
