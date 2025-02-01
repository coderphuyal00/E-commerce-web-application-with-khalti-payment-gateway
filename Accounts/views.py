from django.shortcuts import render,redirect
from .models import User
from django.views.generic import TemplateView,UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserDetailsUpdateForm
# Create your views here.
class UserProfile(LoginRequiredMixin,TemplateView):
    template_name='account/user_details.html'
    context_object_name='user'
    
    def get_user(self):
        return self.request.user
    
def updateUserDetails(request):
    if request.method=='POST':
        form=UserDetailsUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user-details')
    else:
        form=UserDetailsUpdateForm(instance=request.user)
    return render(request,'account/edit_user_details.html',{'form':form})
        