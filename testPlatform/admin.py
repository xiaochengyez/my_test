from django.contrib import admin

# Register your models here.
from testPlatform.models import ProjectInfo, TestCaseInfo, InterInfo

admin.site.register(ProjectInfo)
admin.site.register(TestCaseInfo)
admin.site.register(InterInfo)