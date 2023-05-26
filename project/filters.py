import django_filters
from django_filters import DateFilter, CharFilter, ModelChoiceFilter

from .models import *

class ProjectFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="startDate", lookup_expr='gte', label='Start Date')
    end_date = DateFilter(field_name="completionDate", lookup_expr='lte', label='Completion Date')
    title = CharFilter(field_name="title", lookup_expr='icontains', label='Title')
    description = CharFilter(field_name="description", lookup_expr='icontains', label='Description')
    technology = CharFilter(field_name="technology", lookup_expr='icontains', label='Technology')

    class Meta:
        model = Project
        fields = '__all__'
        exclude = ['estimatedHours', 'startDate', 'completionDate', 'createdtime', 'updatedtime']
        
class ModuleFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="startDate", lookup_expr='gte', label='Start Date')
    moduleName = CharFilter(field_name="moduleName", lookup_expr='icontains', label='Module')
    description = CharFilter(field_name="description", lookup_expr='icontains', label='Description')
    status = ModelChoiceFilter(queryset=Status.objects.all(), empty_label='Select Status')
    project = ModelChoiceFilter(queryset=Project.objects.all(), empty_label='Select Project')

    class Meta:
        model = ProjectModule
        fields = '__all__'
        exclude = ['estimatedHours', 'startDate', 'createdtime', 'updatedtime']

class TaskFilter(django_filters.FilterSet):
    title = CharFilter(field_name="title", lookup_expr='icontains', label='Task')
    priority = CharFilter(field_name="priority", lookup_expr='icontains', label='Priority')
    # priority = ModelChoiceFilter(queryset=Priority.objects.all(), empty_label='Select Priority')
    status = ModelChoiceFilter(queryset=Status.objects.all(), empty_label='Select Status')
    project = ModelChoiceFilter(queryset=Project.objects.all(), empty_label='Select Project')
    module = ModelChoiceFilter(queryset=ProjectModule.objects.all(), empty_label='Select Module')

    class Meta:
        model = Task
        fields = '__all__'
        exclude = ['description', 'totalMinutes', 'createdtime', 'updatedtime']
