from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .forms import *
from .models import *
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from user.decorators import *
from django.db.models import Q
from django.contrib import messages
from django.http.response import JsonResponse

# Create your views here.
# @login_required(login_url='/user/login')
@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ManagerDashboardView(DetailView):
    template_name = 'project/manager_dashboard.html'

    # # chart data
    # labels=[]
    # data =[]
    # labels_task=[]
    # data_task=[]
    # project = Project.objects.all().values_list('title',flat=True).order_by('-id')
    # time = Project.objects.all().values_list('estimatedHours',flat=True).order_by('-id')
    # task = Task.objects.all().values_list('title',flat=True).order_by('-id')
    # minutes = Task.objects.all().values_list('totalMinutes',flat=True).order_by('-id')
    # for i in project:
    #     labels.append(i)
    # for i in time:
    #     data.append(i)
    # for j in task:
    #     labels_task.append(j)
    # for j in minutes:
    #     data_task.append(j)

    def get(self, request, *args, **kwargs):
        # developer Data
        userid = self.request.user.id
        userproject = ProjectTeam.objects.filter(user_id = userid)
        usertaskcount = UserTask.objects.filter(user_id = userid)
        projectuserid = ProjectTeam.objects.filter(user = userid).values('project_id')

        projecttaskid = UserTask.objects.filter(user = userid).values('task_id')
        moduleid = Task.objects.filter(id__in = projecttaskid).values('module_id')
        usermodule = ProjectModule.objects.filter(id__in=moduleid)

        user = User.objects.all()

        # chart data
        labels=[]
        data =[]
        labels_task=[]
        data_task=[]

        if self.request.user.is_manager == True:
            project = Project.objects.order_by('-id')
            usertask = Task.objects.order_by('-id')
            usermodule = ProjectModule.objects.order_by('-id')
            # chart data
            project_chart = Project.objects.all().values_list('title',flat=True).order_by('-id')
            time_chart = Project.objects.all().values_list('estimatedHours',flat=True).order_by('-id')
            task_chart = Task.objects.all().values_list('title',flat=True).order_by('-id')
            minutes_chart = Task.objects.all().values_list('totalMinutes',flat=True).order_by('-id')
            for i in project_chart:
                labels.append(i)
            for i in time_chart:
                data.append(i)
            for j in task_chart:
                labels_task.append(j)
            for j in minutes_chart:
                data_task.append(j)
        else:
            project = Project.objects.filter(id__in=projectuserid).order_by('-id')
            usertask = Task.objects.filter(id__in = projecttaskid).order_by('-id')
            usermodule = ProjectModule.objects.filter(id__in = moduleid).order_by('-id')

            # developer chart data
            project_d_chart = Project.objects.filter(id__in=projectuserid).values_list('title',flat=True).order_by('-id')
            time_d_chart = Project.objects.filter(id__in=projectuserid).values_list('estimatedHours',flat=True).order_by('-id')
            task_d_chart = Task.objects.filter(id__in = projecttaskid).values_list('title',flat=True).order_by('-id')
            minutes_d_chart = Task.objects.filter(id__in = projecttaskid).values_list('totalMinutes',flat=True).order_by('-id')
            for i in project_d_chart:
                labels.append(i)
            for i in time_d_chart:
                data.append(i)
            for j in task_d_chart:
                labels_task.append(j)
            for j in minutes_d_chart:
                data_task.append(j)

        project_count = Project.objects.all().values()
        projectteam = ProjectTeam.objects.order_by('-id')
        projectteam_count = ProjectTeam.objects.all()
        task_count = Task.objects.all()
        # sort data
        sort_by = self.request.GET.get('sort_by', 'title')
        sort_by_user = self.request.GET.get('sort_by_user', 'user')
        direction = self.request.GET.get('direction', 'asc')
        print("....",sort_by)
        print("....",direction)
        if direction == 'asc':
            project = project.order_by(sort_by)
            projectteam = projectteam.order_by(sort_by_user)
        elif direction == 'desc':
            project = project.order_by(f'-{sort_by}')
            projectteam = projectteam.order_by(f'-{sort_by_user}')

        
        context = {'users_count': user.count(), 'projects_count': project_count.count(), 'projectteam_count': projectteam_count.count(), 'project': project[:5], 'projectteam': projectteam[:5], 'task_count': task_count.count(), 'userprojectcount': userproject.count(), 'usertaskcount': usertaskcount.count(), 'usermodulecount': usermodule.count(), 'usertask': usertask, 'usermodule': usermodule[:5], 'labels':labels[:5],'data':data[:5], 'labels_task':labels_task[:5],'data_task':data_task[:5]
                }
        
        return render(request, self.template_name, context)


