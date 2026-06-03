# tasks/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone

from .models import Task
from .forms import TaskForm


def home(request):
    stats = {
        "total": Task.objects.count(),
        "pending": Task.objects.filter(done=False).count(),
        "done": Task.objects.filter(done=True).count(),
    }

    context = {
        "app_name": "Task Manager",
        "current_time": timezone.now(),
        "stats": stats,
    }

    return render(request, "tasks/home.html", context)


def task_list(request):
    tasks = Task.objects.all()

    context = {
        "tasks": tasks,
        "total": tasks.count(),
        "pending": tasks.filter(done=False).count(),
        "done": tasks.filter(done=True).count(),
    }

    return render(request, "tasks/task_list.html", context)


def about(request):
    return render(request, "tasks/about.html")


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    return render(
        request,
        "tasks/task_detail.html",
        {"task": task}
    )


def create_task(request):

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Task created successfully!"
            )

            return redirect("task_list")

    else:
        form = TaskForm()

    return render(
        request,
        "tasks/create_task.html",
        {"form": form}
    )


def edit_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":

        form = TaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Task updated successfully!"
            )

            return redirect(
                "task_detail",
                task_id=task.id
            )

    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "tasks/edit_task.html",
        {
            "form": form,
            "task": task,
        }
    )


def delete_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":

        task_title = task.title

        task.delete()

        messages.success(
            request,
            f'"{task_title}" has been deleted!'
        )

        return redirect("task_list")

    return render(
        request,
        "tasks/delete_task.html",
        {"task": task}
    )


def toggle_done(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":

        task.done = not task.done
        task.save()

        if task.done:
            messages.success(
                request,
                f'"{task.title}" marked as done.'
            )
        else:
            messages.success(
                request,
                f'"{task.title}" marked as pending.'
            )

    return redirect("task_list")# tasks/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone

from .models import Task
from .forms import TaskForm


def home(request):
    stats = {
        "total": Task.objects.count(),
        "pending": Task.objects.filter(done=False).count(),
        "done": Task.objects.filter(done=True).count(),
    }

    context = {
        "app_name": "Task Manager",
        "current_time": timezone.now(),
        "stats": stats,
    }

    return render(request, "tasks/home.html", context)


def task_list(request):
    tasks = Task.objects.all()

    context = {
        "tasks": tasks,
        "total": tasks.count(),
        "pending": tasks.filter(done=False).count(),
        "done": tasks.filter(done=True).count(),
    }

    return render(request, "tasks/task_list.html", context)


def about(request):
    return render(request, "tasks/about.html")


def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    return render(
        request,
        "tasks/task_detail.html",
        {"task": task}
    )


def create_task(request):

    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Task created successfully!"
            )

            return redirect("task_list")

    else:
        form = TaskForm()

    return render(
        request,
        "tasks/create_task.html",
        {"form": form}
    )


def edit_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":

        form = TaskForm(
            request.POST,
            instance=task
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Task updated successfully!"
            )

            return redirect(
                "task_detail",
                task_id=task.id
            )

    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "tasks/edit_task.html",
        {
            "form": form,
            "task": task,
        }
    )


def delete_task(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":

        task_title = task.title

        task.delete()

        messages.success(
            request,
            f'"{task_title}" has been deleted!'
        )

        return redirect("task_list")

    return render(
        request,
        "tasks/delete_task.html",
        {"task": task}
    )


def toggle_done(request, task_id):

    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":

        task.done = not task.done
        task.save()

        if task.done:
            messages.success(
                request,
                f'"{task.title}" marked as done.'
            )
        else:
            messages.success(
                request,
                f'"{task.title}" marked as pending.'
            )

    return redirect("task_list")