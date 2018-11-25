from django.db import models
from taggit.managers import TaggableManager


class Job(models.Model):
    owner = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='job_owner')
    freelancer = models.ForeignKey('user.User', null=True, blank=True, on_delete=models.CASCADE,
                                   related_name="job_freelancer")

    job_title = models.CharField(max_length=300)
    job_description = models.TextField()
    price = models.DecimalField(max_digits=8,decimal_places=2)
    tags = TaggableManager()

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    # 任务附件
    document = models.FileField(upload_to='attachements', blank=True, null=True)

    ACTIVE = 'active'
    WORKING = 'working'
    ENDED = 'ended'
    CHOICES = (
        (ACTIVE, 'active'),
        (WORKING, 'working'),
        (ENDED, 'ended'),
    )

    status = models.CharField(max_length=9,choices=CHOICES,default=ACTIVE)

    class Meta:
        verbose_name = 'job'
        verbose_name_plural = 'jobs'
        unique_together = ('owner', 'date_created')

    def __str__(self):
        return "%s - %s - %s"%(
            self.owner.get_full_name(),
            self.freelancer.get_full_name() if self.freelancer else '',
            self.status
        )

    @property
    def freelancers(self):
        # 申请此任务的freelancer
        proposals = self.job_proposal.all()
        return [proposal.freelancer for proposal in proposals]


class JobProposal(models.Model):
    """
    任务申请模型
    """

    job= models.ForeignKey('Job',on_delete=models.CASCADE,related_name="job_proposal")
    freelancer=models.ForeignKey('user.User',on_delete=models.CASCADE,related_name='job_proposal')

    proposal=models.TextField()

    class Meta:
        unique_together=('job','freelancer')