@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = 'project/project_create.html'
    success_url = '/project/projectlist'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projectlist')
        messages.success(self.request, "Project created successfully!")
        return next

@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ProjectListView(ListView):
    model = Project
    template_name = 'project/project_list.html'
    context_object_name = 'projectlist'

    # def get_queryset(self):
    #     return super().get_queryset()
    
    def get(self, request, *args, **kwargs):
        projectlist = Project.objects.all()
        # sort data
        sort_by = self.request.GET.get('sort_by', 'title')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'asc':
            projectlist = projectlist.order_by(sort_by)
        elif direction == 'desc':
            projectlist = projectlist.order_by(f'-{sort_by}')

        # context = {'projectlist': projectlist}

        # Developer Data
        userid = self.request.user.id
        projectuserid = ProjectTeam.objects.filter(user = userid).values('project_id')

        print("called...")
        input = request.GET.get('input')
        print(input)
        projectlist = []
        if input:
            if self.request.user.is_manager == True:
                projectlist = Project.objects.filter(Q(title__icontains=input) | Q(technology__icontains=input))
                print(projectlist)
            else:
                projectlist = Project.objects.filter(Q(id=projectuserid) | Q(title__icontains=input) | Q(technology__icontains=input))
                print(projectlist)
            return render(request, self.template_name, {'projectlist': projectlist})
        else:
            if self.request.user.is_manager == True:
                projectlist = Project.objects.all()
            else:
                projectlist = Project.objects.filter(id__in=projectuserid)
            return render(request, self.template_name, {'projectlist': projectlist})

        # return render(request, self.template_name, context)
    

@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectCreationForm
    template_name = 'project/project_create.html'
    success_url = '/project/projectlist'

    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projectlist')
        messages.success(self.request, "Project updated successfully!")
        return next

@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'project/project_detail.html'
    context_object_name = 'projectdetail'
    
    def get(self, request, *args, **kwargs):
        team = ProjectTeam.objects.filter(project_id = self.kwargs['pk'])
        module = ProjectModule.objects.filter(project_id = self.kwargs['pk'])
        task = Task.objects.filter(project_id = self.kwargs['pk'])
        # for i in task:
        #     for j in taskuserid:
        #         if i.id==j.task_id:
        #             print('task user id ...',j.task_id)
        #             print('task id ...',i.id)
        #             taskid = i.id
        #             print(taskid)
        taskuser = UserTask.objects.all()
        return render(request, self.template_name, {'projectdetail': self.get_object(), 'team':team, 'module':module, 'task':task, 'taskuser':taskuser})
    
@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = 'project/project_delete.html'
    success_url = '/project/projectlist'
    context_object_name = 'projectdelete'

    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projectlist')
        messages.error(self.request, "Project deleted successfully!")
        return next

    # def get(self, request, *args, **kwargs):
    #     return self.delete(request, *args, **kwargs)
    
    # success_url = 'project/projectlist'
    
@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectTeamCreateView(CreateView):
    model = ProjectTeam
    form_class = ProjectTeamCreationForm
    template_name = 'project/projectteam_create.html'
    success_url = '/project/projectteamlist'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projectteamlist')
        messages.success(self.request, "Project Team created successfully!")
        return next
    
@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ProjectTeamListView(ListView):
    model = ProjectTeam
    template_name = 'project/projectteam_list.html'
    context_object_name = 'projectteamlist'

    # def get_queryset(self):
    #     return super().get_queryset()

    def get(self, request, *args, **kwargs):
        projectteamlist = ProjectTeam.objects.all()
        # sort data
        sort_by = self.request.GET.get('sort_by', 'project')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'asc':
            projectteamlist = projectteamlist.order_by(sort_by)
        elif direction == 'desc':
            projectteamlist = projectteamlist.order_by(f'-{sort_by}')

        # context = {'projectteamlist': projectteamlist}

        print("called...")
        input = request.GET.get('input')
        print(input)
        projectteamlist = []
        if input:
            projectteamlist = ProjectTeam.objects.filter(Q(user__icontains=input) | Q(title__icontains=input) | Q(technology__icontains=input) | Q(status__icontains=input))
            print(projectteamlist)
            return render(request, self.template_name, {'projectteamlist': projectteamlist})
        else:
            projectteamlist = ProjectTeam.objects.all()
            return render(request, self.template_name, {'projectteamlist': projectteamlist})
        
        # return render(request, self.template_name, context)

