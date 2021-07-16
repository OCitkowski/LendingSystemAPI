from django.db import models
from account.models import Investor,Borrower
# from profiles.models import InvestorProfile
# Create your models here.

class RequestsLoan(models.Model):
    borrower        = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    loan_amount     = models.IntegerField(null=False, blank=False)
    loan_period     = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f'{self.id} Loan for {self.borrower.user.username} with {self.loan_amount}$ for {self.loan_period} months'


class Offer(models.Model):
    requested_loan  = models.ForeignKey(RequestsLoan, on_delete=models.CASCADE)
    investor        = models.ForeignKey(Investor, on_delete=models.CASCADE)
    annual_rate     = models.DecimalField(max_digits=5, decimal_places=1)

        #to make calculated total amount loan_amount+(loan_amount*)
    def get_total_amount(self):
        loan_am = self.requested_loan.loan_amount
        if  loan_am is not None:
            total_amount = loan_am + (loan_am*(self.annual_rate)/100)
            return total_amount

    total_amount = property(get_total_amount)

    def __str__(self):
        return f"{self.id}- {self.investor.user.username}'s offer"
    
    

class Loan(models.Model):
    request_loan = models.ForeignKey(RequestsLoan, on_delete=models.CASCADE)
    def get_loan_amount(self):
        return self.request_loan.loan_amount
    loan_amount = property(get_loan_amount)

    accepted_offer       = models.ForeignKey(Offer, on_delete=models.CASCADE)
    # total_amount + lenme's fee(3$)
    def get_total_amount(self):
        return (self.offer.total_amount + 3)

    final_total_amount = property(get_total_amount)

    STATUS_DEFAULT  = 0
    STATUS_DEFAULT  = 1
    GENDER_CHOICES  = [(STATUS_DEFAULT, 'founded'), (STATUS_DEFAULT, 'completed')]
    status          = models.IntegerField(choices=GENDER_CHOICES,default = 0)
    created_at      = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.id