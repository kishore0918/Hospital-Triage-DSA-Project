# Filename: priority_scorer.py
"""
Priority Scoring Module for Hospital Triage System (Educational Simulation).
NOTE: This scoring algorithm is purely illustrative for demonstrating Priority Queue
and Heap Data Structures in an academic M.Tech DSA project. It is NOT a clinically
validated medical triage tool.
"""

# Predefined symptom severity weights for consistent GUI dropdown selection & testing
SYMPTOM_WEIGHTS = {
    "Unconscious / Unresponsive": 45,
    "Chest Pain / Cardiac Arrest Risk": 40,
    "Severe Trauma / Heavy Bleeding": 38,
    "Stroke Symptoms (FAST)": 38,
    "Severe Breathing Difficulty": 35,
    "High Fever with Chills": 20,
    "Moderate Abdominal Pain": 18,
    "Minor Fracture / Sprain": 12,
    "Mild Fever / Cough / Cold": 5,
    "Routine Checkup / Minor Cut": 2
}


def calculate_priority_score(
    age: int,
    heart_rate: int,
    systolic_bp: int,
    diastolic_bp: int,
    temperature: float,
    spo2: int,
    symptoms: str
) -> tuple[int, str, list[str]]:
    """
    Calculates an educational triage priority score based on vital signs and symptoms.

    Returns:
        tuple: (total_score, priority_category, breakdown_notes)
    """
    score = 0
    breakdown = []

    # 1. Oxygen Saturation (SpO2 %) - Normal: 95% to 100%
    if spo2 < 85:
        score += 50
        breakdown.append(f"SpO2 ({spo2}%): Critical Hypoxia (+50)")
    elif spo2 < 90:
        score += 35
        breakdown.append(f"SpO2 ({spo2}%): Severe Hypoxia (+35)")
    elif spo2 < 95:
        score += 15
        breakdown.append(f"SpO2 ({spo2}%): Mild Hypoxia (+15)")
    else:
        breakdown.append(f"SpO2 ({spo2}%): Normal (+0)")

    # 2. Heart Rate (bpm) - Normal: 60 to 100 bpm
    if heart_rate > 130 or heart_rate < 45:
        score += 30
        breakdown.append(f"Heart Rate ({heart_rate} bpm): Critical Range (+30)")
    elif heart_rate > 110 or heart_rate < 55:
        score += 18
        breakdown.append(f"Heart Rate ({heart_rate} bpm): Abnormal Range (+18)")
    elif heart_rate > 100 or heart_rate < 60:
        score += 8
        breakdown.append(f"Heart Rate ({heart_rate} bpm): Borderline (+8)")
    else:
        breakdown.append(f"Heart Rate ({heart_rate} bpm): Normal (+0)")

    # 3. Blood Pressure (mmHg) - Normal: ~90/60 to 120/80
    if systolic_bp > 180 or systolic_bp < 85 or diastolic_bp > 120 or diastolic_bp < 50:
        score += 30
        breakdown.append(f"BP ({systolic_bp}/{diastolic_bp}): Critical Crisis/Shock (+30)")
    elif systolic_bp > 150 or systolic_bp < 90 or diastolic_bp > 95 or diastolic_bp < 60:
        score += 15
        breakdown.append(f"BP ({systolic_bp}/{diastolic_bp}): Abnormal (+15)")
    elif systolic_bp > 135 or diastolic_bp > 85:
        score += 5
        breakdown.append(f"BP ({systolic_bp}/{diastolic_bp}): Slightly Elevated (+5)")
    else:
        breakdown.append(f"BP ({systolic_bp}/{diastolic_bp}): Normal (+0)")

    # 4. Body Temperature (Celsius) - Normal: 36.1 to 37.5 C
    if temperature > 39.5 or temperature < 35.0:
        score += 20
        breakdown.append(f"Temp ({temperature:.1f}°C): Critical Fever/Hypothermia (+20)")
    elif temperature > 38.0 or temperature < 36.0:
        score += 10
        breakdown.append(f"Temp ({temperature:.1f}°C): Moderate Fever/Low Temp (+10)")
    else:
        breakdown.append(f"Temp ({temperature:.1f}°C): Normal (+0)")

    # 5. Age Vulnerability Factor
    if age >= 65 or age <= 5:
        score += 10
        breakdown.append(f"Age ({age} yrs): High-Vulnerability Group (+10)")
    elif age >= 50:
        score += 5
        breakdown.append(f"Age ({age} yrs): Moderate Age Factor (+5)")
    else:
        breakdown.append(f"Age ({age} yrs): Standard Adult (+0)")

    # 6. Reported Symptoms
    symptom_points = SYMPTOM_WEIGHTS.get(symptoms, 10)
    score += symptom_points
    breakdown.append(f"Symptom ('{symptoms}'): +{symptom_points}")

    # Determine Priority Category based on total score
    if score >= 75:
        category = "Critical"
    elif score >= 50:
        category = "High"
    elif score >= 25:
        category = "Medium"
    else:
        category = "Low"

    return score, category, breakdown


# Self-test block when running this file directly
if __name__ == "__main__":
    print("=== Testing Priority Scorer Module (Educational Simulation) ===")
    
    # Test Case 1: Critical Emergency Patient
    s1, cat1, notes1 = calculate_priority_score(
        age=68, heart_rate=138, systolic_bp=185, diastolic_bp=110,
        temperature=37.2, spo2=86, symptoms="Chest Pain / Cardiac Arrest Risk"
    )
    print(f"\nTest Patient 1 -> Score: {s1} | Category: {cat1}")
    for note in notes1:
        print("  -", note)

    # Test Case 2: Low Priority Patient
    s2, cat2, notes2 = calculate_priority_score(
        age=24, heart_rate=76, systolic_bp=118, diastolic_bp=78,
        temperature=37.0, spo2=98, symptoms="Mild Fever / Cough / Cold"
    )
    print(f"\nTest Patient 2 -> Score: {s2} | Category: {cat2}")
    for note in notes2:
        print("  -", note)