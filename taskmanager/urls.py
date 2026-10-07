from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("tasks/add/", views.task_create, name="task_create"),
    path("tasks/<int:task_id>/edit/", views.task_edit, name="task_edit"),
    path("tasks/<int:task_id>/delete/", views.task_delete, name="task_delete"),
    path("tasks/<int:task_id>/subtasks/add/", views.subtask_create, name="subtask_create"),
    path("subtasks/<int:subtask_id>/edit/", views.subtask_edit, name="subtask_edit"),
    path("subtasks/<int:subtask_id>/delete/", views.subtask_delete, name="subtask_delete"),
    path("tasks/<int:task_id>/notes/add/", views.note_create, name="note_create"),
    path("notes/<int:note_id>/edit/", views.note_edit, name="note_edit"),
    path("notes/<int:note_id>/delete/", views.note_delete, name="note_delete"),
]