from sklearn.ensemble import IsolationForest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from .models import HealthRecord

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

def detect_anomalies(records):
    # Extract relevant metrics
    data = [
        [record.heart_rate, record.blood_pressure, record.weight]
        for record in records
    ]

    # Fit isolation forest model
    clf = IsolationForest(contamination=0.1)
    clf.fit(data)

    # Predict anomalies
    anomalies = clf.predict(data)
    
    return anomalies

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from collections import Counter
from .models import HealthRecord

def predict_health_risk(records):
    # Prepare data for prediction
    data = [
        [record.heart_rate, record.blood_pressure, record.weight]
        for record in records
    ]
    labels = [
        1 if record.diseases != 'None' else 0
        for record in records
    ]

    # Count the number of unique classes
    class_counts = Counter(labels)

    # If there is only one class, handle it
    if len(class_counts) < 2:
        return ["Not enough data"], 0.0

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, random_state=42)

    # Train logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Make predictions
    predictions = model.predict(X_test)

    # Evaluate accuracy
    accuracy = accuracy_score(y_test, predictions)

    return predictions, accuracy
