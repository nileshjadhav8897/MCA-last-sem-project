from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.views.generic import UpdateView,ListView
from django.views.decorators.cache import cache_control
from django.contrib import redirects
from django.contrib.sessions.models import Session
from app_cybernatics_protetor.models import adminlogin, success_stories, Job_Postings, CreateAgent, Tips, Applicants, \
    Assign_Agent, CaseDetails, CaseCreation
import datetime
#HOME PAGE URLS FUNCTIONS
def home(re):
    try:
        name=re.session["agent"]
        return render(re, 'home.html', {'name': name})
    except:
        name=re.GET.get("mn")
        return render(re,'home.html',{'name':name})
def findjob(re):

    data=Job_Postings.objects.filter(Last_date__gte=datetime.date.today())
    paginator =Paginator(data,5)
    page_num = re.GET.get('page')
    pa_obj = paginator.get_page(page_num)
    return  render(re,'findjobs.html',{"obj":pa_obj})
def appjob(re):
    jobname = re.GET.get("jobname")
    return render(re, 'apply_jobs.html', {"jobname": jobname})

def ViewApplicants(re):
    JOB_TITLE = re.POST.get("name")
    FN = re.POST.get("fn")
    LN = re.POST.get("ln")
    Dob = re.POST.get("dob")
    Qualification = re.POST.get("quali")
    percentage = re.POST.get("percentage")
    Institute = re.POST.get("institute")
    Experience = re.POST.get("exp")
    Contact_Number = re.POST.get("cno")
    Applicants(JOB_TITLE=JOB_TITLE,First_Name=FN,Last_Name=LN,Dob=Dob,Qualification=Qualification,percentage=percentage,Institute=Institute,Experience=Experience,Contact_Number=Contact_Number).save()
    return render(re,"apply_jobs.html",{'message':'saved'})

def stories(re):
    qs = success_stories.objects.all()
    paginator = Paginator(qs,1)
    page_num=re.GET.get('page')
    pag_obj=paginator.get_page(page_num)
    return render(re,"Stories.html",{"obj":pag_obj})

def Suggest(re):
    name = re.POST.get("name")
    location = re.POST.get("location")
    suggession = re.POST.get('suggession')
    Tips(Name=name,Location=location,Suggession=suggession).save()
    return render(re,"tips.html",{'message':'sent successfully'})
#############################################################################################################################
                                              #END OF HOME URLS
