"""
Account Views (Controllers)

=== LARAVEL COMPARISON ===
These handle user registration, login, logout, and profile management.
Like Laravel's Auth controllers (RegisterController, LoginController, etc.)

Django provides built-in views for login/logout — you don't need to write them!
Like Laravel's Auth::routes() which auto-generates login/register routes.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, ProfileForm, UserUpdateForm
from .models import Profile


def register(request):
    """
    User registration.

    Laravel equivalent:
        class RegisterController extends Controller {
            protected function create(array $data) {
                return User::create([
                    'name' => $data['name'],
                    'email' => $data['email'],
                    'password' => Hash::make($data['password']),
                ]);
            }
        }

    Django's UserCreationForm handles password hashing automatically.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Creates user with hashed password

            # Create a Profile for the new user
            Profile.objects.create(user=user)

            # Auto-login after registration
            # Like Auth::login($user) in Laravel
            login(request, user)

            messages.success(request, f'Welcome, {user.username}! Your account has been created.')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


@login_required
def profile(request):
    """
    View and edit user profile.
    Like: public function edit() in ProfileController
    """
    # Create profile if it doesn't exist (safety check)
    Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })
