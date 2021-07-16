from django.db import models
from account.models import Investor, Borrower
from loans.models import RequestsLoan, Offer 
# Create your models here.
class InvestorProfile(models.Model):
    investor        = models.OneToOneField(Investor, on_delete=models.CASCADE)
    # loans           = models.ForeignKey(Loan, on_delete=models.CASCADE)
    your_requests   = models.ForeignKey(RequestsLoan, on_delete=models.CASCADE, null=True,blank=True)
    def __str__(self):
        return self.investor.user.username


class BorrowerProfile(models.Model):
    borrower        = models.OneToOneField(Borrower, on_delete=models.CASCADE)
    # loans           = models.ForeignKey(Loan, on_delete=models.CASCADE)
    offers          = models.ForeignKey(Offer, on_delete=models.CASCADE)
    requests        = models.ForeignKey(RequestsLoan,on_delete=models.CASCADE, null=True,blank=True )
    def __str__(self):
        return self.borrower.user.username