@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectTeamUpdateView(UpdateView):
    model = ProjectTeam
    form_class = ProjectTeamCreationForm
    template_name = 'project/projectteam_create.html'
    success_url = '/project/projectteamlist'

    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projectteamlist')
        messages.success(self.request, "Project Team updated successfully!")
        return next
    
@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ProjectTeamDetailView(DetailView):
    model = ProjectTeam
    template_name = 'project/projectteam_detail.html'
    context_object_name = 'projectteamdetail'

    def get(self, request, *args, **kwargs):
        team = ProjectTeam.objects.filter(user_id = self.kwargs['pk'])
        return render(request, self.template_name, {'projectteamdetail': self.get_object(), 'team':team})
    
@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectTeamDeleteView(DeleteView):
    model = ProjectTeam
    template_name = 'project/projectteam_delete.html'
    success_url = '/project/projectteamlist'
    context_object_name = 'projectteamdelete'

    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projectteamlist')
        messages.error(self.request, "Project Team deleted successfully!")
        return next

    # def get(self, request, *args, **kwargs):
    #     return self.delete(request, *args, **kwargs)
    
    # success_url = 'project/projectteamlist'

@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectStatusCreateView(CreateView):
    model = Status
    form_class = ProjectStatusCreationForm
    template_name = 'project/projectstatus_create.html'
    success_url = '/project/dashboard'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projectlist')
        messages.success(self.request, "Project Status created successfully!")
        return next

@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectModuleCreateView(CreateView):
    model = ProjectModule
    form_class = ProjectModuleCreationForm
    template_name = 'project/projectmodule_create.html'
    success_url = '/project/projectmodulelist'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projectmodulelist')
        messages.success(self.request, "Project Module created successfully!")
        return next
    
@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ProjectModuleListView(ListView):
    model = ProjectModule
    template_name = 'project/projectmodule_list.html'
    context_object_name = 'projectmodulelist'

    # def get_queryset(self):
    #     return super().get_queryset()

    def get(self, request, *args, **kwargs):
        projectmodulelist = ProjectModule.objects.all()
        # sort data
        sort_by = self.request.GET.get('sort_by', 'project')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'asc':
            projectmodulelist = projectmodulelist.order_by(sort_by)
        elif direction == 'desc':
            projectmodulelist = projectmodulelist.order_by(f'-{sort_by}')

        # context = {'projectmodulelist': projectmodulelist}

        # Developer Data
        userid = self.request.user.id
        projecttaskid = UserTask.objects.filter(user = userid).values('task_id')
        moduleid = Task.objects.filter(id__in = projecttaskid).values('module_id')

        print("called...")
        input = request.GET.get('input')
        print(input)
        projectmodulelist = []
        if input:
            if self.request.user.is_manager == True:
                projectmodulelist = ProjectModule.objects.filter(Q(project__icontains=input) | Q(moduleName__icontains=input) | Q(status__icontains=input) | Q(startDate__icontains=input))
                print(projectmodulelist)
            else:
                projectmodulelist = ProjectModule.objects.filter(Q(id=moduleid) | Q(project__icontains=input) | Q(moduleName__icontains=input) | Q(status__icontains=input) | Q(startDate__icontains=input))
                print(projectmodulelist)
            return render(request, self.template_name, {'projectmodulelist': projectmodulelist})
        else:
            if self.request.user.is_manager == True:
                projectmodulelist = ProjectModule.objects.all()
            else:
                projectmodulelist = ProjectModule.objects.filter(id__in=moduleid)
            return render(request, self.template_name, {'projectmodulelist': projectmodulelist})

        # return render(request, self.template_name, context)

@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectModuleUpdateView(UpdateView):
    model = ProjectModule
    form_class = ProjectModuleCreationForm
    template_name = 'project/projectmodule_create.html'
    success_url = '/project/projectmodulelist'

    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projectmodulelist')
        messages.success(self.request, "Project Module updated successfully!")
        return next

