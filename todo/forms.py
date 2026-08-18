from django import forms
from .models import TodoItem, TodoCategory, TodoTag

class TodoItemForm(forms.ModelForm):
    """Form for creating and updating todo items"""
    
    class Meta:
        model = TodoItem
        fields = ['title', 'description', 'priority', 'status', 'due_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Add task details',
                'rows': 4,
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select',
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
            }),
            'due_date': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local',
            }),
        }


class TodoCategoryForm(forms.ModelForm):
    """Form for creating and updating categories"""
    
    class Meta:
        model = TodoCategory
        fields = ['name', 'description', 'color']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Category name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Category description',
                'rows': 3,
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'type': 'color',
            }),
        }


class TodoFilterForm(forms.Form):
    """Form for filtering todos"""
    
    FILTER_CHOICES = [
        ('all', 'All Tasks'),
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    STATUS_FILTER = [
        ('all', 'All Priorities'),
        ('low', 'Low Priority'),
        ('medium', 'Medium Priority'),
        ('high', 'High Priority'),
    ]
    
    status = forms.ChoiceField(
        choices=FILTER_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    priority = forms.ChoiceField(
        choices=STATUS_FILTER,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False
    )
    search = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search tasks...'
        }),
        required=False
    )
