from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

from taskmanager.models import Category, Note, Priority, SubTask, Task


class Command(BaseCommand):
    help = "Populate the database with sample Hangarin data."

    def handle(self, *args, **options):
        fake = Faker()

        required_categories = [
            "Work",
            "School",
            "Personal",
            "Finance",
            "Projects",
        ]

        required_priorities = [
            "High",
            "Medium",
            "Low",
            "Critical",
            "Optional",
        ]

        categories = {
            category.name: category
            for category in Category.objects.filter(
                name__in=required_categories
            )
        }

        priorities = {
            priority.name: priority
            for priority in Priority.objects.filter(
                name__in=required_priorities
            )
        }

        missing_categories = [
            name for name in required_categories if name not in categories
        ]

        missing_priorities = [
            name for name in required_priorities if name not in priorities
        ]

        if missing_categories or missing_priorities:
            if missing_categories:
                self.stdout.write(
                    self.style.ERROR(
                        "Missing categories: "
                        + ", ".join(missing_categories)
                    )
                )

            if missing_priorities:
                self.stdout.write(
                    self.style.ERROR(
                        "Missing priorities: "
                        + ", ".join(missing_priorities)
                    )
                )

            self.stdout.write(
                self.style.WARNING(
                    "Please add the required Categories and Priorities "
                    "in Django Admin first."
                )
            )
            return

        statuses = ["Pending", "In Progress", "Completed"]

        tasks_created = 0
        notes_created = 0
        subtasks_created = 0

        for _ in range(10):
            task = Task.objects.create(
                title=fake.sentence(),
                description=fake.paragraph(),
                status=fake.random_element(elements=statuses),
                deadline=timezone.make_aware(
                    fake.date_time_this_month()
                ),
                category=fake.random_element(
                    elements=list(categories.values())
                ),
                priority=fake.random_element(
                    elements=list(priorities.values())
                ),
            )
            tasks_created += 1

            for _ in range(2):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(),
                )
                notes_created += 1

            for _ in range(2):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(),
                    status=fake.random_element(elements=statuses),
                )
                subtasks_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully created {tasks_created} Tasks, "
                f"{notes_created} Notes, and "
                f"{subtasks_created} SubTasks."
            )
        )