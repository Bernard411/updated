from django.shortcuts import render

from .models import *
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import RegistrationForm
from django.contrib.auth import logout
from django.shortcuts import redirect


def recommend_exercise_and_water(user):

    health_record = HealthRecord.objects.filter(patient=user).latest('record_date')

    recommendations = {
        'exercise_duration': 30,  # Default recommendation
        'water_intake': 2.0  # Default recommendation in liters
    }

    # Adjust recommendations based on health conditions
    if health_record.diseases == 'Hypertension':
        recommendations['exercise_duration'] = 20  # Moderate exercise
        recommendations['water_intake'] = 2.5  # Increased water intake

    if health_record.diseases == 'Diabetes':
        recommendations['exercise_duration'] = 30  # Regular exercise
        recommendations['water_intake'] = 3.0  # Increased water intake

    if health_record.diseases == 'None':
        recommendations['exercise_duration'] = 45  # More intensive exercise
        recommendations['water_intake'] = 2.0  # Standard water intake

    # Further customizations based on other fields like weight, height, temperature, etc.
    if health_record.weight and health_record.height:
        bmi = health_record.weight / ((health_record.height / 100) ** 2)
        if bmi > 25:  # Overweight
            recommendations['exercise_duration'] += 15  # Additional exercise time

    return recommendations

    
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


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
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import HealthRecord, ExerciseTracker
from .forms import HealthRecordForm, ExerciseTrackerForm

def home(request):
    user = request.user
    recommendations = recommend_exercise_and_water(user)
    records = HealthRecord.objects.filter(patient=request.user)
    recods_count = HealthRecord.objects.count()
    context = {
        'records': records,
        'recods_count': recods_count,
        'recommendations': recommendations
    }
    return render(request, 'index.html', context)

def ai_doctor(request):
    return render(request, 'doc.html')


def exercise_tracker_view(request):
    if request.method == 'POST':
        form = ExerciseTrackerForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.user = request.user
            exercise.save()
            return redirect('home')
    else:
        form = ExerciseTrackerForm()
    return render(request, 'exercise_tracker_form.html', {'form': form})


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



def geo_mapping(request):
    return render(request, 'geo.html')


def analyze_health_trend(user):
    # Fetch the last 5 health records of the user
    health_records = HealthRecord.objects.filter(patient=user).order_by('-record_date')[:5]

    if len(health_records) < 5:
        return {"error": "Insufficient data for trend analysis."}

    # Initialize lists to store metrics
    heart_rates = []
    blood_pressures = []
    weights = []

    # Extract relevant metrics and ensure they are numeric
    for record in health_records:
        try:
            heart_rates.append(int(record.heart_rate))
        except (ValueError, TypeError):
            pass

        try:
            blood_pressures.append(int(record.blood_pressure))
        except (ValueError, TypeError):
            pass

        try:
            weights.append(float(record.weight))
        except (ValueError, TypeError):
            pass

    if not heart_rates or not blood_pressures or not weights:
        return {"error": "Insufficient numeric data for trend analysis."}

    # Calculate trends
    heart_rate_trend = "Increasing" if heart_rates[0] > heart_rates[-1] else "Decreasing"
    blood_pressure_trend = "Increasing" if blood_pressures[0] > blood_pressures[-1] else "Decreasing"
    weight_trend = "Increasing" if weights[0] > weights[-1] else "Decreasing"

    # Calculate averages
    avg_heart_rate = sum(heart_rates) / len(heart_rates)
    avg_blood_pressure = sum(blood_pressures) / len(blood_pressures)
    avg_weight = sum(weights) / len(weights)

    # Example output
    trend_analysis = {
        "heart_rate_trend": heart_rate_trend,
        "blood_pressure_trend": blood_pressure_trend,
        "weight_trend": weight_trend,
        "average_heart_rate": round(avg_heart_rate, 2),
        "average_blood_pressure": round(avg_blood_pressure, 2),
        "average_weight": round(avg_weight, 2)
    }

    return trend_analysis




from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import HealthRecord

@login_required
def vision(request):
    user = request.user
    trend_analysis = analyze_health_trend(user)
    
    # Get individual metrics over time for charts
    health_records = HealthRecord.objects.filter(patient=user).order_by('-record_date')[:5]
    dates = [record.record_date.strftime('%Y-%m-%d') for record in health_records]
    heart_rates = [record.heart_rate for record in health_records]
    blood_pressures = [record.blood_pressure for record in health_records]
    weights = [record.weight for record in health_records]

    context = {
        'trend_analysis': trend_analysis,
        'dates': dates,
        'heart_rates': heart_rates,
        'blood_pressures': blood_pressures,
        'weights': weights,
    }
    
    return render(request, 'vision.html', context)






def health_records(request):
    return render(request, 'geo.html')

def medicine(request):
    records = HealthRecord.objects.filter(patient=request.user)
    context = {
        'records': records,
       
    }
    return render(request, 'medicine.html', context)

from django.shortcuts import render, redirect

from .models import HealthRecord
from .forms import HealthRecordForm


def add_health_record(request):
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            health_record = form.save(commit=False)
            health_record.patient = request.user
            health_record.save()
            return redirect('home')
    else:
        form = HealthRecordForm()
    return render(request, 'recods.html', {'form': form})

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import HealthRecord

@login_required
def delete_health_record(request, record_id):
    record = get_object_or_404(HealthRecord, id=record_id, patient=request.user)
    record.delete()
    return redirect('home')


# views.py


