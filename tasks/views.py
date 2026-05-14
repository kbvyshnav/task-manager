from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

def home(request):
    today=datetime.today().strftime("%d-%m-%Y")

    return HttpResponse(
        f"Welcome to Task Manager — Home Page <br> Today's date is: {today}"
    )

def about(request):
    return HttpResponse("<h1>About</h1><p>This is a task manager app built with Django.</p>")

def task_list(request):
    return render(request, 'tasks/task_list.html')

def task_detail(request, task_id):
    return HttpResponse(f"Viewing task number {task_id}")
