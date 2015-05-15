from apps.jobs.models import Jobs
from .models import Commission


class CommissionManager(object):
    """
    Manager for commission calculations
    """
    def getCommUser(self, user):
        """
        Returns commission amount due for the user
        """
        commissions = Commission.objects.filter(
            handyman=user,
            is_paid=False
        )
        comm = 0.0
        for commission in commissions:
            comm += float(commission.amount.amount)
        return [comm, commissions]

    def addCommission(self, job):
        for handyman in job.handyman.all():
            amount = (0.2 * float(job.fee.amount))/job.handyman.count()
            commission = Commission(job=job, amount=amount, handyman=handyman)
            Commission.save(commission)
