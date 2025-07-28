# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
from django.contrib import messages  # če želiš prikazati napake tudi v predlogi

from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from datetime import date  # za validacijo datuma
from django.http import HttpResponseRedirect
from django.urls import reverse




@login_required
def index(request):
    priority_filter = request.GET.get('priority')

#   tasks = Task.objects.all()
#   Show only user's tasks
    if priority_filter:
        tasks = Task.objects.filter(user=request.user, priority=priority_filter).order_by('priority')
    else:
        tasks = Task.objects.filter(user=request.user).order_by('priority')

    # If the request method is POST, handle form submission
    # Otherwise, render the index page with the tasks and an empty form
    if request.method == "POST":
        # Handle form submission
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('index')
    else:
        form = TaskForm()
    return render(request, 'todo/index.html', {'tasks': tasks, 'form': form})


@login_required
def add_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            # Save the task with the current user and redirect to the index page
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('index')
        else:
            # Optional: log or print form errors for debugging

            # Logiranje napak v konzolo
            print("Form is not valid:")
            print(form.errors.as_data())  # struktura napak
            print(form.errors)            # berljive napake

            # Če želiš prikazati napako v predlogi (neobvezno)
            messages.error(request, "There was an error saving the task.")

            tasks = Task.objects.filter(user=request.user)
            return render(request, 'todo/index.html', {'tasks': tasks, 'form': form})
    else:
        # Če nekdo obišče /add/ z GET metodo, ga preusmerimo
        return redirect('index')


@login_required
def delete_task(request, task_id):
#    Task.objects.get(id=task_id).delete()
    Task.objects.filter(id=task_id, user=request.user).delete()  # Secure deletion

    return redirect('/')


def task_list(request):
    priority_filter = request.GET.get('priority')
    if priority_filter:
        tasks = Task.objects.filter(priority=priority_filter).order_by('priority')
    else:
        tasks = Task.objects.all().order_by('priority')
    return render(request, 'task_list.html', {'tasks': tasks})


@login_required
def task_detail(request, task_id):
    task = Task.objects.get(id=task_id, user=request.user)

