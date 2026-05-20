# tasks/views.py
from django.shortcuts import render
from django.http import HttpResponse
import datetime

def home(request):
    context = {
        "app_name" : "Task Manager",
        "current_time": datetime.datetime.now(),
        "stats": {
            "total": 5,
            "pending": 3,
            "done": 2,
        }
    }
    return render(request, 'tasks/home.html', context)

def task_list(request):
    tasks = [
        {"id": 1, "title": "Buy groceries", "done": True, "priority": "low"},
        {"id": 2, "title": "Fix login bug", "done": False, "priority": "high"},
        {"id": 3, "title": "Write unit tests", "done": False, "priority": "medium"},
        {"id": 4, "title": "Update README", "done": True, "priority": "low"},
        {"id": 5, "title": "Deploy to staging", "done": False, "priority": "high"},
    ]
    tasks.sort(key=lambda task: task["done"])

    context = {
        "tasks": tasks,
        "total": len(tasks),
        "pending": len([t for t in tasks if not t["done"]]),
        "done": len([t for t in tasks if t["done"]]),
    }
    return render(request, 'tasks/task_list.html', context)

def about(request):
    return render(request, 'tasks/about.html')