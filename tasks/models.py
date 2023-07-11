from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.files.storage import Storage


# Create your models here.

class Xtorage(models.Model):
    upload = models.FileField(upload_to="example/")

def user_directory_path(instance, filename):
    return "example/user_{0}/{1}".format(instance.user.id, filename)

class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default= False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filetask = models.FileField(upload_to= user_directory_path, null=True, blank=True) 
    
    def __str__(self):
        return self.title + " -by: " + self.user.username
    def getTitle(self):
        return self.title
    def getDescription(self):
        return self.description
    def getDateCompleted(self):
        return self.datecompleted
    def getUser(self):
        return self.user
        
class GroupUsers(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, through="GroupMembers")
    
    def __str__(self):
        return self.name
    def getName(self):
        return self.name

class GroupMembers(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(GroupUsers, on_delete=models.CASCADE, related_name='group_members')
    date_joined = models.DateTimeField(auto_now_add=True)
    charge = models.CharField(max_length=64, null=True)
    
    def __str__(self):
        if self.charge == 'Leader':
            return self.person.username + ' is leader of ' + self.group.name
        else:
            return self.person.username + ' belongs to: ' + self.group.name                                   
    def getPerson(self):
        return self.person
    def getGroup(self):
        return self.group
    def getCharge(self):
        return self.charge  
    def setCharge(self, charge):
        self.charge = charge
    
class TaskGroup(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    coment= models.TextField(blank=True)
    group = models.ForeignKey(GroupUsers, on_delete=models.CASCADE, related_name='task_groups')
    
    def __str__(self):
        return self.title + ' by: ' + self.group.name
    def getTitle(self):
        return self.title
    def getDescription(self):
        return self.description
    def getComent(self):
        return self.coment
    
class CategoryTest(models.Model):
    Name = models.CharField(max_length=100)
    userName = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.Name
    def getName(self):
        return self.Name
    def getUserName(self):
        return self.userName
    
class CategoryTestTask(models.Model):
    category = models.ForeignKey(CategoryTest, on_delete=models.CASCADE) # data for category which also contains the user data 
    task = models.ForeignKey(Task, on_delete=models.CASCADE)   # task will be used to be stored by category 
    
    def __str__(self):
        cat= f'{self.category.getName()} | {self.task}' 
        return cat                                     
    def getTask(self):
        return self.task
    def getCategory(self):
        return self.category




# class GroupUsers(models.Model):
#     members = models.ForeignKey(User, on_delete=models.CASCADE)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)

# class UserTask(models.Model):
#     Name = models.CharField(max_length=100)
#     created 
#     finalization_date 
#     category = models.ForeignKey("a")