from django.db import models
# from django.contrib.auth.models import AbstractUser
from user.models import User

# Create your models here.

# class Role(models.Model):
#     roleName = models.CharField(max_length=20,null=False,unique=True)

#     createdtime = models.DateTimeField(auto_now_add=True)
#     updatedtime = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.roleName

#     class Meta:
#         db_table = 'Role'

# class User(AbstractUser):
#     # role = models.ForeignKey(Role, on_delete=models.CASCADE)

#     createdtime = models.DateTimeField(auto_now_add=True)
#     updatedtime = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.first_name

#     class Meta:
#         db_table = 'user'

# class User(models.Model):
#     firstName = models.CharField(max_length=30)
#     email = models.EmailField(max_length=30)
#     password = models.CharField(max_length=30)
#     role = models.ForeignKey(Role, on_delete=models.CASCADE)

#     createdtime = models.DateTimeField(auto_now_add=True)
#     updatedtime = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.firstName

#     class Meta:
#         db_table = 'User'


class Project(models.Model):
    title = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=500)
    technology = models.CharField(max_length=100)
    estimatedHours = models.PositiveIntegerField()
    startDate = models.DateField()
    completionDate = models.DateField()

    createdtime = models.DateTimeField(auto_now_add=True)
    updatedtime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Project'

class ProjectTeam(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    createdtime = models.DateTimeField(auto_now_add=True)
    updatedtime = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Project_team'

    def __str__(self):
        return self.project.title

class Status(models.Model):
    statusName = models.CharField(max_length=20, null=False, unique=True)

    createdtime = models.DateTimeField(auto_now_add=True)
    updatedtime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.statusName

    class Meta:
        db_table = 'status'

class ProjectModule(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    moduleName = models.CharField(max_length=30, null=False)
    description = models.CharField(max_length=300)
    estimatedHours = models.PositiveIntegerField()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    startDate = models.DateField()

    createdtime = models.DateTimeField(auto_now_add=True)
    updatedtime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.moduleName

    class Meta:
        db_table = 'Project_module'

# class Priority(models.Model):
#     priorityName = models.CharField(max_length=20, null=False, unique=True)

#     createdtime = models.DateTimeField(auto_now_add=True)
#     updatedtime = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.priorityName

#     class Meta:
#         db_table = 'Priority'

class Task(models.Model):
    module = models.ForeignKey(ProjectModule, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    priority = models.CharField(max_length=30)
    # priority = models.ForeignKey(Priority, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=500, null=False)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    totalMinutes = models.PositiveIntegerField()

    createdtime = models.DateTimeField(auto_now_add=True)
    updatedtime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task'

class UserTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_task'

    def __str__(self):
        return self.user.username