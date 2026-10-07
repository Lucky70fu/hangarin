from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Exists, OuterRef, Prefetch, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TaskForm, SubTaskForm, NoteForm, PriorityForm, CategoryForm
from .models import Category, Priority, SubTask, Task, Note


@login_required
def dashboard(request):
    tasks = Task.objects.select_related(
        "category",
        "priority",
    ).prefetch_related(
        Prefetch(
            "subtask_set",
            queryset=SubTask.objects.order_by("created_at"),
            to_attr="dashboard_subtasks",
        ),
        Prefetch(
            "note_set",
            queryset=Note.objects.order_by("-created_at"),
            to_attr="dashboard_notes",
        ),
    )

    search_query = request.GET.get("q", "").strip()
    status_filter = request.GET.get("status", "").strip()
    category_filter = request.GET.get("category", "").strip()
    priority_filter = request.GET.get("priority", "").strip()

    sort = request.GET.get("sort", "created")

    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    if status_filter:
        tasks = tasks.filter(status=status_filter)

    if category_filter:
        tasks = tasks.filter(category_id=category_filter)

    if priority_filter:
        tasks = tasks.filter(priority_id=priority_filter)

    sort_options = {
        "created": "-created_at",
        "created_oldest": "created_at",
        "deadline": "deadline",
        "deadline_desc": "-deadline",
    }

    tasks = tasks.order_by(
        sort_options.get(sort, "-created_at")
    )

    paginator = Paginator(tasks, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "tasks": page_obj.object_list,
        "total_tasks": Task.objects.count(),
        "pending_tasks": Task.objects.filter(
            status="Pending"
        ).count(),
        "in_progress_tasks": Task.objects.filter(
            status="In Progress"
        ).count(),
        "completed_tasks": Task.objects.filter(
            status="Completed"
        ).count(),
        "now": timezone.now(),
        "search_query": search_query,
        "status_filter": status_filter,
        "category_filter": category_filter,
        "priority_filter": priority_filter,
        "sort": sort,
        "categories": Category.objects.all().order_by("name"),
        "priorities": Priority.objects.all().order_by("name"),
    }

    return render(
        request,
        "taskmanager/dashboard.html",
        context,
    )


@login_required
def task_create(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = TaskForm()

    return render(
        request,
        "taskmanager/task_form.html",
        {
            "form": form,
            "page_title": "Add Task",
            "button_text": "Create Task",
        },
    )


@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "taskmanager/task_form.html",
        {
            "form": form,
            "page_title": "Edit Task",
            "button_text": "Save Changes",
        },
    )


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task.delete()
        return redirect("dashboard")

    return render(
        request,
        "taskmanager/task_confirm_delete.html",
        {
            "task": task,
        },
    )

