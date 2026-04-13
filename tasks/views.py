"""
Task Views (Controllers)

=== LARAVEL COMPARISON ===
Views in Django = Controllers in Laravel.
(Confusing naming! Django's "views" are Laravel's "controllers".)

     Laravel                              Django
     ------                              ------
     Controller method                    View function (or class)
     return view('tasks.index', $data)    return render(request, 'template.html', context)
     $request->validate([...])            form.is_valid()
     $task = Task::findOrFail($id)        task = get_object_or_404(Task, pk=id)
     auth()->user()                       request.user
     $this->authorize('update', $task)    @login_required decorator
     redirect()->route('tasks.index')     redirect('task_list')

Two styles of views in Django:
1. Function-Based Views (FBV) — like simple controller methods
2. Class-Based Views (CBV) — like Laravel Resource Controllers

This file uses BOTH so you can compare them!
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages  # Like Laravel's session()->flash()
from django.db.models import Q, Count  # Q = complex queries, Count = aggregate
from .models import Project, Task, Comment
from .forms import ProjectForm, TaskForm, CommentForm


# ============================================================
# DASHBOARD
# Like: class DashboardController { public function index() }
# ============================================================
@login_required  # Like Laravel's 'auth' middleware
def dashboard(request):
    """
    Main dashboard showing overview of user's projects and tasks.

    @login_required is like Laravel's:
        Route::get('/dashboard', ...)->middleware('auth');
    or in controller:
        $this->middleware('auth');
    """
    user = request.user  # Like auth()->user() or $request->user()

    # QuerySet = Like Eloquent query builder
    # user.projects.all() = Like $user->projects()->get()
    projects = user.projects.all()

    # Filter tasks assigned to this user
    # Like: Task::where('assigned_to_id', auth()->id())->where('status', '!=', 'done')->get()
    my_tasks = Task.objects.filter(assigned_to=user).exclude(status='done')

    # Aggregate counts — like Task::where(...)->count()
    task_stats = {
        'total': Task.objects.filter(project__owner=user).count(),
        'todo': Task.objects.filter(project__owner=user, status='todo').count(),
        'in_progress': Task.objects.filter(project__owner=user, status='in_progress').count(),
        'done': Task.objects.filter(project__owner=user, status='done').count(),
    }

    # context = Like compact('projects', 'my_tasks', 'task_stats') in Laravel
    context = {
        'projects': projects,
        'my_tasks': my_tasks,
        'task_stats': task_stats,
    }

    # render() = Like return view('dashboard', compact(...))
    return render(request, 'tasks/dashboard.html', context)


# ============================================================
# PROJECT CRUD — Function-Based Views (simple approach)
# Like: class ProjectController { index, create, store, show, edit, update, destroy }
# ============================================================

@login_required
def project_list(request):
    """
    List all projects for the logged-in user.
    Like: public function index() { return view('projects.index', ['projects' => auth()->user()->projects]); }
    """
    projects = request.user.projects.annotate(
        task_count=Count('tasks')  # Like withCount('tasks') in Laravel
    )
    return render(request, 'tasks/project_list.html', {'projects': projects})


@login_required
def project_create(request):
    """
    Show create form (GET) or save new project (POST).

    In Laravel, these are TWO separate methods:
        public function create() { return view('projects.create'); }       // GET
        public function store(Request $request) { Project::create(...); }  // POST

    In Django, we handle both in ONE function using request.method.
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST)  # Like $request->all()
        if form.is_valid():               # Like $request->validate([...])
            project = form.save(commit=False)  # Create but don't save yet
            project.owner = request.user        # Set the owner
            project.save()                      # Now save to database

            # Flash message — like session()->flash('success', '...')
            messages.success(request, f'Project "{project.name}" created successfully!')
            return redirect('project_detail', pk=project.pk)  # Like redirect()->route('projects.show', $project)
    else:
        form = ProjectForm()  # Empty form for GET request

    return render(request, 'tasks/project_form.html', {
        'form': form,
        'title': 'Create Project'
    })


