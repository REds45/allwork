from django.shortcuts import render,redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login
from django.views.generic import (
    TemplateView, UpdateView,
    CreateView, ListView,
)

from .models import User
from .forms import FreelancerSignUpForm,OwnerSignUpForm
# Create your views here.


class SignUpView(TemplateView):
    template_name = "users/signup.html"


class UserDetailView(TemplateView):
    '''
    展示个人信息
    '''
    model=User
    template_name = 'users/user_profile.html'

    def get_context_data(self,**kwargs):
        context=super(UserDetailView,self).get_context_data(**kwargs)
        username=self.kwargs.get('username')
        context['profile']=User.objects.get(username=username)
        return context


class UpdateProfileView(UpdateView):
    '''
    更新个人信息
    '''
    model = User
    fields = ['profile_photo', 'first_name', 'last_name', 'profile', 'skills']
    template_name = "users/user_profile_update.html"

    def form_valid(self,form):
        user=form.save(commit=False)
        user.save()
        form.save_m2m()
        messages.success(self.request ,"更新成功")
        return redirect('user:user_profile', self.object.username)

    def get_success_url(self):
        return reverse('user:user_profile',kwargs={'username': self.object.username})


class ListFreelancersView(ListView):
    """
    自由职业者列表
    """
    model = User
    context_object_name = 'freelancers'
    template_name = 'users/freelancer_list.html'

    def get_queryset(self):
        return User.objects.filter(is_freelancer=True)


class FreelancerSignUpView(CreateView):
    '''
    注册为自由职业
    '''
    model = User
    form_class = FreelancerSignUpForm
    template_name = 'users/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = "freelancer"
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user=form.save()
        login(self.request, user)
        return redirect('home')


class OwnerSignUpView(CreateView):
    '''
        注册为Owner
    '''
    model = User
    form_class = OwnerSignUpForm
    template_name = 'users/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'owner'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user=form.save()
        login(self.request, user)
        return redirect('home')


class UserJobProfile(TemplateView):
    """

    """
    model = User
    template_name = 'users/user_job_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['user']=User.objects.get(username=username)
        return context