@login_required
def subtask_create(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if task.subtask_set.count() >= 5:
        return redirect("dashboard")

    if request.method == "POST":
        form = SubTaskForm(request.POST)

        if form.is_valid():
            subtask = form.save(commit=False)
            subtask.parent_task = task
            subtask.save()
            return redirect("dashboard")

    else:
        form = SubTaskForm()

    return render(
        request,
        "taskmanager/subtask_form.html",
        {
            "form": form,
            "task": task,
            "page_title": "Add SubTask",
            "button_text": "Create SubTask",
        },
    )


@login_required
def subtask_edit(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    if request.method == "POST":
        form = SubTaskForm(request.POST, instance=subtask)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = SubTaskForm(instance=subtask)

    return render(
        request,
        "taskmanager/subtask_form.html",
        {
            "form": form,
            "task": subtask.parent_task,
            "page_title": "Edit SubTask",
            "button_text": "Save Changes",
        },
    )


@login_required
def subtask_delete(request, subtask_id):
    subtask = get_object_or_404(SubTask, id=subtask_id)

    if request.method == "POST":
        subtask.delete()
        return redirect("dashboard")

    return render(
        request,
        "taskmanager/subtask_confirm_delete.html",
        {
            "subtask": subtask,
        },
    )

@login_required
def note_create(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = NoteForm(request.POST)

        if form.is_valid():
            note = form.save(commit=False)
            note.task = task
            note.save()
            return redirect("dashboard")

    else:
        form = NoteForm()

    return render(
        request,
        "taskmanager/note_form.html",
        {
            "form": form,
            "task": task,
            "page_title": "Add Note",
            "button_text": "Add Note",
        },
    )


@login_required
def note_edit(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = NoteForm(instance=note)

    return render(
        request,
        "taskmanager/note_form.html",
        {
            "form": form,
            "task": note.task,
            "page_title": "Edit Note",
            "button_text": "Save Changes",
        },
    )


@login_required
def note_delete(request, note_id):
    note = get_object_or_404(Note, id=note_id)

    if request.method == "POST":
        note.delete()
        return redirect("dashboard")

    return render(
        request,
        "taskmanager/note_confirm_delete.html",
        {
            "note": note,
        },
    )

@login_required
def priority_create(request):
    if request.method == "POST":
        form = PriorityForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = PriorityForm()

    return render(
        request,
        "taskmanager/priority_form.html",
        {
            "form": form,
            "page_title": "Add Priority",
            "button_text": "Create Priority",
        },
    )


@login_required
def priority_edit(request, priority_id):
    priority = get_object_or_404(Priority, id=priority_id)

    if request.method == "POST":
        form = PriorityForm(request.POST, instance=priority)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = PriorityForm(instance=priority)

    return render(
        request,
        "taskmanager/priority_form.html",
        {
            "form": form,
            "page_title": "Edit Priority",
            "button_text": "Save Changes",
        },
    )


@login_required
def priority_delete(request, priority_id):
    priority = get_object_or_404(Priority, pk=priority_id)

    task_count = Task.objects.filter(priority=priority).count()

    if task_count > 0:
        return render(
            request,
            "taskmanager/priority_confirm_delete.html",
            {
                "priority": priority,
                "task_count": task_count,
                "blocked": True,
            },
        )

    if request.method == "POST":
        priority.delete()
        return redirect("manage_categories_priorities")

    return render(
        request,
        "taskmanager/priority_confirm_delete.html",
        {
            "priority": priority,
            "task_count": 0,
            "blocked": False,
        },
    )


@login_required
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = CategoryForm()

    return render(
        request,
        "taskmanager/category_form.html",
        {
            "form": form,
            "page_title": "Add Category",
            "button_text": "Create Category",
        },
    )


@login_required
def category_edit(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)

        if form.is_valid():
            form.save()
            return redirect("dashboard")

    else:
        form = CategoryForm(instance=category)

    return render(
        request,
        "taskmanager/category_form.html",
        {
            "form": form,
            "page_title": "Edit Category",
            "button_text": "Save Changes",
        },
    )


@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, pk=category_id)

    task_count = Task.objects.filter(category=category).count()

    if task_count > 0:
        return render(
            request,
            "taskmanager/category_confirm_delete.html",
            {
                "category": category,
                "task_count": task_count,
                "blocked": True,
            },
        )

    if request.method == "POST":
        category.delete()
        return redirect("manage_categories_priorities")

    return render(
        request,
        "taskmanager/category_confirm_delete.html",
        {
            "category": category,
            "task_count": 0,
            "blocked": False,
        },
    )


@login_required
def manage_categories_priorities(request):
    categories = Category.objects.annotate(
        task_count=Count("task", distinct=True),
        has_tasks=Exists(
            Task.objects.filter(category=OuterRef("pk"))
        ),
    ).order_by("name")

    priorities = Priority.objects.annotate(
        task_count=Count("task", distinct=True),
        has_tasks=Exists(
            Task.objects.filter(priority=OuterRef("pk"))
        ),
    ).order_by("name")

    return render(
        request,
        "taskmanager/manage_categories_priorities.html",
        {
            "categories": categories,
            "priorities": priorities,
        },
    )