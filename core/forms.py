# forms.py
from django import forms
from .models import HealthRecord




from django import forms
from .models import Patient, HealthRecord

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['age', 'medical_history']

class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        fields = [
            'record_date', 'description', 'blood_pressure', 'heart_rate',
            'temperature', 'weight', 'height', 'notes', 'blood_group',
            'diseases', 'surgery_history'
        ]




from django import forms
from .models import ExerciseTracker

class ExerciseTrackerForm(forms.ModelForm):
    class Meta:
        model = ExerciseTracker
        fields = ['exercise_date', 'exercise_type', 'duration_minutes']
        widgets = {
            'exercise_date': forms.DateInput(attrs={'type': 'date'}),
        }





from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Patient

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=False)
    medical_history = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'age', 'medical_history']

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            age = self.cleaned_data.get('age')
            medical_history = self.cleaned_data.get('medical_history')
            Patient.objects.create(user=user, age=age, medical_history=medical_history)
        return user