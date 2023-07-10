from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect 
from django.urls import reverse
from django.db import IntegrityError
from .forms import TaskForm, CateForm, CateTaskForm, GroupForm,GroupMembersForm,TaskGroupForm
from .models import Task , CategoryTest, CategoryTestTask, GroupMembers, GroupUsers,TaskGroup
from django.utils import timezone 
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):    
    if request.method == 'GET':
        print( 'Sending form registration')
        return render(request, 'signup.html',{
        'form': UserCreationForm 
    })
    else:
        if request.POST['password1'] == request.POST['password2']:
            #register user
            try:
                user= User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('usertask')
            except IntegrityError:
                return render(request, 'login.html',{
                    'form': UserCreationForm,
                    'error': 'User already exists'
                })
        return render(request,'signup.html',{
            'form': UserCreationForm,
            'error':'Password do not match'})
        # print(request.POST)
        # print('Obtaining data')

def loguserout(request):
    logout(request)
    return redirect('home')

def loguserin(request):
    if request.method == 'GET':
        return render(request,'login.html',{
            'form': AuthenticationForm,
        })
    else:
        user = authenticate(request, username=request.POST['username'], 
        password=request.POST['password'])
        if user is None:
            return render(request,'login.html',{
            'form': AuthenticationForm,
            'error': 'Username or password is incorrect'
            })
        else:
            login(request,user)
            return redirect('usertask')



#from here, requires login 


@login_required
def createTask(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            print(new_task)
            return redirect('usertask')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error':'Please provide valid data'
        })
@login_required        
def task(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'usertask.html',
    {'tasks': tasks})

@login_required
def taskend(request):
    tasks = Task.objects.filter(user=request.user,
    datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'usertask.html',
    {'tasks': tasks})

