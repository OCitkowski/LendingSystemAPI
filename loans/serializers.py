from rest_framework import serializers
from rest_framework.fields import ChoiceField
from .models import RequestsLoan,Offer, Loan, STATUS_CHOICES
# class ChoiceField(serializers.ChoiceField):

#     def to_representation(self, obj):
#         if obj == '' and self.allow_blank:
#             return obj
#         return self._choices[obj]

#     def to_internal_value(self, data):
#         # To support inserts with the value
#         if data == '' and self.allow_blank:
#             return ''

#         for key, val in self._choices.items():
#             if val == data:
#                 return key
#         self.fail('invalid_choice', input=data)
# # 
class OfferSerializers(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields=['id','requested_loan','investor','annual_rate']

class RequestsLoanSerializers(serializers.ModelSerializer):
    offers = serializers.HyperlinkedRelatedField(
        many=True,read_only=True,view_name='offer-detail')
    class Meta:
        model = RequestsLoan
        fields=[
            'id',
            'borrower',
            'loan_amount',
            'loan_period',
            'offers'
            ]


class LoanSerializers(serializers.ModelSerializer):

    status = serializers.ChoiceField(choices=STATUS_CHOICES,default = 0)
    class Meta:
        model = Loan
        fields=['id','requested_loan','accepted_offer','status']