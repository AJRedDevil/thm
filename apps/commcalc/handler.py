

from django.db.models import Sum
from django.utils import timezone

from .models import Commission
from apps.jobs.models import Jobs


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

    def setCommPaid(self, user):
        """
        Sets commission flag as true for the user
        """
        Commission.objects.filter(
            handyman=user,
            is_paid=False
        ).update(is_paid=True, paidout_date=timezone.now())
        return True

    def getTotalCommUser(self, user):
        """Returns the total commission paid
        """
        commissions=Commission.objects.filter(handyman=user, is_paid=True)
        return "Rs.{:,.2f}".format(commissions.aggregate(Sum('amount'))['amount__sum'])
