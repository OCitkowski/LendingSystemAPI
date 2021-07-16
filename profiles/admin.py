from django.contrib import admin
from .models import InvestorProfile, BorrowerProfile
# Register your models here.
admin.site.register(InvestorProfile)
admin.site.register(BorrowerProfile)