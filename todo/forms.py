from datetime import date, timezone
from django import forms
from .models import Task
from django.utils.timezone import now


class TaskForm(forms.ModelForm):
    due_date = forms.DateField(
       # widget=forms.DateInput(format='%d.%m.%Y', attrs={'type': 'date'}),
       # input_formats=['%d.%m.%Y'],


        widget=forms.DateInput(attrs={'type': 'date'}),
        input_formats=['%Y-%m-%d', '%d.%m.%Y'],  # dodan ISO format

        initial=now()
    )


# due_date = forms.DateField(
#    widget=forms.TextInput(attrs={'placeholder': 'dd.mm.yyyy'}),
#    input_formats=['%d.%m.%Y'],
#    initial=now()
# )


    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title'}),
        required=True
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Task description', 'rows': 3}),
        required=False
    )

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Task description', 'rows': 3}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'title': 'Task Title',
            'description': 'Description',
            'due_date': 'Due Date',
        }
        help_texts = {
            'title': 'Enter the title of the task.',
            'description': 'Enter a detailed description of the task.',
            'due_date': 'Select the due date for the task.',
        }
        error_messages = {
            'title': {
                'required': 'This field is required.',
                'max_length': 'Title cannot exceed 200 characters.',
            },
            'description': {
                'max_length': 'Description cannot exceed 500 characters.',
            },
        }

    # Add any additional validation or customization here
    def clean_due_date(self):
        due_date = self.cleaned_data.get('due_date')
        if due_date and due_date < date.today():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        description = cleaned_data.get('description')

        if not title and not description:
            raise forms.ValidationError("At least one of title or description must be provided.")
            return cleaned_data

    def save(self, commit=True):
        task = super().save(commit=False)
        if commit:
            task.save()
        return task

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('task_detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        from django.urls import reverse
        return reverse('task_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        from django.urls import reverse
        return reverse('task_delete', kwargs={'pk': self.pk})

    def get_fields(self):
        return self._meta.fields

    def get_field_names(self):
        return [field.name for field in self._meta.fields]

    def get_field_labels(self):
        return {field.name: field.label for field in self._meta.fields}

