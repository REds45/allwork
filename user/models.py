from django.db import models
from taggit.managers import TaggableManager
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin
)
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self,username,email,password,**kwargs):
        """
        创建普通用户
        """
        if not email:
            raise ValueError("Users must hava a vaild email address.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=kwargs.get('first_name'),
            last_name=kwargs.get('last_name')
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self,username,email,password=None,**kwargs):
        '''
        创建超级用户
        '''
        #先创建普通用户
        user=self.create_user(username,email,password,**kwargs)

        user.is_admin = True  # 管理员
        user.is_superuser = True  # 超级用户
        user.is_staff = True  # 职员
        user.save()
        return user

class User(AbstractBaseUser,PermissionsMixin):
    email=models.EmailField(unique=True)#邮箱，唯一属性

    username=models.CharField(max_length=100,unique=True)
    first_name=models.CharField(max_length=100,blank=True,null=True)
    last_name=models.CharField(max_length=100,blank=True,null=True)

    profile_photo = models.ImageField(upload_to='pic_folder',default='pic_folder/default.jpg')
    profile=models.TextField(null=True,blank=True)
    skills=TaggableManager(blank=True)

    is_owner= models.BooleanField('project_owner status',default=False)
    is_freelancer=models.BooleanField('freelancer status',default=False)

    date_created=models.DateTimeField(auto_now_add=True)
    date_modified=models.DateTimeField(auto_now=True)

    is_admin=models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects=UserManager()

    USERNAME_FIELD = 'username'  # 描述用户模型上用作唯一标识符的字段名称的字符串。
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']  # 通过createsuperuser管理命令创建用户时将提示的字段名称列表。

    class Meta:
        verbose_name="user"
        verbose_name_plural="users"

    #获得名字缩写
    def get_short_name(self):
        return self.first_name

    #获得全名
    def get_full_name(self):
        if self.first_name:
            first_name = ' '.join(
                [i.capitalize() for i in self.first_name.split(' ')]
            )
            last_name = ' '.join(
                [i.capitalize() for i in self.last_name.split(' ')
                 if self.last_name]
            )
            full_name = [first_name, last_name]
            full_name = ' '.join(
                [i.strip() for i in full_name if i.strip()]
            )

            return full_name
        else:
            return "%s" % (self.email)


# 此项为收入属性，与后面jobs应用关联，在jobs应用实现前我们将其注释
    # @property
    # def income(self):
    #     """
    #     计算自由职业者的所有完成任务的总收入。
    #     """
    #     completed_jobs = self.job_freelancer.filter(status="ended")
    #
    #     income = 0
    #     for job in completed_jobs:
    #         income += job.price
    #
    #     return income
