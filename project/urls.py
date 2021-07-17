"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from account.views import (
    AccountViewsets,
    InvestorViewsets,
    BorrowerViewsets
)
from loans.views import (
    RequestsLoanViewsets,
    OfferViewsets,
    LoanViewsets,
    LoanMixinsCL,
    LoanGenericsRUD,
    # new_loan,
    # edit_loan
)
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
router = DefaultRouter()
router.register('accounts',AccountViewsets)
router.register('investors',InvestorViewsets)
router.register('borrowers',BorrowerViewsets)
router.register('requestloans',RequestsLoanViewsets)
router.register('offers',OfferViewsets)
router.register('loans',LoanViewsets)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')) ,
    # Token authentication
    path('api-token-auth', obtain_auth_token, name="login"),
    #viewsets for all models
    path('rest/viewsets/', include(router.urls)),
#8 fbv new reservation
    # path('rest/loans/',new_loan),
    # path('rest/loans/<int:pk>/', edit_loan),

    path('rest/loans/', LoanMixinsCL.as_view()), 
    path('rest/loans/<int:pk>/', LoanGenericsRUD.as_view()), 
]
