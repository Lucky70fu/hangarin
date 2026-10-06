from django import forms

from .models import Task, SubTask


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "title",
            "description",
            "status",
            "deadline",
            "priority",
            "category",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter task title",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "placeholder": "Describe the task",
                    "rows": 5,
                }
            ),
            "deadline": forms.DateTimeInput(
                format="%Y-%m-%dT%H:%M",
                attrs={
                    "type": "datetime-local",
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["deadline"].input_formats = [
            "%Y-%m-%dT%H:%M",
        ]

        if self.instance and self.instance.pk and self.instance.deadline:
            self.initial["deadline"] = self.instance.deadline.strftime(
                "%Y-%m-%dT%H:%M"
            )

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = [
            "title",
            "status",
        ]

        widgets = {
            "title": forms.TextInput(
                attrs={
                    "placeholder": "Enter subtask title",
                }
            ),
        }