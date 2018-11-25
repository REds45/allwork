from django.contrib import admin
from .models import Job, JobProposal


# Register your models here.
class JobModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Job


class ProposalModelAdmin(admin.ModelAdmin):
    class Meta:
        model = JobProposal


admin.site.register(Job, JobModelAdmin)
admin.site.register(JobProposal, ProposalModelAdmin)
