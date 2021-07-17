from account.models import Investor,Borrower
from django.shortcuts import redirect, render, get_object_or_404
from .models import RequestsLoan,Offer,Loan
from .serializers import RequestsLoanSerializers, OfferSerializers, LoanSerializers
from .mixins import *
from django.http.response import Http404, JsonResponse
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework import status, filters, mixins, generics,viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.
class RequestsLoanViewsets(viewsets.ModelViewSet, BorrowerRequiredMixmin):
    queryset = RequestsLoan.objects.all()
    serializer_class = RequestsLoanSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']
    authentication_classes = [TokenAuthentication]

class OfferViewsets(viewsets.ModelViewSet, InvestorRequiredMixmin):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']
    authentication_classes = [TokenAuthentication]

class LoanViewsets(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']
    authentication_classes = [TokenAuthentication]

#1 - list, create
class LoanMixinsCL(BorrowerRequiredMixmin,mixins.ListModelMixin,mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializers
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']  
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        if self.queryset.get(self.queryset.requested_loan == self.queryset.accepted_offer_id.requested_loan):
            return self.create(request, *args, **kwargs)

#2 - retrive, update, destroy
class LoanGenericsRUD(generics.RetrieveUpdateDestroyAPIView ,BorrowerRequiredMixmin):
    lookup_field = 'pk'
    queryset = Loan.objects.all()
    serializer_class = LoanSerializers
    authentication_classes = [TokenAuthentication]
    filter_backends = [filters.SearchFilter]
    search_fields = ['id']   
    
    def get_queryset(self):
        loans = Loan.objects.all()
        pk = self.kwargs.get("pk")
        requested_loans = RequestsLoan.objects.get(pk=pk)
        accepted_offer = Offer.objects.filter(requested_loans=requested_loans)
        return super().get_queryset()
    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)
    # def put(self, request, *args, **kwargs):
    #         if self.queryset.get(self.queryset.requested_loan == self.queryset.accepted_offer_id.requested_loan):
    #             return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)

















#3 function based views
#3.1 GET POST
# @api_view(['GET','POST'])
# def new_loan(request,pk=None):
#     #GET 
#     if request.method == 'GET':
#         loans = Loan.objects.all()
#         serializer = LoanSerializers(loans, many=True)
#         return Response(serializer.data)
#     #POST
#     elif request.method == 'POST':
#         serializer = LoanSerializers(data = request.data)
#         loan = Loan.objects.get(id=pk)
#         if serializer.is_valid():
#                 if Loan.objects.get(loan.accepted_offer.investor.invest_money) >= loan.final_total_amount:
#                     serializer.save()
#                     return Response(serializer.data, status= status.HTTP_201_CREATED)
#                 return Response(serializer.data, status= status.HTTP_400_BAD_REQUEST) 
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def edit_loan(request, pk=None): 
#     try:
#         loan = Loan.objects.get(id=pk)
#     except Loan.DoesNotExist:
#         return Response(status= status.HTTP_404_NOT_FOUND)

#     #GET 
#     if request.method == 'GET':
#         serializer = LoanSerializers(loan)
#         return Response(serializer.data)
#     #PUT
#     elif request.method == 'PUT':
#         serializer = LoanSerializers(loan, data = request.data)
#         if serializer.is_valid():
#             # if Loan.requested_loan.id == Loan.accepted_offer.requested_loan.id:
#             serializer.save()
#                 # return Response(serializer.data, status= status.HTTP_201_CREATED)
#             return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

#     #DELETE 
#     if request.method == 'DELETE':
#         loan.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
# # #7 new loan
# @api_view(['POST'])
# def new_loan(request):
#     # try:
#     requested_loan = RequestsLoan.objects.get(
#         borrower = request.data['borrower'],
#         loan_amount = request.data['loan_amount'],
#         loan_period = request.data['loan_period']

#     )
#     accepted_offer = Offer.objects.get(
#         req     = request.data['requested_loan'],
#         investor = request.data['investor'],
#         annual_rate = request.data['annual_rate']
#     )

#     ## for create new loan with exist guests
#     # except Guest.DoesNotExist:
#     #     raise Http404

#     loan = Loan()
#     loan.requested_loan = requested_loan
#     loan.accepted_offer = accepted_offer
#     loan.status = 0
#     loan.save()

#     serializer = LoanSerializers(loan, data = request.data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status='Funded')
