# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task


@login_required
def index(request):
#    tasks = Task.objects.all()
    tasks = Task.objects.filter(user=request.user)  # Show only user's tasks
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        if title:
#            Task.objects.create(title=title)
            Task.objects.create(title=title, description=description, user=request.user)  # Assign task to user
        return redirect('/')
    return render(request, 'todo/index.html', {'tasks': tasks})


@login_required
def delete_task(request, task_id):
#    Task.objects.get(id=task_id).delete()
    Task.objects.filter(id=task_id, user=request.user).delete()  # Secure deletion

    return redirect('/')
