from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import TaskForm
from .models import Task
#Create your views here.

@login_required
def dashboard(request):
    tasks = Task.objects.select_related(
        "category",
        "priority",
    )

    search_query = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "deadline")

    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query)
            | Q(description__icontains=search_query)
        )

    sort_options = {
        "deadline": "deadline",
        "deadline_desc": "-deadline",
        "title": "title",
        "title_desc": "-title",
        "created": "-created_at",
        "created_oldest": "created_at",
    }

    tasks = tasks.order_by(
        sort_options.get(sort, "deadline")
    )

    context = {
        "tasks": tasks,
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
        "sort": sort,
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