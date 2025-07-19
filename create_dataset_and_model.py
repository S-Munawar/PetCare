import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import MultiLabelBinarizer, LabelEncoder
import pickle

# --- 1. Define Realistic Vital Sign Ranges and Breeds ---
vital_ranges = {
    "Dog": {"temp": (37.5, 39.2), "hr": (60, 140), "rr": (10, 35)},
    "Cat": {"temp": (38.1, 39.2), "hr": (140, 220), "rr": (20, 30)},
    "Horse": {"temp": (37.2, 38.6), "hr": (28, 44), "rr": (10, 24)}
}
breeds = {
    "Dog": ["Labrador Retriever", "German Shepherd", "Golden Retriever", "Bulldog", "Poodle", "Beagle", "Other"],
    "Cat": ["Domestic Shorthair", "Siamese", "Persian", "Maine Coon", "Bengal", "Sphynx", "Other"],
    "Horse": ["Thoroughbred", "Quarter Horse", "Arabian", "Paint Horse", "Appaloosa", "Morgan", "Other"]
}
symptom_list = [
    'Vomiting', 'Lethargy', 'Coughing', 'Diarrhea', 'Weight Loss',
    'Difficulty Breathing', 'Anxiety', 'Limping', 'Skin Irritation',
    'Loss of Appetite', 'Excessive Thirst', 'Frequent Urination', 'Hair Loss',
    'Swelling', 'Discharge', 'Pale Gums' # Added more symptoms for robustness
]
hydration_options = ["Well Hydrated", "Slightly Dehydrated", "Dehydrated"]
activity_options = ["High", "Moderate", "Low"]
diet_options = ["Balanced", "Needs Improvement", "Poor"]
vaccine_options = ["Up to Date", "Overdue", "Not Vaccinated"]

# --- 2. Generate a Highly Realistic Dataset ---
records = []
NUM_RECORDS = 10000 # Increased dataset size for robustness
for i in range(NUM_RECORDS):
    species = np.random.choice(list(vital_ranges.keys()))
    vitals = vital_ranges[species]

    # More nuanced health status generation
    health_rand = np.random.rand()
    if health_rand < 0.65: # ~65% healthy
        is_healthy_pet = True
        is_at_risk_pet = False
    elif health_rand < 0.90: # ~25% at risk
        is_healthy_pet = False
        is_at_risk_pet = True
    else: # ~10% unhealthy
        is_healthy_pet = False
        is_at_risk_pet = False

    # Generate vitals based on health status
    if is_healthy_pet:
        temp = round(np.random.uniform(vitals["temp"][0], vitals["temp"][1]), 1)
        hr = int(np.random.uniform(vitals["hr"][0], vitals["hr"][1]))
        rr = int(np.random.uniform(vitals["rr"][0], vitals["rr"][1]))
        num_symptoms = np.random.choice([0, 1], p=[0.95, 0.05]) # Very few or no symptoms
        symptoms = ['None'] if num_symptoms == 0 else list(np.random.choice(symptom_list, 1, replace=False))
        vaccination_status = np.random.choice(vaccine_options, p=[0.9, 0.08, 0.02])
        hydration = np.random.choice(hydration_options, p=[0.95, 0.05, 0.0])
        activity_level = np.random.choice(activity_options, p=[0.6, 0.35, 0.05])
        diet = np.random.choice(diet_options, p=[0.9, 0.08, 0.02])
    elif is_at_risk_pet:
        # Vitals slightly outside normal range or at the edge
        temp = round(np.random.uniform(vitals["temp"][0] - 0.5, vitals["temp"][1] + 0.5), 1)
        hr = int(np.random.uniform(vitals["hr"][0] - 20, vitals["hr"][1] + 20))
        rr = int(np.random.uniform(vitals["rr"][0] - 5, vitals["rr"][1] + 5))
        num_symptoms = np.random.randint(1, 3) # 1 or 2 symptoms
        symptoms = list(np.random.choice(symptom_list, num_symptoms, replace=False))
        vaccination_status = np.random.choice(vaccine_options, p=[0.4, 0.5, 0.1])
        hydration = np.random.choice(hydration_options, p=[0.2, 0.7, 0.1])
        activity_level = np.random.choice(activity_options, p=[0.2, 0.6, 0.2])
        diet = np.random.choice(diet_options, p=[0.4, 0.5, 0.1])
    else: # Unhealthy pet
        # Vitals clearly outside normal range, more symptoms
        temp = round(np.random.uniform(vitals["temp"][0] - 1.5, vitals["temp"][1] + 1.5), 1)
        hr = int(np.random.uniform(vitals["hr"][0] - 50, vitals["hr"][1] + 50))
        rr = int(np.random.uniform(vitals["rr"][0] - 10, vitals["rr"][1] + 10))
        num_symptoms = np.random.randint(2, 5) # 2 to 4 symptoms
        symptoms = list(np.random.choice(symptom_list, num_symptoms, replace=False))
        # Ensure critical symptom like Difficulty Breathing for very unhealthy
        if np.random.rand() < 0.3 and 'Difficulty Breathing' not in symptoms:
            symptoms.append('Difficulty Breathing')
        if np.random.rand() < 0.2 and 'Vomiting' not in symptoms:
            symptoms.append('Vomiting')

        vaccination_status = np.random.choice(vaccine_options, p=[0.1, 0.3, 0.6])
        hydration = np.random.choice(hydration_options, p=[0.05, 0.2, 0.75])
        activity_level = np.random.choice(activity_options, p=[0.05, 0.15, 0.8])
        diet = np.random.choice(diet_options, p=[0.1, 0.2, 0.7])


    record = {
        'species': species,
        'breed': np.random.choice(breeds[species]),
        'age': round(np.random.uniform(0.1, 20.0), 2), # Age from ~1 month to 20 years, with 2 decimal places
        'weight': round(np.random.uniform(0.5, 550.0), 2), # Weight can be fractional, for small animals
        'temperature': temp,
        'heart_rate': hr,
        'respiratory_rate': rr,
        'symptoms': symptoms,
        'vaccination_status': vaccination_status,
        'hydration': hydration,
        'activity_level': activity_level,
        'diet': diet
    }
    records.append(record)
