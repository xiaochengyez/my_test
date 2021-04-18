import datetime
import json

from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
import requests

from testPlatform.models import UserInfo, ProjectInfo, TestCaseInfo, PictureInfo, InterInfo
from testPlatform.util.common import delete_project, get_ajax_msg


# Create your views here.
from testPlatform.util.mysqlUtil import MysqlUtil

#检查登录
from testPlatform.util.redisUtil import RedisUtil


def login_check(func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('login_status'):
            return HttpResponseRedirect('/')
        return func(request, *args, **kwargs)
    return wrapper

#登录
def login(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        password = request.POST.get('passwd')
        if UserInfo.objects.filter(username__exact=username).filter(password__exact=password).count() == 1:
            request.session['login_status'] = True
            request.session['now_account'] = username
            return HttpResponseRedirect('/index/')
        else:
            request.session['login_status'] = False
            message = {'message': '账号或密码错误'}
            return render(request,'login.html',message)
    elif request.method == 'GET':
        return render(request,'login.html')



#添加项目
@login_check
def add_project(request):
    if request.method == 'POST':
        project_name = request.POST.get('project_name', '')
        project_detail = request.POST.get('project_detail', '')
        project_manager = request.POST.get('project_manager','')
        project_status = request.POST.get('project_status', '')
        project_company = request.POST.get('project_company', '')
        project_process = request.POST.get('project_process','')
        project = ProjectInfo(project_name=project_name,project_detail=project_detail,project_manager=project_manager,
                              project_company=project_company,project_status=project_status,project_process=project_process)
        project.save()
        project_member = request.POST.getlist('project_member','')
        for member in project_member:
            picture = PictureInfo(member=member,belong_project=project)
            picture.save()
        return HttpResponseRedirect('/index/')
    elif request.method == 'GET':
        user = request.session["now_account"]
        return render(request,"project/project-add.html",{'user':user})


#项目详情
@login_check
def detail_project(request,id):
    user = request.session['now_account']
    project = get_object_or_404(ProjectInfo, id=id)
    picture = PictureInfo.objects.filter(belong_project_id=id)
    return render(request, 'project/project-detail.html',{'user':user,'project':project,'picture':picture})

#修改项目
@login_check
def edit_project(request,id):
    if request.method == 'POST':
        project_name = request.POST.get('project_name', '')
        project_detail = request.POST.get('project_detail', '')
        project_manager = request.POST.get('project_manager','')
        project_company = request.POST.get('project_company', '')
        ProjectInfo.objects.filter(id=id).update(project_name=project_name,project_detail=project_detail,project_manager=project_manager,
                              project_company=project_company)
        return HttpResponseRedirect('/index/')
    elif request.method == 'GET':
        user = request.session["now_account"]
        project = get_object_or_404(ProjectInfo, id=id)

        return render(request, "project/project-edit.html", {'project_name': project.project_name,
                                                     'project_detail': project.project_detail,
                                                     'project_manager': project.project_manager,
                                                     'project_status': project.get_project_status_display(),
                                                     'project_company': project.project_company,
                                                     'project_process': project.project_process,
                                                     'id': project.id,
                                                     'user': user})
    return render(request, 'project/project-edit.html')

#项目列表
@login_check
def project(request):
    if request.is_ajax():
        kwargs = json.loads(request.body.decode('utf-8'))
        mode = kwargs.pop('mode')
        id = kwargs.pop('id')
        if mode == 'del':
            msg = delete_project(id)
        return HttpResponse(get_ajax_msg(msg, 'ok'))
    else:
        user = request.session['now_account']
        project_list = ProjectInfo.objects.all()
        picture_list = PictureInfo.objects.all()
        return render(request, 'project/projects.html', {'user': user, 'project_list': project_list ,'picture_list':picture_list})


#项目报告
@login_check
def project_report(request):
    user = request.session['now_account']
    return render(request,'project/project-report.html',{'user':user})

#测试报告
@login_check
def report(request):
    user = request.session['now_account']
    return render(request, 'tester/test_report.html',{'user':user})


#测试用例列表
@login_check
def case(request):
    if request.is_ajax():
        kwargs = json.loads(request.body.decode('utf-8'))
        mode = kwargs.pop('mode')
        id = kwargs.pop('id')
        if mode == 'run':
            msg = run_case(id)
        return HttpResponse(get_ajax_msg(msg, 'ok'))
    else:
        user = request.session['now_account']
        case_list = TestCaseInfo.objects.all()
        return render(request, 'tester/test_case.html', {'user': user, 'case_list': case_list})

#添加用例
@login_check
def add_case(request):
    if request.method == 'POST':
        case_name = request.POST.get('case_name', '')
        case_detail = request.POST.get('case_detail', '')
        case_level = request.POST.get('case_level','')
        project_id = request.POST.get('belong_pro_id','')
        case_type = request.POST.get('case_type','')
        case = TestCaseInfo(case_name=case_name,case_detail=case_detail,case_level=case_level,case_status='2',case_type=case_type,belong_pro_id=project_id)
        case.save()
        return HttpResponseRedirect('/test_case/')
    elif request.method == 'GET':
        user = request.session["now_account"]
        project_list = ProjectInfo.objects.all()
        return render(request,'tester/add_case.html',{'user':user,'project_list':project_list})

#修改用例
@login_check
def edit_case(request,id):
    if request.method == 'POST':
        case_name = request.POST.get('case_name', '')
        case_detail = request.POST.get('case_detail', '')
        case_level = request.POST.get('case_level', '')
        case_type = request.POST.get('case_type', '')
        TestCaseInfo.objects.filter(id=id).update(case_name=case_name, case_detail=case_detail,
                                                 case_level=case_level,
                                                 case_type=case_type)
        return HttpResponseRedirect('/test_case/')
    elif request.method == 'GET':
        user = request.session["now_account"]
        case = get_object_or_404(TestCaseInfo, id=id)
        project = get_object_or_404(ProjectInfo,id=case.belong_pro_id)
        return render(request, "tester/edit_case.html", {'case':case,
                                                             'project': project,
                                                             'id': case.id,
                                                             'user': user})
    return render(request, 'tester/edit_case.html')
#更新用例
@login_check
def update_case(request):
    id = request.GET.get('id','')
    status = request.GET.get('status','')
    res = TestCaseInfo.objects.filter(id=id).update(case_status =status)
    return HttpResponse(res)

#接口

def api_send(method,url,params=None,json=None,**kwargs):
    res = requests.request(method,
                     url=url,
                     params=params,
                     json=json
                     )
    return res


#执行用例

def run_case(request,id):
    # if request.is_ajax():
    #     kwargs = json.loads(request.body.decode('utf-8'))
    #     mode = kwargs.pop('mode')
    #     id = kwargs.pop('id')
    #     if mode == 'del':
    #         msg = delete_project(id)

    inter = InterInfo.objects.filter(id=id)
    url = inter.get().inter_url
    method = inter.get().inter_method
    params = inter.get().inter_params
    headers = inter.get().inter_headers
    if headers== ''or params is None:
        response = '请求头不能为空'
    elif params == ''or params is None:
        response = api_send(method, url,headers=headers)
    else:
        params = json.loads(inter.get().inter_params)
        if method == 'get':
            response = api_send(method,url,params=params,headers=headers)
        elif method == 'post':
            response = api_send(method,url,json=params,headers=headers)
        else:
            response = '方法错误'
    return HttpResponse(get_ajax_msg(response, 'ok'))

#接口列表
@login_check
def interface(request,id=None):
    user = request.session["now_account"]
    if id==None:
        inter_list = InterInfo.objects.all()
        project = ProjectInfo.objects.all()
        case_list = TestCaseInfo.objects.all()
        return render(request, 'tester/test_inerface.html',
                      {'user': user, 'inter_list': inter_list, 'project_list': project,'case_list':case_list})
    else:
        inter_list = InterInfo.objects.filter(belong_case_id=id)
        case = get_object_or_404(TestCaseInfo,id=id).case_name
        case_list = TestCaseInfo.objects.all()
        return render(request, 'tester/test_inerface.html',
                      {'user': user, 'inter_list': inter_list, 'case':case,'case_list':case_list})


#搜索用例
@login_check
def case_search(request,case_name=None):
    user = request.session["now_account"]
    name = request.GET.get('case_name', '')
    if name is None or name != '':
        case_list = TestCaseInfo.objects.filter(case_name=name)
    else:
        case_list = TestCaseInfo.objects.all()
    return render(request, 'tester/test_case.html', {'case_list': case_list, 'user': user})

#新增用例
@login_check
def add_inter(request):
    if request.method == 'POST':
        belong_case_id = request.POST.get('belong_case_id','')
        inter_url = request.POST.get('inter_url','')
        inter_method = request.POST.get('inter_type','')
        inter_param = request.POST.get('inter_param','')
        inter_header = request.POST.get('inter_header','')
        inter = InterInfo(inter_url=inter_url,inter_method=inter_method,inter_params=inter_param,inter_headers=inter_header,belong_case_id=belong_case_id)
        inter.save()
        return HttpResponseRedirect('/test_interface/')
    else:
        return HttpResponseRedirect('/test_interface/')


#测试工具
@login_check
def testTool(request):
    user = request.session["now_account"]
    return render(request,'tester/mailbox.html',{'user':user})

#更新用户
@login_check
def update_user(request):
    mobile = request.GET.get('phone','')
    result = MysqlUtil.execute("update biz_user set mobile = %s,open_id = %s,union_id=%s where mobile = %s",('', '', '', mobile))
    if result == 1:
        return HttpResponse(1)
    else:
        return HttpResponse(0)


#查看限购数量
@login_check
def get_limit_count(request):
    redis = RedisUtil()
    count = redis.get_data('user:buy:count')
    return HttpResponse(count)


#设置限购数量
@login_check
def set_limit_count(request):
    count = request.GET.get('count','')
    redis1 = RedisUtil()
    redis1.set_data('user:buy:count', count)
    result = redis1.get_data('user:buy:count')
    return HttpResponse(result)


# 查看库存数量
@login_check
def get_goods_count(request,date=None):
    station_sn = request.GET.get('station_sn', '')
    sku_id = request.GET.get('sku_id','')
    redis2 = RedisUtil()
    if date==None:
        date = datetime.date.today().strftime('%Y%m%d')
        count =redis2.get_data('{%s}:%s:1:%s:' % (station_sn, date, sku_id))
        return HttpResponse(count)
    else:
        count =redis2.get_data('{%s}:%s:1:%s:' % (station_sn, date, sku_id))
        return HttpResponse(count)


# 设置库存数量
@login_check
def set_goods_count(request):
    station_sn = request.GET.get('station_sn', '')
    sku_id = request.GET.get('sku_id', '')
    count = request.GET.get('goods_count', '')
    redis3 = RedisUtil()
    date = datetime.date.today().strftime('%Y%m%d')
    redis3.set_data('{%s}:%s:1:%s:' % (station_sn, date, sku_id), count)
    new_count = redis3.get_data('{%s}:%s:1:%s:' % (station_sn, date, sku_id))
    return HttpResponse(new_count)


@login_check
def profile(request):
    user = request.session['now_account']
    return render(request,'profile.html',{'user':user})


