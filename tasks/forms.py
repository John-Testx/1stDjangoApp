from django import forms
from .models import Task, CategoryTest, CategoryTestTask, GroupUsers, GroupMembers, TaskGroup
from django.contrib.auth.models import User


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important', 'filetask']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control ','placeholder':'write a title'}),
            'description':forms.Textarea(attrs={'class':'form-control ','placeholder':'write a title'})
        }
        
class TaskGroupForm(forms.ModelForm):
    class Meta:
        model = TaskGroup
        fields = ['title','description','coment']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control ','placeholder':'write a title'}),
            'description':forms.Textarea(attrs={'class':'form-control ','placeholder':'write a title'}),
            'coment':forms.Textarea(attrs={'class':'form-control '})
        }
        
    def onlyComentView(self):
        self.fields['coment'].disabled = True
                
class GroupForm(forms.ModelForm):
    class Meta:
        model = GroupUsers
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter name of group'}),
        }   

class GroupMembersForm(forms.ModelForm):
    class Meta:
        model = GroupUsers
        fields = ['members']
        widgets = {
            'members': forms.CheckboxSelectMultiple,
        }
    def filtmember(self, user=None, **kwargs):
        self.fields['members'].queryset = User.objects.all().exclude(pk=user.id)   
        

class CateForm(forms.ModelForm):
    class Meta:
        model = CategoryTest
        fields = ['Name']
        widgets = {
            'Name': forms.TextInput(attrs={'class': 'form-control','placeholder':'Enter name of category'}),
        }
        
class CateTaskForm(forms.ModelForm):
    class Meta:
        model = CategoryTestTask
        fields = ['category','task']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control p-1 mt-1'}),
            'task': forms.Select(attrs={'class': 'form-control p-1 mt-1'}),
        }
    
    def filtx(self, user=None, **kwargs):
        self.fields['category'].queryset = CategoryTest.objects.filter(userName=user)
        self.fields['task'].queryset = Task.objects.filter(user=user)

        