df = pd.DataFrame(records)

# --- 3. Determine Health Status Based on Realistic Factors ---
def determine_health_status(row):
    score = 0
    vitals = vital_ranges[row['species']]

    # Vital Sign Deviation
    if not (vitals["temp"][0] <= row['temperature'] <= vitals["temp"][1]): score -= 2
    if not (vitals["hr"][0] <= row['heart_rate'] <= vitals["hr"][1]): score -= 2
    if not (vitals["rr"][0] <= row['respiratory_rate'] <= vitals["rr"][1]): score -= 2

    # Symptom Impact
    if 'None' not in row['symptoms']:
        score -= len(row['symptoms']) * 0.5 # Each symptom has a base penalty
        if 'Difficulty Breathing' in row['symptoms']: score -= 2.5 # High impact
        if 'Vomiting' in row['symptoms']: score -= 1.5
        if 'Diarrhea' in row['symptoms']: score -= 1.5
        if 'Lethargy' in row['symptoms']: score -= 1.5
        if 'Weight Loss' in row['symptoms']: score -= 1.0
        # Add more specific symptom penalties

    # Lifestyle/Care Factors
    if row['vaccination_status'] == 'Overdue': score -= 1.0
    if row['vaccination_status'] == 'Not Vaccinated': score -= 2.0
    if row['hydration'] == 'Slightly Dehydrated': score -= 1.0
    if row['hydration'] == 'Dehydrated': score -= 2.5
    if row['activity_level'] == 'Low': score -= 1.0 # Can be normal for old pets, but generally negative
    if row['diet'] == 'Needs Improvement': score -= 1.0
    if row['diet'] == 'Poor': score -= 2.0

    # Age and Weight consideration (simple example, can be more complex)
    # Very young or very old pets might be slightly more vulnerable
    if row['age'] < 1 or row['age'] > 15: score -= 0.5
    # Extreme weight might be a factor, needs species-specific ranges typically
    # For now, a very general penalty for extreme weights
    if row['weight'] < 1 or row['weight'] > 100: # Adjust bounds based on typical animal sizes
         if row['species'] == 'Dog' and (row['weight'] < 2 or row['weight'] > 80): score -= 0.5
         if row['species'] == 'Cat' and (row['weight'] < 1 or row['weight'] > 15): score -= 0.5
         if row['species'] == 'Horse' and (row['weight'] < 150 or row['weight'] > 600): score -= 0.5


    if score <= -6: return 'Unhealthy' # More severe conditions needed for Unhealthy
    if score <= -2: return 'At Risk'
    return 'Healthy'
df['status'] = df.apply(determine_health_status, axis=1)

# --- 4. Preprocess Data with MultiLabelBinarizer for Symptoms ---
label_cols = ['species', 'breed', 'vaccination_status', 'hydration', 'activity_level', 'diet']
encoders = {col: LabelEncoder() for col in label_cols}
for col in label_cols:
    df[col] = encoders[col].fit_transform(df[col])

mlb = MultiLabelBinarizer()
# FIX: Ensure all symptom list elements are standard Python strings for fitting MLB
symptom_list_str = [str(s) for s in symptom_list] + ['None'] # Convert to str and add 'None'
mlb.fit([symptom_list_str]) # Fit on a list containing the list of all possible symptoms. This ensures all are known.
# Or, more robustly, fit on a flat list of all unique possible symptoms:
# all_possible_symptoms_flat = sorted(list(set(symptom_list + ['None'])))
# mlb.fit([all_possible_symptoms_flat]) # This ensures correct column order and inclusion

# Let's use a simpler and more direct approach for fitting MLB to avoid the warning:
mlb.fit([symptom_list_str]) # This is still the correct way to train MLB with all possible labels

# Ensure that the 'symptoms' column in the DataFrame also contains standard Python strings
# This step is crucial if df['symptoms'] was created using numpy arrays which might yield np.str_
df['symptoms'] = df['symptoms'].apply(lambda x: [str(item) for item in x] if isinstance(x, list) else x)


symptom_encoded = mlb.transform(df['symptoms'])
symptom_df = pd.DataFrame(symptom_encoded, columns=mlb.classes_, index=df.index)
encoders['symptoms'] = mlb

df_processed = pd.concat([df.drop('symptoms', axis=1), symptom_df], axis=1)

# Explicitly convert all column names to standard Python strings.
df_processed.columns = [str(col) for col in df_processed.columns]

# --- 5. Train and Save the Model ---
X = df_processed.drop('status', axis=1)
y = df_processed['status']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
model = RandomForestClassifier(n_estimators=300, random_state=42, class_weight='balanced', n_jobs=-1, max_depth=10, min_samples_leaf=5) # Increased estimators, added max_depth and min_samples_leaf for robustness
model.fit(X_train, y_train)

with open('pet_health_model.pkl', 'wb') as f:
    pickle.dump(model, f)
with open('encoders.pkl', 'wb') as f:
    pickle.dump(encoders, f)

print("Advanced dataset, encoders, and model created successfully!")
print(f"Model Accuracy on Test Data: {model.score(X_test, y_test) * 100:.2f}%")