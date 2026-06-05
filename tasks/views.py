from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotAllowed
from django.contrib import messages

from .models import Task, Category
from .forms import TaskForm


def home(request):
    stats = {
        "total": Task.objects.count(),
        "pending": Task.objects.filter(done=False).count(),
        "done": Task.objects.filter(done=True).count(),
    }
    return render(request, "tasks/home.html", {"stats": stats})


def task_list(request):
    tasks = Task.objects.select_related('category').all()

    status = request.GET.get('status')
    priority = request.GET.get('priority')
    category_id = request.GET.get('category')

    if status == 'done':
        tasks = tasks.filter(done=True)
    elif status == 'pending':
        tasks = tasks.filter(done=False)

    if priority in ('low', 'medium', 'high'):
        tasks = tasks.filter(priority=priority)

    if category_id:
        tasks = tasks.filter(category_id=category_id)

    categories = Category.objects.all()

    context = {
        "tasks": tasks,
        "total": tasks.count(),
        "pending": tasks.filter(done=False).count(),
        "done": tasks.filter(done=True).count(),
        "categories": categories,
        "current_status": status or '',
        "current_priority": priority or '',
        "current_category": category_id or '',
    }

    return render(request, "tasks/task_list.html", context)


def about(request):
    return render(request, "tasks/about.html")


def task_detail(request, task_id):
    task = get_object_or_404(Task.objects.select_related('category'), id=task_id)
    return render(request, "tasks/task_detail.html", {"task": task})


def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully!")
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(request, "tasks/create_task.html", {"form": form})


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated successfully!")
            return redirect("task_detail", task_id=task.id)
    else:
        form = TaskForm(instance=task)

    return render(request, "tasks/edit_task.html", {"form": form, "task": task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    if request.method == "POST":
        task_title = task.title
        task.delete()
        messages.success(request, f'"{task_title}" has been deleted!')
        return redirect("task_list")

    return render(request, "tasks/delete_task.html", {"task": task})


def toggle_done(request, task_id):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    task = get_object_or_404(Task, id=task_id)
    task.done = not task.done
    task.save()

    status = "done" if task.done else "pending"
    messages.success(request, f'"{task.title}" marked as {status}.')
    return redirect("task_list")
