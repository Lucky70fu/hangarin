from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Task
# Create your views here.



@login_required
def dashboard(request):
    tasks = Task.objects.select_related(
        "category",
        "priority",
    ).order_by("deadline")

    context = {
        "tasks": tasks,
        "total_tasks": tasks.count(),
        "pending_tasks": tasks.filter(status="Pending").count(),
        "in_progress_tasks": tasks.filter(status="In Progress").count(),
        "completed_tasks": tasks.filter(status="Completed").count(),
    }

    return render(request, "taskmanager/dashboard.html", context)