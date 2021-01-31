from app_cybernatics_protetor import views
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    #PROJECT HOME URLS
    path('',views.home, name='home'),
    path('find_jobs/', views.findjob, name='findjob'),
    path('apply_jobs/', views.appjob),
    path('applicant/', views.ViewApplicants),
    path('stories/', views.stories, name="stories"),
    path('tips/', TemplateView.as_view(template_name="tips.html")),
    path('suggest/', views.Suggest),
    #End of home urls

    # PROJECT ADMIN URLS
    path('adminlogin/',views.adminloginpage),
    path('welcomeadmin/', views.AdminLogin),
    path('admin_logout/',views.adminlogout,name="adminlogout"),
    path('allstories/', views.AllStories,name='allstories'),
    path('succestories/', views.Success_Stories),
    path('job/',views.jobposting),
    path('postsaved/', views.PostSaved),
    path('viewapplicants/', views.ShowApplicants),
    path('app_agent/', views.appagent),
    path("assign_agent/", views.showAgent),
    path('savecasedetails/', views.Ass_Agent),
    path('agentmanage/',views.agentmanage),
    path('createagent/',views.createagent),
    path('agentregister/', views.AgentRegister),
    path('editagent/', views.Updateagent),
    path('update<int:pk>/', views.editagent.as_view()),
    path('caseexchange/',views.caseexchange,name="caseexchange"),
    path('agentchange/',views.agentchange,name="agentchange"),
    path('getagent/',views.getagent,name="getagent"),
    path('viewallagents/', views.AdminViewAgents),
    path('reports_admin/', views.adminreport),
    #end of admin urls

    #PROJECT AGENT URLS

    path('agentlogin/',views.agentlogin),
    path('agentlogout/',views.agentlogout),
    path('agentsign/', views.loginsucess),
    path('agentprofile/', views.agentprofile, name="agentprofile"),
    path('agentcase/', views.GetDetails),
    path('update_evidence/', views.upDetails),
    path('upevidence/', views.UpEvidence, name="upevidence"),
    path('upevidences/', views.upevidences, name="upevidences"),
    path('reports/', views.casereport),

#PROJECT MAIN DEPARTMENT URLS
    path('defenceloginpage/',views.defenceloginpage),
    path('welcomedefence/', views.Defence),
    path('suggestions/',views.suggestions, name="suggestions"),
    path('case_creation/',views.defcasecreation),
    path('create_case/', views.Create_Case),
    path('defviewagent/', views.defviewagent),
    path('defcasedetails/', views.defcasedetails, name="defcasedetails"),
    path('reports_defence/', views.defencereport),
    path('defence_logout/',views.deflogout),
    #end of main deparment urls

    #PROJECT ABOUT URLS
    path('about/',views.aboutus,name="aboutus"),
]
