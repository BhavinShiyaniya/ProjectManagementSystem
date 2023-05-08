from django.contrib import admin
from .models import *

# Register your models here.
class ProjectList(admin.ModelAdmin):
    list_display = ("title", "technology", "startDate", "completionDate")

admin.site.register(Project, ProjectList)

class ProjectTeamList(admin.ModelAdmin):
    list_display = ("user", "project")

admin.site.register(ProjectTeam, ProjectTeamList)
admin.site.register(Status)

class ProjectModuleList(admin.ModelAdmin):
    list_display = ("moduleName", "project", 'status')

admin.site.register(ProjectModule, ProjectModuleList)

class ProjectTaskList(admin.ModelAdmin):
    list_display = ("title", "project", "module", "priority")

admin.site.register(Task, ProjectTaskList)

class UserTaskList(admin.ModelAdmin):
    list_display = ("user", "task")

admin.site.register(UserTask, UserTaskList)