from django.shortcuts import render

from .models import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth import logout
from django.shortcuts import redirect





def logout_view(request):
    logout(request)
   
    return redirect('login')  # Replace 'home' with the name of your home URL pattern.

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:  # Check if both username and password are provided
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
            
                return redirect('home')  # Assuming you have a 'success' URL name defined in your urls.py
            else:
               
                messages.error(request, 'Invalid username or password.')
        else:
            # Return an error message if either username or password is missing
            messages.error(request, 'Please provide both username and password.')
    return render(request, 'login.html')  # Assuming you have a login.html template in your templates directory



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            
            # Authenticate the user
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            if new_user is not None:
                login(request, new_user)  # Log in the user
                return redirect('login')  # Redirect to the home page after successful registration
            
    else:
        form = RegistrationForm()
    return render(request, 'reg.html', {'form': form})




from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import HealthRecordForm
from .models import HealthRecord, Patient

def home(request):
    records = HealthRecord.objects.filter(patient=request.user)
    context = {
        'records': records
    }
    return render(request, 'index.html', context)

def ai_doctor(request):
    return render(request, 'doc.html')




def add_health_record(request):
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            health_record = form.save(commit=False)
            health_record.patient = request.user.patient_profile
            health_record.save()
            return redirect('health_record_list')
    else:
        form = HealthRecordForm()
    return render(request, 'add_recod.html', {'form': form})



from django.shortcuts import render
from .models import HealthRecord

def health_records(request):
    records = HealthRecord.objects.filter(patient=request.user)
    return render(request, 'recods.html', {'records': records})


def geo_mapping(request):
    return render(request, 'geo.html')

def medicine(request):
    return render(request, 'medicine.html')


# views.py



    
