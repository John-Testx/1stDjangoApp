from django import forms
from .models import Task, CategoryTest, CategoryTestTask
from django.contrib.auth.models import Group


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title','description','important', 'filetask']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control ','placeholder':'write a title'}),
            'description':forms.Textarea(attrs={'class':'form-control ','placeholder':'write a title'})
        }
        
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']   
    
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
    
    def filtx(self, user=None, **kwargs):
        self.fields['category'].queryset = CategoryTest.objects.filter(userName=user)
        self.fields['task'].queryset = Task.objects.filter(user=user)

class groupfornothing(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name','permissions']
        