@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user= request.user)
        form = TaskForm(instance=task) 
        # print(task_id)
        return render(request, 'usertaskdetail.html',{'task':task , 'form':form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id ,user= request.user)
            # task.filetask = request.POST['filetask'] or task.filetask
            # task.save()
            form= TaskForm(request.POST, instance=task)
            form.save()
            return redirect('usertask')
        except ValueError:
            return render(request, 'usertaskdetail.html',
            {'task':task , 'form':form , 'error': 'Error updating task'})

@login_required            
def taskComplete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user= request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('usertask')
    
@login_required    
def taskDelete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user= request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('usertask')
    
#categories here
    
@login_required
def createCategory(request):   
    if request.method == 'GET':
        return render(request, 'create_category.html',{
        'form': CateForm, 
        })
    else:
        try:
            form = CateForm(request.POST)
            new_cate = form.save(commit=False)
            new_cate.userName = request.user
            new_cate.save()
            print(new_cate)
            return redirect('categories')
        except ValueError:
            return render(request, 'create_category.html',{
            'form': CateForm,
            'error':'Please provide valid data'
        })
            
@login_required        
def category(request):
    if request.method == 'GET':
        cateform = CateTaskForm()
        cateform.filtx(request.user)
        cate = CategoryTest.objects.filter(userName=request.user).order_by('Name')
        taskcate = []
        for x in cate:
            xcate = CategoryTestTask.objects.filter(category=x)
            taskcate.append(xcate)
        return render(request, 'category.html',
        {'cate': cate, 'task': taskcate , 'form':cateform })
    else:
        try:
            form = CateTaskForm(request.POST)
            form.save()
            return redirect('categories')
        
        except ValueError:
            cateform = CateTaskForm()
            cateform.filtx(request.user)
            cate = CategoryTest.objects.filter(userName=request.user).order_by('Name')
            taskcate = []
            for x in cate:
                xcate = CategoryTestTask.objects.filter(category=x)
                taskcate.append(xcate)
            return render(request, 'category.html',
            {'cate': cate, 'task': taskcate , 'form':cateform, 'error':'the task you selected is already in the category'})
    

@login_required
def deleteCategory(request, category_id):
    category = get_object_or_404(CategoryTest, pk=category_id, userName=request.user)
    print(category)
    if request.method == 'POST':
        category.delete()
        return redirect('categories')

@login_required
def updateCategory(request, category):    
    return render(request, 'create_category.html')


#groups here



@login_required
def showGroup(request):
    g = GroupMembers.objects.filter(person=request.user)
    members = []
    for x in g:
        xmembers = GroupMembers.objects.filter(group=x.group)
        members.append(xmembers)
    return render (request, 'manage_group.html' , {'groups':g,'members':members})

@login_required
def deleteGroup(request, group_id):
    group = get_object_or_404(GroupUsers, pk=group_id)
    if request.method == 'POST':
        group.delete()
        return redirect('managegroup')

@login_required    
def modifyGroup(request, group_id):
    if request.method == 'GET':
        user= User.objects.get(username=request.user.username)
        group = get_object_or_404(GroupUsers , pk= group_id)
        members = GroupMembers.objects.filter(group=group_id)
        tasks = TaskGroup.objects.filter(group=group_id)
        form = GroupForm(instance=group) 
        return render (request, 'group_detail.html' , {'form':form , 'members':members,
        'tasks':tasks, 'group':group_id, 'cgroup':group, 'user':user})
    else:
        group = get_object_or_404(GroupUsers,pk= group_id)
        form= GroupForm(request.POST, instance=group)
        form.save()
        return redirect('managegroup')

@login_required
def createGroup(request):
    if request.method == 'GET': 
        # form = GroupMembersForm()
        # form.filtmember(request.user) 
                
        return render (request,"create_group.html", {"form": GroupForm})
    else:
        try:
            # listmembers = []
            group = GroupUsers.objects.create(name=request.POST['name'])
            group.save() # guardar los cambios
            
            # tal = request.POST.getlist('members')
            
            # for x in tal:
            #     member= User.objects.get(pk=x)
            #     listmembers.append(member)
            
            xuser = GroupMembers.objects.create(group=group,person=request.user)
            xuser.setCharge('Leader')
            xuser.save() 
            # print(listmembers)
            
            # for nmember in listmembers:
            #     xmember = GroupMembers.objects.create(group=group,person=nmember)
            #     xmember.save()                 
            
            return redirect('managegroup') #Ingresar directorio de seccion grupos
        except Exception as e:
            return render (request,"create_group.html", {"form": GroupForm, "error":e})

@login_required
def addMembers(request,group_id):
    grupo = get_object_or_404(GroupUsers, pk=group_id)
    
    if request.method=="POST":
        try:
            buscar = request.POST.get("find")
                    
            if buscar:
                        
                usuario= User.objects.get(username = buscar )
                print (usuario)
                
                if  usuario is not None:
                    xmember = GroupMembers.objects.create(group=grupo,person=usuario)
                    xmember.save() 
                                    
            return redirect('managegroup')
        except Exception as e:
            return redirect('managegroup')

def deleteGroupTask(request,taskgroup_id):
    taskgroup= TaskGroup.objects.get(pk=taskgroup_id)
    # group = GroupUsers.objects.get(pk=taskgroup.group.id)
    if request.method == "POST":
        taskgroup.delete()
        return redirect('managegroup')
    
@login_required
def createGroupTask(request,group_id):
    if request.method == 'GET':
        return render(request, 'create_group_task.html', {
            'form': TaskGroupForm
        })
    else:
        try:
            group= GroupUsers.objects.get(pk=group_id)
            grouptask= TaskGroup.objects.create(title=request.POST['title'],
                                                description=request.POST['description'],
                                                coment=request.POST['coment'],
                                                group=group)
            grouptask.save()
            return redirect('managegroup')
        except ValueError:
            return render(request, 'create_task.html', {
            'form': TaskForm,
            'error':'Please provide valid data'
        })

@login_required
def task_group_detail(request, taskgroup_id):
    if request.method == 'GET':
        task = get_object_or_404(TaskGroup, pk=taskgroup_id)
        form = TaskGroupForm(instance=task)
        form.onlyComentView() 
        return render(request, 'group_taskdetail.html',{'task':task , 'form':form})
    else:
        try:
            task = get_object_or_404(TaskGroup, pk=taskgroup_id)
            comment = task.coment
            if request.POST['yourcoment'] != '':
                new_comment= f"{comment}\n{request.user.username}: {request.POST['yourcoment']}"
                form= TaskGroupForm(request.POST, instance=task)
                form.save()
                task.coment= new_comment
                task.save()
            elif request.POST['yourcoment'] == '':
                form= TaskGroupForm(request.POST, instance=task)
                form.save()
                task.coment= comment
                task.save()
            return redirect('managegroup')
        except ValueError:
            return render(request, 'usertaskdetail.html',
            {'task':task , 'form':form , 'error': 'Error updating task'})

@login_required
def exitGroup(request,group_id):
    group= GroupUsers.objects.get(pk=group_id)
    member=GroupMembers.objects.get(group=group,person=request.user)
    if request.method == 'POST':
        member.delete()
        return redirect('managegroup')
        

def sendCommentary(request, taskgroup_id):
    task = get_object_or_404(TaskGroup, pk=taskgroup_id)
    if request.method == 'POST':
        comment = task.coment
        if request.POST['yourcoment'] != '':
            new_comment= f"{comment}\n{request.user.username}: {request.POST['yourcoment']}"
            task.coment= new_comment
            task.save()
            return HttpResponseRedirect(request.path_info)
        elif request.POST['yourcoment'] == '':
            task.coment= comment
            task.save()
            return HttpResponseRedirect(request.path_info)
    
# def FindMember(request):
#     buscar = request.GET.get("find")
#     usuario = User.objects.filter(username = True)
#     if buscar:
#         usuario= User.objects.filter(
#             Q(username = buscar)
#         )
#     return render (request,"create_group.html", {"user":usuario})