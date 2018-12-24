from django.shortcuts import render
from propertydetails.forms import *
from django.http import HttpResponseRedirect
def payonline_base(request):
  form = PropertyDetailsForm()
  if request.method=='POST':
       property_no  = request.POST['property_no']
       
       try:
          data = PropertyNumber.objects.get( property_number = property_no)
          
          dict_val = {'property_no':property_no,
                      'data':data
                      }
          return render(request,'payonline/payonline_base.html',dict_val)
       except:
          
          return HttpResponseRedirect(request.META.get('HTTP_REFERER'))    
  else:
    return render(request,'payonline/payonline_base.html',{'form':form})  
