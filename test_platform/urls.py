"""test_platform URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from testPlatform import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login),
    path('index/', views.project),
    path('project/', views.project),
    path('add_project/', views.add_project),
    path('detail_project/<int:id>', views.detail_project),
    path('edit_project/<int:id>', views.edit_project),
    path('project_report/',views.project_report),
    path('test_report/',views.report),
    path('test_case/',views.case),
    path('add_case/',views.add_case),
    path('edit_case/<int:id>', views.edit_case),
    path('test_interface/',views.interface),
    path('test_interface/<int:id>',views.interface),
    path('case_search/',views.case_search),
    path('run_case/<int:id>',views.run_case),
    path('test_tool/',views.testTool),


    path('add_inter/',views.add_inter),
    path('update_link/',views.update_link),
    path('get_limit_count/',views.get_limit_count),
    path('set_limit_count/',views.set_limit_count),
    path('get_goods_count/',views.get_goods_count),
    path('set_goods_count/',views.set_goods_count),

    path('update_case/',views.update_case),
    path('profile/',views.profile)


]
