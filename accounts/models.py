"""
Accounts Models

=== LARAVEL COMPARISON ===
Django comes with a built-in User model (like Laravel's default User model).
You don't need to create one from scratch.

The built-in User model already has:
  - username, email, password, first_name, last_name
  - is_active, is_staff, is_superuser
  - date_joined, last_login

If you need extra fields, you extend it with a "Profile" model
using a OneToOneField (like Laravel's hasOne relationship).
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Extends the built-in User model with additional fields.

    Laravel equivalent:
        class Profile extends Model {
            public function user() { return $this->belongsTo(User::class); }
        }
        // And in User model:
        public function profile() { return $this->hasOne(Profile::class); }

    Usage: user.profile.bio, user.profile.role
    """
    ROLE_CHOICES = [
        ('developer', 'Developer'),
        ('manager', 'Manager'),
        ('designer', 'Designer'),
        ('qa', 'QA Engineer'),
    ]

    # OneToOneField = hasOne/belongsTo (1-to-1 relationship)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='developer')

    def __str__(self):
        return f"{self.user.username}'s profile"