@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ProjectModuleDetailView(DetailView):
    model = ProjectModule
    template_name = 'project/projectmodule_detail.html'
    context_object_name = 'projectmoduledetail'

    def get(self, request, *args, **kwargs):
        module = ProjectModule.objects.filter(project_id = self.kwargs['pk'])
        return render(request, self.template_name, {'projectmoduledetail': self.get_object(), 'module':module})

@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectModuleDeleteView(DeleteView):
    model = ProjectModule
    template_name = 'project/projectmodule_delete.html'
    success_url = '/project/projectmodulelist'
    context_object_name = 'projectmoduledelete'

    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projectmodulelist')
        messages.error(self.request, "Project Module deleted successfully!")
        return next

    # def get(self, request, *args, **kwargs):
    #     return self.delete(request, *args, **kwargs)
    
    # success_url = 'project/projectteamlist'

@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectTaskCreateView(CreateView):
    model = Task
    form_class = ProjectTaskCreationForm
    template_name = 'project/projecttask_create.html'
    success_url = '/project/projecttasklist'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projecttasklist')
        messages.success(self.request, "Project Task created successfully!")
        return next
    
@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ProjectTaskListView(ListView):
    model = Task
    template_name = 'project/projecttask_list.html'
    context_object_name = 'projecttasklist'

    # def get_queryset(self):
    #     return super().get_queryset()

    def get(self, request, *args, **kwargs):
        projecttasklist = Task.objects.all()
        # sort data
        sort_by = self.request.GET.get('sort_by', 'project')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'asc':
            projecttasklist = projecttasklist.order_by(sort_by)
        elif direction == 'desc':
            projecttasklist = projecttasklist.order_by(f'-{sort_by}')

        # context = {'projecttasklist': projecttasklist}

        #  Developer Data
        userid = self.request.user.id
        projecttaskid = UserTask.objects.filter(user = userid).values('task_id')

        print("called...")
        input = request.GET.get('input')
        print(input)
        projecttasklist = []
        if input:
            if self.request.user.is_manager == True:
                projecttasklist = Task.objects.filter(Q(title__icontains=input) | Q(project__icontains=input) | Q(module__icontains=input) | Q(priority__icontains=input) | Q(status__icontains=input))
                print(projecttasklist)
            else:
                projecttasklist = Task.objects.filter(Q(id=projecttaskid) | Q(title__icontains=input) | Q(project__icontains=input) | Q(module__icontains=input) | Q(priority__icontains=input) | Q(status__icontains=input))
                print(projecttasklist)
            return render(request, self.template_name, {'projecttasklist': projecttasklist})
        else:
            if self.request.user.is_manager == True:
                projecttasklist = Task.objects.all()
            else:
                projecttasklist = Task.objects.filter(id__in=projecttaskid)
            return render(request, self.template_name, {'projecttasklist': projecttasklist})

        # return render(request, self.template_name, context)

@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectTaskUpdateView(UpdateView):
    model = Task
    form_class = ProjectTaskCreationForm
    template_name = 'project/projecttask_create.html'
    success_url = '/project/projecttasklist'

    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projecttasklist')
        messages.success(self.request, "Project Task updated successfully!")
        return next

@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ProjectTaskDetailView(DetailView):
    model = Task
    template_name = 'project/projecttask_detail.html'
    context_object_name = 'projecttaskdetail'

    def get(self, request, *args, **kwargs):
        module = ProjectModule.objects.filter(project_id = self.kwargs['pk'])
        task = Task.objects.filter(project_id = self.kwargs['pk'])
        return render(request, self.template_name, {'projecttaskdetail': self.get_object(), 'module':module, 'task':task})

@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectTaskDeleteView(DeleteView):
    model = Task
    template_name = 'project/projecttask_delete.html'
    success_url = '/project/projecttasklist'
    context_object_name = 'projecttaskdelete'

    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projecttasklist')
        messages.error(self.request, "Project Task deleted successfully!")
        return next

    # def get(self, request, *args, **kwargs):
    #     return self.delete(request, *args, **kwargs)
    
    # success_url = 'project/projectteamlist'

