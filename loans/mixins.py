from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.http import Http404

class InvestorRequiredMixmin(object):
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super(InvestorRequiredMixmin, self).as_view(*args, **kwargs)
        return login_required(view)
    
    @method_decorator(login_required)
    def dispatch(self, request,*args, **kwargs):
        if request.user.is_investor:
            return super(InvestorRequiredMixmin, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404
class BorrowerRequiredMixmin(object):
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super(BorrowerRequiredMixmin, self).as_view(*args, **kwargs)
        return login_required(view)
    
    @method_decorator(login_required)
    def dispatch(self, request,*args, **kwargs):
        if request.user.is_borrower:
            return super(BorrowerRequiredMixmin, self).dispatch(request, *args, **kwargs)
        else:
            raise Http404

class LoginRequiredMixmin(object):
    @classmethod
    def as_view(self, *args, **kwargs):
        view = super(LoginRequiredMixmin, self).as_view(*args, **kwargs)
        return login_required(view)
    
    @method_decorator(login_required)
    def dispatch(self, request,*args, **kwargs):
            return super(LoginRequiredMixmin, self).dispatch(request, *args, **kwargs)