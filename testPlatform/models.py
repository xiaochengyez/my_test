from django.db import models

# Create your models here.

class BaseTable(models.Model):
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)
    class Meta:
        abstract = True
        verbose_name = '公共字段表'
        db_table = 'BaseTable'

class ProjectInfo(BaseTable):
    status_choices = (
        ('1', '正在进行'),
        ('0', '取消'),
        ('2','已完成')
    )
    project_name = models.CharField('项目名称',max_length=20,null=False)
    project_detail = models.CharField('项目描述',max_length=50)
    project_manager = models.CharField('项目负责人',max_length=50,null=False)
    project_status = models.CharField('状态',choices=status_choices,max_length=20,default='1')
    project_process = models.CharField('项目进度',max_length=3,default=0)
    project_company = models.CharField('所属公司',max_length=20)

    def get_count(self):
        cases = TestCaseInfo.objects.filter(belong_pro_id=self.id)
        sum = 0
        for case in cases:
            inter_count = InterInfo.objects.filter(belong_case_id=case.id).count()
            sum += inter_count
        return sum

    def __str__(self):
        return self.project_name

    class Meta:
        verbose_name = '项目信息'
        db_table = 'ProjectInfo'

class TestCaseInfo(BaseTable):
    status_choices = (
        ('1', '成功'),
        ('0', '失败'),
        ('2','未运行')
    )

    level_choices = (
        ('0', 'P0'),
        ('1', 'P1'),
        ('2','P2')
    )

    type_choices = (
        ('0', '功能'),
        ('1', '性能'),
        ('2','安全'),
        ('3','稳定')
    )
    case_name = models.CharField('用例名称',max_length=20,null=False)
    case_detail = models.CharField('用例描述',max_length=50)
    case_level = models.CharField('用例级别',choices=level_choices,max_length=20,default='1')
    case_status = models.CharField('状态',choices=status_choices,max_length=20,default='1')
    case_type = models.CharField('用例类型',choices=type_choices,max_length=20,default=0)
    belong_pro = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    def __str__(self):
        return self.case_name

    class Meta:
        verbose_name = '用例信息'
        db_table = 'TestCaseInfo'

class InterInfo(BaseTable):

    inter_url = models.CharField('接口url',max_length=100,null=False)
    inter_method = models.CharField('接口类型',max_length=5,null=False)
    inter_headers = models.TextField('接口头信息',max_length=200)
    inter_params = models.TextField('接口参数',max_length=200)
    belong_case = models.ForeignKey(TestCaseInfo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = '接口信息'
        db_table = 'InterInfo'

class UserInfo(BaseTable):
    username = models.CharField('邮箱名',max_length=30,unique=True,null=False)
    password = models.CharField('密码',max_length=20,null=False)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户信息'
        db_table = 'UserInfo'


class PictureInfo(BaseTable):
    belong_project = models.ForeignKey(ProjectInfo, on_delete=models.CASCADE)
    member = models.CharField('项目成员', max_length=50, null=False)
    class Meta:
        verbose_name = '图片地址'
        db_table = 'PictureInfo'