#############################################################################################################################
#HOME ADMIN URLS FUNCTIONS:-
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminloginpage(re):
    name=re.GET.get('mn')
    try:
        if re.session['admin']:
            return render(re,'welcomeadmin.html',{"name":name})
    except:
        return render(re,'admin.html',{"name":name})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def AdminLogin(re):
    username = re.POST.get('name')
    password = re.POST.get('password')
    qs = adminlogin.objects.filter(username=username,password=password)
    if qs:
        re.session['admin']=username
        return render(re,"welcomeadmin.html")
    else:
        return render(re,"admin.html",{'message':'Invalid User'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminlogout(re):
    try:
        del re.session['admin']
        return render(re,'home.html')
    except:
        return render(re,"home.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Success_Stories(re):
    story_title = re.POST.get("t1")
    Description = re.POST.get("t2")
    success_stories(story_title=story_title,Description=Description).save()
    messages.success(re,"New Story Added Successfully ")
    return redirect('/allstories/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def AllStories(re):
    try:
        if re.session['admin']:
            qs = success_stories.objects.all()
            paginator = Paginator(qs,1)
            page_num=re.GET.get('page')
            pag_obj=paginator.get_page(page_num)
            return render(re,"successtories.html",{"obj":pag_obj})
    except:
        return redirect ('/adminlogin/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def jobposting(re):
    try:
       if re.session['admin']:
           return render(re,'jobposting.html')
    except:
        return redirect('/adminlogin/')

def PostSaved(re):
    job = re.POST.get('job')
    title = re.POST.get('name')
    qualification = re.POST.get('qualification')
    percentage = re.POST.get('percentage')
    Experience = re.POST.get('exp')
    LastDate = re.POST.get('lastdate')
    Location = re.POST.get('location')
    Salary = re.POST.get('salary')
    Job_Postings(Job=job,Title=title,
                 Qualification=qualification,Percentage=percentage,
                 Experience=Experience,Last_date=LastDate,Location=Location,Salary=Salary).save()
    return render(re,"jobposting.html",{'message':'Posted Successfully'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def ShowApplicants(re):
    try:
        if re.session['admin']:
            qs = Applicants.objects.all()
            return render(re,"showapplicants.html",{'data':qs})
    except:
        return redirect("/adminlogin/")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def appagent(re):
    try:
        if re.session["admin"]:
            idlist = []
            idlist1=[]
            caseid = CaseDetails.objects.all().values_list("case_id")
            for x in caseid:
                for y in x:
                    idlist.append(y)
            caseid1=CaseCreation.objects.all().values_list("id")
            for a in caseid1:
                for b in a:
                    idlist1.append(b)
            if(all(x in idlist for x in idlist1)):
                flag=1
            else:
                flag=2
            return render(re,"appoint_agent.html",{'data':CaseCreation.objects.all(),"idlist":idlist, "flag":flag})
    except:
        return redirect('/adminlogin/')


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def showAgent(re):
    agent=CreateAgent.objects.all()
    id= re.GET.get("mno")
    recall=CaseCreation.objects.get(id=id)
    return render(re, "appointcaseid.html",{"data":recall,"agent":agent,})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Ass_Agent(re):
    agentid = re.POST.get("agentid")
    caseid = re.POST.get("caseid")
    case_name = re.POST.get("name")
    evidence = re.POST.get("evidence")
    status = re.POST.get("status")
    agentname = CreateAgent.objects.get(id=agentid)
    ag=agentname.Agent_Name
    Assign_Agent(case_id=caseid,agent_id=agentid,Agent_Name=ag).save()
    CaseDetails(agent_id=agentid,case_id=caseid,case_name=case_name,evidence=evidence,status=status).save()
    return appagent(re)

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def agentmanage(re):
    try:
        if re.session['admin']:
            return render(re,'agent_manage.html')
    except:
        return redirect('/adminlogin/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def createagent(re):
    try:
        if re.session['admin']:
            return render(re,'createagent.html')
    except:
        return redirect('/adminlogin/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def AgentRegister(re):
    Agent_Name = re.POST.get("name")
    Password = re.POST.get("password")
    Dob = re.POST.get("dateofbirth")
    Contact_Number = re.POST.get("cno")
    Qualification = re.POST.get("quali")
    Address = re.POST.get("adress")
    email=re.POST.get('email')
    if CreateAgent.objects.filter(Email=email):
        return render(re, "createagent.html", {'message': 'Email Already exists'})
    if CreateAgent.objects.filter(Contact_Number=Contact_Number):
        return render(re,"createagent.html",{'message':"Contact number Already Exists "})
    else:
        CreateAgent(Agent_Name=Agent_Name, Password=Password, Dob=Dob, Contact_Number=Contact_Number,
                    Qualification=Qualification,Address=Address,Email=email).save()
    return render(re, "createagent.html", {'message': 'Created Successfully'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Updateagent(re):
    try:
        if re.session['admin']:
            qs = CreateAgent.objects.all()
            return render(re, "updateagent.html", {'data': qs})
    except:
        return redirect('/adminlogin/')

class editagent(UpdateView):
    model = CreateAgent
    template_name = "editedagent.html"
    fields = ('Agent_Name','Password','Dob','Contact_Number','Qualification','Address')
    success_url = '/editagent/'

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def caseexchange(re):
    try:
        if re.session['admin']:
            data1=CreateAgent.objects.all()
            data=CaseDetails.objects.all()
            return render(re,"CaseChange.html",{"data":data,"data1":data1})
    except:
        return redirect('/adminlogin/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def  agentchange(re):
    ag=re.GET.get("AG")
    ai=re.GET.get("ai")
    caid=re.GET.get("caid")
    ca=re.GET.get("ca")
    data=CreateAgent.objects.all()
    return  render(re ,"AgentChange.html",{"data":data,"ag":ag,"ai":ai,"caid":caid,"ca":ca})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def getagent(re):
    agentid=re.POST.get("agentid")
    caid=re.POST.get("caid")
    CaseDetails.objects.filter(case_id=caid).update(agent_id=agentid)
    return caseexchange(re)
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def AdminViewAgents(re):
    try:
        if re.session['admin']:
            qs = CreateAgent.objects.all()
            return render(re,"viewallagents.html",{'data':qs})
    except:
        return redirect('/adminlogin/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def adminreport(re):
    try:
        if re.session['admin']:
            qs = CaseDetails.objects.all()
            return render(re, "report_admin.html", {'data': qs})
    except:
        return redirect('/adminlogin/')


###################################################################################################################################3
                                  ##End of admin function
###############################################################################################################################
#Agent function urls:-
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def agentlogin(re):
    name=re.GET.get("mn")
    try:
        if re.session['agent']:
            agentname=re.session['agentname']
            return render(re,"welcomeagent.html",{"name":name,"agentname":agentname})
    except:
        return render(re,'agent_login.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def agentlogout(re):
    try:
        del re.session['agent']
        del re.session['agentname']
        return render(re,'home.html')
    except:
        return  render(re,'home.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def loginsucess(re):
    Agent_Name = re.POST.get("name")
    Password = re.POST.get("password")
    qs = CreateAgent.objects.filter(Email=Agent_Name,Password=Password)
    if not qs:
        return render(re,"agent_login.html",{'message':'Invalid Agent'})
    else:
       agentid=CreateAgent.objects.get(Email=Agent_Name)
       name=agentid.id
       agna=agentid.Agent_Name
       re.session['agent'] =Agent_Name
       re.session['agentname']=Agent_Name
       return render(re,"welcomeagent.html",{ "agna":agna,"name":name,"agentname":Agent_Name})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def agentprofile(re):
    try:
        if re.session['agent']:
            id=re.GET.get("mn")
            mypro=CreateAgent.objects.get(id=id)
        return render(re,"agent_profile.html",{"name":id,"x":mypro})
    except:
        return redirect('/agentlogin/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def GetDetails(re):
    try:
        if re.session['agent']:
            id = re.GET.get("mn")
            page_num = re.GET.get('page')
            allre=CaseDetails.objects.filter(agent_id=id).values_list("case_id")
            casidlist = []
            for x in allre:
                for y in x:
                    casidlist.append(y)
            cas=CaseCreation.objects.filter(id__in=casidlist)
            paginator = Paginator(cas,1)
            pag_obj = paginator.get_page(page_num)
            return render(re,"casedetails.html",{"name":id,"cascre":cas,"obj":pag_obj})
    except:
        return redirect('/agentlogin/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upDetails(re):
    try:
        if re.session['agent']:
            id=re.GET.get('mn')
            data=CaseDetails.objects.filter(agent_id=id)
            return render(re,"updateevidence.html",{"data":data,"name":id})
    except:
        return redirect('/agentlogin/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def  UpEvidence(re):
    try:
        if re.session['agent']:
            casid=re.GET.get("mno")
            id=re.GET.get("mn")
            data= CaseDetails.objects.filter(case_id=casid)
            return render(re,"editevidence.html",{"data":data,"name":id})
    except:
        return redirect('/agentlogin/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def upevidences(re):
    try:
        if re.seesion['agent']:
            id=re.GET.get('mn')
            casid=re.POST.get("casid")
            sta=re.POST.get("status")
            evi=re.POST.get("evi")
            CaseDetails.objects.filter(case_id=casid).update(status=sta,evidence=evi)
            CaseCreation.objects.filter(id=casid).update(evidence=evi)
            data = CaseDetails.objects.filter(agent_id=id)
            return render(re,"updateevidence.html", {"data":data, "name": id})
    except:
        return redirect('/agentlogin/')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def casereport(re):
    try:
        if re.session['agent']:
            id = re.GET.get('mn')
            data = CaseDetails.objects.filter(agent_id=id)
            return render(re,"report.html",{'data':data,"name":id})
    except:
        return redirect('/agentlogin/')
##############################################################################################################
###########END OF AGENTS URLS FUNCTION#######################################################################
#MAIN DEFARTMENT FUNCTIONS:
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def defenceloginpage(re):
    name = re.GET.get('mn')
    try:
        if re.session['def']:
            return render(re,"welcomedefence.html",{"name":name})
    except:return render(re,"defence_login.html",{"name":name})
def  deflogout(re):
    try:
        del re.session['def']
        return render(re,'home.html')
    except:return render(re,"home.html")

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Defence(re):
    username = re.POST.get('name')
    password = re.POST.get('password')
    qs = adminlogin.objects.filter(username=username, password=password)
    if qs:
        re.session['def']=username
        return render(re, "welcomedefence.html")
    else:
        return render(re, "defence_login.html", {'message': 'Invalid User'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def defcasecreation(re):
    try:
        if re.session['def']:
            return render(re,"casecreation.html")
    except:
        return redirect('/defenceloginpage/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Create_Case(re):
    case_details= re.POST.get("case details")
    case_name = re.POST.get("case name")
    doc = re.POST.get("date")
    evidence  = re.POST.get("evidence")
    #image  = re.FILES['image']
    CaseCreation(case_name=case_name,case_details=case_details,doc=doc,evidence=evidence,).save()
    return render(re,"casecreation.html",{'message':'case created'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def defencereport(re):
    try:
        if re.session['def']:
            qs = CaseDetails.objects.all()
            return render(re, "report_defence.html", {'data': qs})
    except:
        return redirect('/defenceloginpage/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def defcasedetails(re):
    try:
        if re.session['def']:
            details=CaseCreation.objects.all()
            paginator=Paginator(details,1)
            page_num=re.GET.get('page')
            pag_obj=paginator.get_page(page_num)
            return  render(re,"defence_casedetails.html",{"obj":pag_obj})
    except:
        return redirect('/defenceloginpage/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def suggestions(re):
    try:
        if re.session['def']:
            data=Tips.objects.all()
            paginator = Paginator(data, 1)
            page_num = re.GET.get('page')
            pag_obj = paginator.get_page(page_num)
            return render(re, "Suggestions.html", {"obj":pag_obj})
    except:
        return redirect('/defenceloginpage/')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def defviewagent(re):
    try:
        if re.session['def']:
            qs = CreateAgent.objects.all()
            return render(re,"defallagentview.html",{'data':qs})
    except:
        return redirect('/defenceloginpage/')
#################################################################################################################################################
                                    #End of Dwf
################################################################################################################################################
# ABOUT US
def aboutus(re):
    name=re.GET.get('mn')
    return render(re,"aboutus.html",{"name":name})