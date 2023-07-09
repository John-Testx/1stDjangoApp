from django.contrib import admin
from .models import Task
from .models import CategoryTest,CategoryTestTask
from .models import Xtorage
from .models import GroupUsers , GroupMembers, TaskGroup

class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)

# Register your models here.
admin.site.register(Task, TaskAdmin)
admin.site.register(CategoryTest)
admin.site.register(CategoryTestTask)
admin.site.register(Xtorage)
admin.site.register(GroupUsers)
admin.site.register(GroupMembers)
admin.site.register(TaskGroup)