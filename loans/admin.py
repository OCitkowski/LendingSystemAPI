from django.contrib import admin
from .models import RequestsLoan, Offer, Loan
# Register your models here.

admin.site.register(RequestsLoan)

class OfferAdmin(admin.ModelAdmin):
    readonly_fields = ['total_amount',]
admin.site.register(Offer,OfferAdmin)

class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ['loan_amount','final_total_amount']
admin.site.register(Loan,LoanAdmin)