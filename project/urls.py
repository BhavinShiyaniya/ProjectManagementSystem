from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('dashboard/', ManagerDashboardView.as_view(), name='dashboard'),
    path('projectcreate/', ProjectCreateView.as_view(), name='projectcreate'),
    path('projectlist/', ProjectListView.as_view(), name='projectlist'),
    path('projectteamcreate/', ProjectTeamCreateView.as_view(), name='projectteamcreate'),
    path('projectteamlist/', ProjectTeamListView.as_view(), name='projectteamlist'),
    path('projectupdate/<int:pk>', ProjectUpdateView.as_view(), name='projectupdate'),
    path('projectdetail/<int:pk>', ProjectDetailView.as_view(), name='projectdetail'),
    path('projectdelete/<int:pk>', ProjectDeleteView.as_view(), name='projectdelete'),
    path('projectteamupdate/<int:pk>', ProjectTeamUpdateView.as_view(), name='projectteamupdate'),
    path('projectteamdetail/<int:pk>', ProjectTeamDetailView.as_view(), name='projectteamdetail'),
    path('projectteamdelete/<int:pk>', ProjectTeamDeleteView.as_view(), name='projectteamdelete'),
    path('projectstatuscreate/', ProjectStatusCreateView.as_view(), name='projectstatuscreate'),
    path('projectmodulecreate/', ProjectModuleCreateView.as_view(), name='projectmodulecreate'),
    path('projectmodulelist/', ProjectModuleListView.as_view(), name='projectmodulelist'),
    path('projectmoduleupdate/<int:pk>', ProjectModuleUpdateView.as_view(), name='projectmoduleupdate'),
    path('projectmoduledetail/<int:pk>', ProjectModuleDetailView.as_view(), name='projectmoduledetail'),
    path('projectmoduledelete/<int:pk>', ProjectModuleDeleteView.as_view(), name='projectmoduledelete'),
    path('projecttaskcreate/', ProjectTaskCreateView.as_view(), name='projecttaskcreate'),
    path('projecttasklist/', ProjectTaskListView.as_view(), name='projecttasklist'),
    path('projecttaskupdate/<int:pk>', ProjectTaskUpdateView.as_view(), name='projecttaskupdate'),
    path('projecttaskdetail/<int:pk>', ProjectTaskDetailView.as_view(), name='projecttaskdetail'),
    path('projecttaskdelete/<int:pk>', ProjectTaskDeleteView.as_view(), name='projecttaskdelete'),

    path('projecttaskusercreate/', ProjectTaskUserCreateView.as_view(), name='projecttaskusercreate'),
    path('projecttaskuserlist/', ProjectTaskUserListView.as_view(), name='projecttaskuserlist'),
    path('projecttaskuserupdate/<int:pk>', ProjectTaskUserUpdateView.as_view(), name='projecttaskuserupdate'),
    path('projecttaskuserdetail/<int:pk>', ProjectTaskUserDetailView.as_view(), name='projecttaskuserdetail'),
    path('projecttaskuserdelete/<int:pk>', ProjectTaskUserDeleteView.as_view(), name='projecttaskuserdelete'),

    path('project-list', projectlistAjax),
    path('searchproject', searchproject, name='searchproject'),
]