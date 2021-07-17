from django.db.models.signals import post_save
from django.db import models
from account.models import Investor,Borrower
from django.core.validators import MaxValueValidator, MinValueValidator

# from profiles.models import InvestorProfile
# Create your models here.
class RequestsLoan(models.Model):
    # id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    borrower        = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    loan_amount     = models.IntegerField(validators=[MinValueValidator(50),MaxValueValidator(5000)])
    loan_period     = models.IntegerField(validators=[MinValueValidator(1)])
    # def offers(self):
    #     offer = Offer.objects.filter(requested_loan=self)
    #     return str(offer)
    def __str__(self):
        return f'id={str(self.id)}, Loan for {self.borrower.user.username} with {self.loan_amount}$ for {self.loan_period} months'
 

class Offer(models.Model):
    # id  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    requested_loan  = models.ForeignKey(RequestsLoan,related_name='offers', on_delete=models.CASCADE)
    investor        = models.ForeignKey(Investor, on_delete=models.CASCADE)
    annual_rate     = models.DecimalField(max_digits=3, decimal_places=1)

        #to make calculated total amount loan_amount+(loan_amount*)
    def get_total_amount(self):
        loan_am = self.requested_loan.loan_amount
        if  loan_am is not None:
            total_amount = loan_am + (loan_am*(self.annual_rate)/100)
            return total_amount

    total_amount = property(get_total_amount)

    def __str__(self):
        return f"id={str(self.id)}, {self.investor.user.username}'s offer for {self.requested_loan.borrower.user}'s loan request"

    #to make unique offer -> investor can submit one offer for requested_loan
    class Meta:
        unique_together = (('investor', 'requested_loan'),)
        index_together = (('investor', 'requested_loan'),)
    
STATUS_CHOICES  = [(0,'founded'), (1,'completed')]

from datetime import datetime,timedelta
class Loan(models.Model):
    # uuid  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   
    requested_loan  = models.ForeignKey(RequestsLoan, on_delete=models.CASCADE)
    accepted_offer  = models.ForeignKey(Offer, on_delete=models.CASCADE)
    status  = models.IntegerField(choices=STATUS_CHOICES,default = 'founded')
    created_at  = models.DateTimeField(auto_now_add=True)
    # ended_at    = models.DateTimeField(default=datetime.now() + timedelta(days=1))
    def get_loan_amount(self):
        return self.requested_loan.loan_amount
    loan_amount     = property(get_loan_amount)

    # total_amount + lenme's fee(3$)
    def get_total_amount(self):
        return (self.accepted_offer.total_amount + 3)
    final_total_amount  = property(get_total_amount)

    def __str__(self):
        return str(self.id)
    
    def inv(self):
        if self.accepted_offer.investor.invest_money >= self.final_total_amount:
            return True
        
    #to make unique loan -> loan have unique requested_loan and accepted_offer
    class Meta:
        unique_together = ('requested_loan', 'accepted_offer')
        index_together = ('requested_loan', 'accepted_offer')

# def loan_post_saved_receiver(sender, instance,created, *args, **kwargs):
#     product = instance
#     loan = Loan.loan_set.get()
#     if variations.count() == 0:
#         new_var = Variation()
#         new_var.product = product
#         new_var.title = "Default"
#         new_var.price = product.price
#         new_var.save()

# post_save.connect(product_post_saved_receiver, sender=Product)
