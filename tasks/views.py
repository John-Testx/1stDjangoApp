from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import TaskForm,CateForm, CateTaskForm
from .models import Task , CategoryTest, CategoryTestTask 
from django.utils import timezone 
from django.contrib.auth.decorators import login_required


# Create your views here.

def home(request):
    return render(request, 'home.html')

def deleteCategory(request, cate_id):
    category = get_object_or_404(CategoryTest, pk=cate_id, userName=request.user)
    if request.method == 'POST':
        category.delete()
        return redirect('usertask')

def updateCategory(request, category):    
    return render(request, 'create_category.html')

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
            return redirect('usertask')
        except ValueError:
            return render(request, 'create_category.html',{
            'form': CateForm,
            'error':'Please provide valid data'
        })
            
@login_required        
def category(request):
    cate = CategoryTest.objects.filter(userName=request.user).order_by('Name')
    return render(request, 'category.html',
    {'cate': cate})
    
# def categoriesavailable(request):   no la utilizare todavía, no funciona 
#     cate = CategoryTest.objects.filter(userName=request.user).order_by('Name')
#     return render(request, 'usertask.html',
#     {'cate': cate})

@login_required
def createGroup(request):
    return render(request, 'creategroup.html')


@login_required
def category_in_task(request):
    if request.method == 'GET':
        x = CateTaskForm()
        x.filtx(request.user)
        return render(request, 'taskscate.html',{
            'form':x }
        )
    else:
        try:
            form = CateTaskForm(request.POST)
            save_cate = form.save(commit=False)
            save_cate.save()
            print(save_cate)
            return redirect('usertask')
        except ValueError:
            task = Task.objects.filter(user=request.user)
            cate = CategoryTest.objects.filter(userName=request.user)
            return render(request, 'taskscate.html',{
            'form': CateForm,
            'error':'Please provide valid data',
            'task':task,
            'cate':cate
        })

# task inside category
    # task = Task.objects.filter(user=request.user)
    # cate = CategoryTest.objects.filter(userName=request.user)
    # task = get_object_or_404(Task, pk=request.POST['task2'] ,user= request.user)
    # categ= get_object_or_404(CategoryTest, pk=request.POST['category2'] ,userName= request.user)          
    # xs = CategoryTestTask()
    # xs.task = task
    # xs.category = categ
    # xs.save()
# task inside category end