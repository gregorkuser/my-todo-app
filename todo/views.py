# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm

from django.contrib import messages  # če želiš prikazati napake tudi v predlogi



@login_required
def index(request):
#    tasks = Task.objects.all()
    tasks = Task.objects.filter(user=request.user)  # Show only user's tasks
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

            # 🔍 Logiranje napak v konzolo
            print("Form is not valid:")
            print(form.errors.as_data())  # struktura napak
            print(form.errors)            # berljive napake

            # 🔔 Če želiš prikazati napako v predlogi (neobvezno)
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
