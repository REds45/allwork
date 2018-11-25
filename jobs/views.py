from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, ListView,
    DetailView, RedirectView,
)
from jobs.models import Job, JobProposal
from user.models import User
from direct_messages.services import MessagingService
from direct_messages.models import ChatRoom

# Create your views here.


class JobListView(ListView):
    """
    任务列表
    """
    model = Job
    ordering = 'job_title'
    context_object_name = 'jobs'
    template_name = 'jobs/job_list.html'
    queryset = Job.objects.all()


@method_decorator([login_required], name='dispatch')
class JobCreateView(CreateView):
    """
    创建任务
    """
    model = Job
    fields = ('job_title', 'job_description', 'price', 'tags', 'document')
    template_name = 'jobs/job_add_form.html'

    def form_valid(self, form):
        job = form.save(commit=False)
        job.owner = self.request.user

        job.save()
        form.save_m2m()
        return redirect('jobs:job_detail', job.pk)


@method_decorator([login_required], name='dispatch')
class JobDetailView(DetailView):
    """
    任务详细信息
    """
    model = Job
    template_name = 'jobs/job_detail.html'
    context_object_name = 'job'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_id = self.kwargs.get('pk')
        job = Job.objects.get(pk=job_id)
        if job.owner != self.request.user and self.request.user in job.freelancers:
            context['current_proposal'] = JobProposal.objects.get(
                job__pk=job_id,
                freelancer=self.request.user
            )
        return context


@method_decorator([login_required], name='dispatch')
class JobApplyView(CreateView):
    """
    任务申请
    """
    model = JobProposal
    fields = ('proposal',)
    template_name = 'jobs/job_apply_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['jobs'] = Job.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        proposal = form.save(commit=False)
        proposal.job = Job.objects.get(pk=self.kwargs.get('pk'))
        proposal.freelancer = self.request.user

        proposal.save()
        return redirect('user:job_profile', self. request.user.username)


@method_decorator([login_required], name='dispatch')
class ProposalAcceptView(RedirectView):
    """

    """
    permanent = False
    query_string = True
    pattern_name = 'jobs:job_detail'

    def get_redirect_url(self, *args, **kwargs):
        job = get_object_or_404(Job, pk=kwargs['pk'])
        job.freelancer = User.objects.get(username=kwargs.get('username'))
        job.status = 'working'
        job.save()

        return super().get_redirect_url(*args,pk=kwargs['pk'])


@method_decorator([login_required], name='dispatch')
class JobCloseView(RedirectView):
    """
    关闭任务
    """
    permanent = False
    pattern_name = 'home'

    def get_redirect_url(self, *args, **kwargs):
        job = get_object_or_404(Job, pk=kwargs['pk'])
        job.status = 'ended'
        job.save()

        return super().get_redirect_url(*args)


class ProposalAcceptView(RedirectView):

    permanent = False
    query_string = True
    pattern_name = 'jobs:job_detail'

    def get_redirect_url(self, *args, **kwargs):
        job = get_object_or_404(Job,pk=kwargs['pk'])
        job.freelancer = User.objects.get(username=kwargs.get('username'))
        job.status = 'working'
        job.save()

        is_chatroom = False
        try:
            chatromm = ChatRoom.objects.get(sender=self.request.user, recipient=job.freelancer)
            is_chatroom = True

        except:
            pass

        if not is_chatroom:
            try:
                chatromm = ChatRoom.objects.create(sender=self.request.user, recipient=job.freelancer)

            except:
                pass

        if not is_chatroom:
            chatromm = ChatRoom.objects.create(sender=self.request.user, recipient=job.freelancer)

        MessagingService().send_messages(
            sender=self.request.user,
            recipient=job.freelancer,
            message='''
            Hi {username},

            Your proposal is accepted.

            project details : <a href='{url}'>{job}</a>
            '''.format(username=job.freelancer.username,
                       url=reverse("jobs:job_detail", kwargs={"pk": job.pk}),
                       job=job.job_title)
        )
        messages.success(
            self.request, 'User : {} is assiged to your project'.format(kwargs.get('username')))

        return super().get_redirect_url(*args,pk=kwargs['pk'])








