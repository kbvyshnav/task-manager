# tasks/views.py
from django.shortcuts import render
from django.http import HttpResponse
from .models import Task
import datetime
from django.shortcuts import render, get_object_or_404

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