@login_required
def project_detail(request, pk):
    """
    Show a single project with its tasks.
    Like: public function show(Project $project) { ... }

    pk = primary key (like $id in Laravel routes)
    get_object_or_404 = Like Project::findOrFail($id)
    """
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    # Get tasks with optional filtering
    # Like: $tasks = $project->tasks()->when($request->status, fn($q, $s) => $q->where('status', $s))->get()
    tasks = project.tasks.all()

    status_filter = request.GET.get('status')  # Like $request->query('status')
    if status_filter:
        tasks = tasks.filter(status=status_filter)

    priority_filter = request.GET.get('priority')
    if priority_filter:
        tasks = tasks.filter(priority=priority_filter)

    return render(request, 'tasks/project_detail.html', {
        'project': project,
        'tasks': tasks,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
    })


@login_required
def project_edit(request, pk):
    """
    Edit an existing project.
    Like: public function edit(Project $project) + public function update(Request $request, Project $project)
    """
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)  # instance= binds to existing record
        if form.is_valid():
            form.save()
            messages.success(request, f'Project "{project.name}" updated!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = ProjectForm(instance=project)  # Pre-fill form with existing data

    return render(request, 'tasks/project_form.html', {
        'form': form,
        'title': 'Edit Project',
        'project': project,
    })


@login_required
def project_delete(request, pk):
    """
    Delete a project.
    Like: public function destroy(Project $project) { $project->delete(); }
    """
    project = get_object_or_404(Project, pk=pk, owner=request.user)

    if request.method == 'POST':  # Only delete on POST (safety, like Laravel's DELETE method)
        project_name = project.name
        project.delete()  # Like $project->delete()
        messages.success(request, f'Project "{project_name}" deleted!')
        return redirect('project_list')

    return render(request, 'tasks/project_confirm_delete.html', {'project': project})


# ============================================================
# TASK CRUD
# ============================================================

@login_required
def task_create(request, project_pk):
    """Create a new task within a project."""
    project = get_object_or_404(Project, pk=project_pk, owner=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.project = project
            task.save()
            messages.success(request, f'Task "{task.title}" created!')
            return redirect('project_detail', pk=project.pk)
    else:
        form = TaskForm()

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'project': project,
        'title': 'Create Task',
    })


@login_required
def task_detail(request, pk):
    """Show task details with comments."""
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)

    # Handle comment form
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.task = task
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            return redirect('task_detail', pk=task.pk)
    else:
        comment_form = CommentForm()

    return render(request, 'tasks/task_detail.html', {
        'task': task,
        'comments': task.comments.all(),  # Like $task->comments()->get()
        'comment_form': comment_form,
    })


@login_required
def task_edit(request, pk):
    """Edit an existing task."""
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, f'Task "{task.title}" updated!')
            return redirect('task_detail', pk=task.pk)
    else:
        form = TaskForm(instance=task)

    return render(request, 'tasks/task_form.html', {
        'form': form,
        'project': task.project,
        'title': 'Edit Task',
        'task': task,
    })


@login_required
def task_delete(request, pk):
    """Delete a task."""
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)

    if request.method == 'POST':
        project_pk = task.project.pk
        task.delete()
        messages.success(request, 'Task deleted!')
        return redirect('project_detail', pk=project_pk)

    return render(request, 'tasks/task_confirm_delete.html', {'task': task})


@login_required
def task_update_status(request, pk):
    """
    Quick status update (AJAX-like or simple POST).
    Like a Laravel API endpoint: Route::patch('/tasks/{task}/status', ...)
    """
    task = get_object_or_404(Task, pk=pk, project__owner=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            task.save()
            messages.success(request, f'Task status updated to "{task.get_status_display()}"!')

    return redirect('task_detail', pk=task.pk)


# ============================================================
# SEARCH
# Like a search controller with Eloquent query scopes
# ============================================================

@login_required
def search(request):
    """
    Search across tasks and projects.

    Q objects = Like Laravel's complex where clauses:
        Task::where(function($q) use ($search) {
            $q->where('title', 'like', "%$search%")
              ->orWhere('description', 'like', "%$search%");
        })->get();
    """
    query = request.GET.get('q', '')  # Like $request->query('q', '')
    tasks = []
    projects = []

    if query:
        # Q() allows OR conditions — like Laravel's orWhere()
        tasks = Task.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query),
            project__owner=request.user
        )
        projects = Project.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            owner=request.user
        )

    return render(request, 'tasks/search.html', {
        'query': query,
        'tasks': tasks,
        'projects': projects,
    })
