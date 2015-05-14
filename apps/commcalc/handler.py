from apps.jobs.models import Jobs


class CommissionManager(object):
    """
    Manager for commission calculations
    """
    def getCommUser(self, user):
        """
        Returns commission amount due for the user
        """
        jobs = Jobs.objects.filter(
            handyman=user,
            is_paid=True,
            comm_paid=False,
            status='3'
        )
        comm = 0.0
        for job in jobs:
            comm += (0.2 * float(job.fee.amount))/job.handyman.count()
        return comm
