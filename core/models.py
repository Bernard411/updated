from django.db import models
from django.contrib.auth.models import User

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)

    @property
    def health_recommendations(self):
        if self.age is None:
            return "Age not provided. Unable to give recommendations."

        recommendations = {
            'sleep': '',
            'exercise': '',
            'diet': ''
        }

        if 1 <= self.age <= 12:
            recommendations['sleep'] = "9-12 hours"
            recommendations['exercise'] = "60 minutes of physical activity per day"
            recommendations['diet'] = "Balanced diet with adequate fruits, vegetables, protein, and dairy"
        elif 13 <= self.age <= 18:
            recommendations['sleep'] = "8-10 hours"
            recommendations['exercise'] = "60 minutes of moderate to vigorous physical activity per day"
            recommendations['diet'] = "Balanced diet, rich in calcium and iron"
        elif 19 <= self.age <= 64:
            recommendations['sleep'] = "7-9 hours"
            recommendations['exercise'] = "150 minutes of moderate aerobic activity or 75 minutes of vigorous activity per week, plus muscle-strengthening activities on 2 or more days per week"
            recommendations['diet'] = "Balanced diet with appropriate caloric intake based on activity level"
        elif self.age >= 65:
            recommendations['sleep'] = "7-8 hours"
            recommendations['exercise'] = "Same as adults, with a focus on balance and flexibility exercises to prevent falls"
            recommendations['diet'] = "Nutrient-dense diet, paying attention to calcium, vitamin D, fiber, and hydration"
        else:
            return "Age out of expected range. Unable to give recommendations."

        return recommendations

class HealthRecord(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    DISEASE_CHOICES = [
        ('None', 'None'),
        ('HIV', 'HIV'),
        ('COVID', 'COVID'),
        ('Diabetes', 'Diabetes'),
        ('Hypertension', 'Hypertension'),
        ('Cancer', 'Cancer'),
        # Add more diseases as necessary
    ]

    SURGERY_CHOICES = [
        ('None', 'None'),
        ('Appendectomy', 'Appendectomy'),
        ('Cardiac Surgery', 'Cardiac Surgery'),
        ('Orthopedic Surgery', 'Orthopedic Surgery'),
        ('Neurosurgery', 'Neurosurgery'),
        # Add more surgeries as necessary
    ]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_records')
    record_date = models.DateField()
    description = models.TextField()
    blood_pressure = models.CharField(max_length=10, blank=True, null=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, blank=True, null=True)
    diseases = models.CharField(max_length=20, choices=DISEASE_CHOICES, default='None')
    surgery_history = models.CharField(max_length=50, choices=SURGERY_CHOICES, default='None')

    def __str__(self):
        return f"Health Record for {self.patient} on {self.record_date}"

class Medicine(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medicines')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Medicine {self.name} for {self.patient}"



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10)
    height = models.FloatField()
    weight = models.FloatField()

    def __str__(self):
        return self.user.username

class Device(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    device_type = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    device_id = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.device_type} ({self.device_id})"

class HealthData(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    heart_rate = models.IntegerField()
    steps = models.IntegerField()
    calories_burned = models.FloatField()
    sleep_duration = models.FloatField()
    activity_level = models.CharField(max_length=50)

    def __str__(self):
        return f"HealthData for {self.user.username} at {self.timestamp}"

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    alert_type = models.CharField(max_length=50)
    message = models.TextField()
    resolved = models.BooleanField(default=False)

    def __str__(self):
        return f"Alert for {self.user.username} at {self.timestamp}"

class MLModel(models.Model):
    model_name = models.CharField(max_length=100)
    description = models.TextField()
    accuracy = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.model_name


from django.db import models
from django.contrib.auth.models import User

class ExerciseTracker(models.Model):
    EXERCISE_TYPE_CHOICES = [
        ('Cardio', 'Cardio'),
        ('Strength Training', 'Strength Training'),
        ('Flexibility', 'Flexibility'),
        ('Balance', 'Balance'),
        # Add more types as necessary
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercise_tracker')
    exercise_date = models.DateField()
    exercise_type = models.CharField(max_length=20, choices=EXERCISE_TYPE_CHOICES)
    duration_minutes = models.PositiveIntegerField()  # Duration in minutes
    calories_burned = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"Exercise on {self.exercise_date} for {self.user}"