@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectTaskUserCreateView(CreateView):
    model = UserTask
    form_class = ProjectTaskUserCreationForm
    template_name = 'project/projecttaskuser_create.html'
    success_url = '/project/projecttaskuserlist'

    def form_valid(self, form):
        return super().form_valid(form)
    
    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projecttaskuserlist')
        messages.success(self.request, "Task User created successfully!")
        return next
    
@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ProjectTaskUserListView(ListView):
    model = UserTask
    template_name = 'project/projecttaskuser_list.html'
    context_object_name = 'projecttaskuserlist'

    # def get_queryset(self):
    #     return super().get_queryset()

    def get(self, request, *args, **kwargs):
        projecttaskuserlist = UserTask.objects.all()
        # sort data
        sort_by = self.request.GET.get('sort_by', 'task')
        direction = self.request.GET.get('direction', 'asc')
        if direction == 'asc':
            projecttaskuserlist = projecttaskuserlist.order_by(sort_by)
        elif direction == 'desc':
            projecttaskuserlist = projecttaskuserlist.order_by(f'-{sort_by}')

        # context = {'projecttaskuserlist': projecttaskuserlist}

        print("called...")
        input = request.GET.get('input')
        print(input)
        projecttaskuserlist = []
        if input:
            projecttaskuserlist = UserTask.objects.filter(Q(user__icontains=input) | Q(task__icontains=input) | Q(project__icontains=input) | Q(status__icontains=input))
            print(projecttaskuserlist)
            return render(request, self.template_name, {'projecttaskuserlist': projecttaskuserlist})
        else:
            projecttaskuserlist = UserTask.objects.all()
            return render(request, self.template_name, {'projecttaskuserlist': projecttaskuserlist})

        # return render(request, self.template_name, context)
    
@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectTaskUserUpdateView(UpdateView):
    model = UserTask
    form_class = ProjectTaskUserCreationForm
    template_name = 'project/projecttaskuser_create.html'
    success_url = '/project/projecttaskuserlist'

    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projecttaskuserlist')
        messages.success(self.request, "Task User updated successfully!")
        return next

@method_decorator(login_required(login_url='/user/login'), name='dispatch')
class ProjectTaskUserDetailView(DetailView):
    model = UserTask
    template_name = 'project/projecttaskuser_detail.html'
    context_object_name = 'projecttaskuserdetail'

    def get(self, request, *args, **kwargs):
        task = Task.objects.all()
        print(task)
        module = ProjectModule.objects.all()
        return render(request, self.template_name, {'projecttaskuserdetail': self.get_object(), 'module':module, 'task':task})

@method_decorator([login_required(login_url='/user/login'), manager_required], name='dispatch')
class ProjectTaskUserDeleteView(DeleteView):
    model = UserTask
    template_name = 'project/projecttaskuser_delete.html'
    success_url = '/project/projecttaskuserlist'
    context_object_name = 'projecttaskuserdelete'

    def get_success_url(self):
        next = self.request.POST.get('next', '/project/projecttaskuserlist')
        messages.error(self.request, "Task User deleted successfully!")
        return next

    # def get(self, request, *args, **kwargs):
    #     return self.delete(request, *args, **kwargs)
    
    # success_url = 'project/projectteamlist'

def projectlistAjax(request):
    projects = Project.objects.all().values_list('title',flat=True)
    modules = ProjectModule.objects.all().values_list('moduleName',flat=True)
    tasks = Task.objects.all().values_list('title',flat=True)
    projectList = [item for projectList in zip(projects, modules, tasks) for item in projectList]
    # projectList = list(projects)

    return JsonResponse(projectList, safe=False)

def searchproject(request):
    if request.method == 'POST':
        searchedterm = request.POST.get('projectsearch')
        if searchedterm == "":
            return redirect(request.META.get('HTTP_REFERER'))
        else:
            project = Project.objects.filter(title__contains=searchedterm).first()
            module = ProjectModule.objects.filter(moduleName__contains=searchedterm).first()
            task = Task.objects.filter(title__contains=searchedterm).first()

            if project:
                return redirect(f'/project/projectdetail/{project.id}')
            elif module:
                return redirect(f'/project/projectmoduledetail/{module.id}')
            elif task:
                return redirect(f'/project/projecttaskdetail/{task.id}')
            else:
                messages.info(request, "No project matched your search")
                return redirect(request.META.get('HTTP_REFERER'))
            
    return redirect(request.META.get('HTTP_REFERER'))
