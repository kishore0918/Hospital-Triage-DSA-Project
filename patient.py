# Filename: patient.py
"""
Patient Data Model for Priority-Based Hospital Triage System.
Encapsulates patient attributes, automatic priority score calculation,
and tie-breaking comparison logic (higher score first; if tied, earlier arrival first).
"""

from datetime import datetime
import itertools
from priority_scorer import calculate_priority_score

# Global atomic counter to guarantee strict FIFO tie-breaking even if two patients
# are created within the exact same microsecond during automated benchmarks.
_arrival_counter = itertools.count(1)


class Patient:
    def __init__(
        self,
        patient_id: str,
        name: str,
        age: int,
        heart_rate: int,
        systolic_bp: int,
        diastolic_bp: int,
        temperature: float,
        spo2: int,
        symptoms: str,
        arrival_time: str = None
    ):
        self.patient_id = patient_id.strip()
        self.name = name.strip()
        self.age = int(age)
        self.heart_rate = int(heart_rate)
        self.systolic_bp = int(systolic_bp)
        self.diastolic_bp = int(diastolic_bp)
        self.temperature = float(temperature)
        self.spo2 = int(spo2)
        self.symptoms = symptoms

        # Record arrival timestamp and exact monotonic arrival sequence number
        self.arrival_sequence = next(_arrival_counter)
        if arrival_time is None:
            self.arrival_time = datetime.now().strftime("%H:%M:%S")
        else:
            self.arrival_time = arrival_time

        # Automatically compute Priority Score and Category using priority_scorer module
        self.priority_score, self.priority_category, self.score_breakdown = calculate_priority_score(
            age=self.age,
            heart_rate=self.heart_rate,
            systolic_bp=self.systolic_bp,
            diastolic_bp=self.diastolic_bp,
            temperature=self.temperature,
            spo2=self.spo2,
            symptoms=self.symptoms
        )

    @property
    def blood_pressure_str(self) -> str:
        """Returns formatted systolic/diastolic blood pressure string."""
        return f"{self.systolic_bp}/{self.diastolic_bp}"

    def has_higher_priority_than(self, other: "Patient") -> bool:
        """
        Core DSA Comparison Method used by Binary Max Heap and Leftist Heap.
        Rule 1: Higher priority_score always wins.
        Rule 2 (Tie-Breaker): If priority_score is equal, the patient who arrived EARLIER
                              (smaller arrival_sequence) has higher priority.
        """
        if self.priority_score != other.priority_score:
            return self.priority_score > other.priority_score
        return self.arrival_sequence < other.arrival_sequence

    def __repr__(self) -> str:
        return (
            f"Patient(ID={self.patient_id}, Name='{self.name}', "
            f"Score={self.priority_score} [{self.priority_category}], "
            f"Arrived={self.arrival_time}, Seq=#{self.arrival_sequence})"
        )


# Self-test block when running this file directly
if __name__ == "__main__":
    print("=== Testing Patient Model & Tie-Breaking Logic ===")

    p1 = Patient(
        patient_id="P101", name="Arun Kumar", age=45,
        heart_rate=95, systolic_bp=130, diastolic_bp=85,
        temperature=38.5, spo2=94, symptoms="High Fever with Chills",
        arrival_time="10:00:01"
    )

    p2 = Patient(
        patient_id="P102", name="Divya Nair", age=45,
        heart_rate=95, systolic_bp=130, diastolic_bp=85,
        temperature=38.5, spo2=94, symptoms="High Fever with Chills",
        arrival_time="10:05:30"
    )

    p3 = Patient(
        patient_id="P103", name="Karthik S", age=67,
        heart_rate=135, systolic_bp=185, diastolic_bp=115,
        temperature=37.0, spo2=84, symptoms="Chest Pain / Cardiac Arrest Risk",
        arrival_time="10:10:00"
    )

    print("Created Patient 1:", p1)
    print("Created Patient 2:", p2)
    print("Created Patient 3:", p3)

    print(f"\nDoes P3 (Score {p3.priority_score}) have higher priority than P1 (Score {p1.priority_score})?")
    print("Result:", p3.has_higher_priority_than(p1), "(Expected: True)")

    print(f"\nTie-Breaker Test: P1 and P2 both have Score {p1.priority_score}.")
    print("P1 arrived at 10:00:01 (Seq #1), P2 arrived at 10:05:30 (Seq #2).")
    print("Does P1 have higher priority than P2?", p1.has_higher_priority_than(p2), "(Expected: True)")
    print("Does P2 have higher priority than P1?", p2.has_higher_priority_than(p1), "(Expected: False)")