from django import forms
from .models import Task


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'due_date', 'category']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'What needs to be done?',
                'style': 'width: 100%; padding: 8px;',
            }),
            'description': forms.Textarea(attrs={
                'rows': 3,
                'placeholder': 'Optional details...',
                'style': 'width: 100%; padding: 8px;',
            }),
            'priority': forms.Select(attrs={
                'style': 'padding: 8px;',
            }),
            'due_date': forms.DateInput(attrs={
                'type': 'date',
                'style': 'padding: 8px;',
            }),
            'category': forms.Select(attrs={
                'style': 'padding: 8px;',
            }),
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if not title.strip():
            raise forms.ValidationError("Title cannot be empty or just spaces.")
        return title.strip()
