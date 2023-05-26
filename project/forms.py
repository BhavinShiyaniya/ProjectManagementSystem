from django import forms
from django.db import transaction
from .models import Project, ProjectTeam, Status, ProjectModule, Task, UserTask
from user.models import User
from django.db.models import Q

class ProjectCreationForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Project Description'}),
            'technology': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Project Technology'}),
            'estimatedHours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '12'}),
            'startDate': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'MM/DD/YYYY'}),
            'completionDate': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'MM/DD/YYYY'})
        }

    @transaction.atomic
    def save(self):
        project = super().save(commit=False)
        project.save()
        return project

class ProjectTeamCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(Q(is_teamleader=True) | Q(is_developer=True) | Q(is_tester=True)), empty_label="Select User", widget=forms.Select(attrs={'class': 'form-control', 'value':'Select User'}))

    class Meta:
        model = ProjectTeam
        fields = '__all__'

        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super(ProjectTeamCreationForm, self).__init__(*args, **kwargs)
        self.fields['project'].empty_label = "Select Project"

    @transaction.atomic
    def save(self):
        projectteam = super().save(commit=False)
        projectteam.save()
        return projectteam

class ProjectStatusCreationForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = '__all__'

        widgets = {
            'statusName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Status Name'})
        }

class ProjectModuleCreationForm(forms.ModelForm):
    class Meta:
        model = ProjectModule
        fields = '__all__'

        widgets = {
            'project': forms.Select(attrs={'class': 'form-control'}),
            'moduleName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Module Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'estimatedHours': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '12'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'startDate': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'MM/DD/YYYY'})
        }

    def __init__(self, *args, **kwargs):
        super(ProjectModuleCreationForm, self).__init__(*args, **kwargs)
        self.fields['project'].empty_label = "Select Project"
        self.fields['status'].empty_label = "Select Status"

# class TaskPriorityCreationForm(forms.ModelForm):
#     class Meta:
#         model = Priority
#         fields = '__all__'

#         widgets = {
#             'priorityName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Priority Name'})
#         }

class ProjectTaskCreationForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

        widgets = {
            'module': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Task Title'}),
            'priority': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Priority'}),
            # 'priority': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'totalMinutes': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '12'})
        }
        
    def __init__(self, *args, **kwargs):
        super(ProjectTaskCreationForm, self).__init__(*args, **kwargs)
        self.fields['module'].empty_label = "Select Module"
        self.fields['project'].empty_label = "Select Project"
        # self.fields['priority'].empty_label = "Select Priority"
        self.fields['status'].empty_label = "Select Status"

class ProjectTaskUserCreationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.filter(Q(is_teamleader=True) | Q(is_developer=True) | Q(is_tester=True)), empty_label="Select User", widget=forms.Select(attrs={'class': 'form-control', 'value':'Select User'}))

    class Meta:
        model = UserTask
        fields = '__all__'

        widgets = {
            'task': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        super(ProjectTaskUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['task'].empty_label = "Select Task"