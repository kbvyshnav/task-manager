# tasks/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Task
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .forms import TaskForm
from django.contrib import messages

def home(request):
    stats = {
        "total" : Task.objects.count(),
        "pending" : Task.objects.filter(done=False).count(),
        "done" : Task.objects.filter(done=True).count(),
    }
    context = {
        "app_name" : "Task Manager",
        "current_time": datetime.datetime.now(),
        "stats": stats,
    }
    return render(request, 'tasks/home.html', context)

def task_list(request):
    tasks = Task.objects.all()
    context = {
        "tasks": tasks,
        "total": tasks.count(),
        "pending": tasks.filter(done=False).count(),
        "done": tasks.filter(done=True).count(),
    }
    return render(request, 'tasks/task_list.html', context)

def about(request):
    return render(request, 'tasks/about.html')

def task_detail(request, task_id):
    task = get_object_or_404(Task, id =task_id)
    return render(request, 'tasks/task_detail.html',{'task':task})

def create_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task created successfully !")
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/create_task.html', {'form': form})


def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)  # instance = existing object
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskForm(instance=task)  # pre-fill form with existing data
    return render(request, 'tasks/edit_task.html', {'form': form, 'task': task})


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.delete()
        messages.success(request, f'"{task.title}" has been deleted !')
        return redirect('task_list')
    # GET request — show confirmation page
    return render(request, 'tasks/delete_task.html', {'task': task})


def toggle_done(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        task.done = not task.done  # flip the boolean
        task.save()
    return redirect('task_list')