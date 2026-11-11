# Filename: binary_max_heap.py
"""
Manual Binary Max Heap Implementation for Hospital Triage Priority Queue.
Built from scratch without heapq or PriorityQueue.
Tracks live performance metrics (comparisons, heapify-up/down operations,
restructuring time, execution time) and logs step-by-step tree restructuring.
"""

import time
from typing import Optional, List
from patient import Patient


class BinaryMaxHeap:
    def __init__(self):
        # Dynamic array storing the Complete Binary Tree
        self.heap: List[Patient] = []

        # Cumulative Performance Metrics for Dashboard & Analysis
        self.total_insertions: int = 0
        self.total_extractions: int = 0
        self.heapify_up_count: int = 0
        self.heapify_down_count: int = 0
        self.total_comparisons: int = 0
        self.last_restructure_time_ms: float = 0.0
        self.last_execution_time_ms: float = 0.0
        self.cumulative_execution_time_ms: float = 0.0

        # Step-by-step trace of the most recent heap restructuring operation
        self.last_operation_steps: List[str] = []

    # ------------------------------------------------------------------
    # Index Navigation Helper Methods (0-based Array Representation)
    # ------------------------------------------------------------------
    def _parent(self, index: int) -> int:
        return (index - 1) // 2

    def _left_child(self, index: int) -> int:
        return (2 * index) + 1

    def _right_child(self, index: int) -> int:
        return (2 * index) + 2

    def _swap(self, i: int, j: int) -> None:
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def size(self) -> int:
        return len(self.heap)

    def is_empty(self) -> bool:
        return len(self.heap) == 0

    # ------------------------------------------------------------------
    # Core Heap Operations: Insert, Heapify-Up, Extract-Max, Heapify-Down
    # ------------------------------------------------------------------
    def insert(self, patient: Patient) -> None:
        """
        Inserts a patient into the Binary Max Heap in O(log n) time.
        Places patient at the bottom leaf and performs Heapify-Up.
        """
        start_exec = time.perf_counter()
        self.last_operation_steps = []

        # Step 1: Append patient at the end of the array
        self.heap.append(patient)
        inserted_index = len(self.heap) - 1
        self.total_insertions += 1

        self.last_operation_steps.append(
            f"[INSERT] Added {patient.patient_id} ({patient.name}, Score={patient.priority_score}) "
            f"at leaf index [{inserted_index}]."
        )

        # Step 2: Restore Max-Heap property via Heapify-Up
        start_restructure = time.perf_counter()
        self._heapify_up(inserted_index)
        end_restructure = time.perf_counter()

        end_exec = time.perf_counter()

        self.last_restructure_time_ms = (end_restructure - start_restructure) * 1000.0
        self.last_execution_time_ms = (end_exec - start_exec) * 1000.0
        self.cumulative_execution_time_ms += self.last_execution_time_ms

    def _heapify_up(self, index: int) -> None:
        """
        Bubbles a node upward until its parent has higher priority, or it reaches root (index 0).
        """
        while index > 0:
            parent_idx = self._parent(index)
            current_patient = self.heap[index]
            parent_patient = self.heap[parent_idx]

            self.total_comparisons += 1

            # Compare using Patient.has_higher_priority_than (handles score + arrival tie-breaker)
            if current_patient.has_higher_priority_than(parent_patient):
                self.heapify_up_count += 1
                self.last_operation_steps.append(
                    f"  -> Heapify-Up Swap: [{index}] {current_patient.patient_id} (Score {current_patient.priority_score}) "
                    f"has higher priority than Parent [{parent_idx}] {parent_patient.patient_id} "
                    f"(Score {parent_patient.priority_score}). Swapping nodes."
                )
                self._swap(index, parent_idx)
                index = parent_idx
            else:
                self.last_operation_steps.append(
                    f"  -> Heapify-Up Stop: Parent [{parent_idx}] {parent_patient.patient_id} "
                    f"(Score {parent_patient.priority_score}) >= [{index}] {current_patient.patient_id} "
                    f"(Score {current_patient.priority_score}). Max-Heap property satisfied."
                )
                break

        if index == 0:
            self.last_operation_steps.append(
                f"  -> Node {self.heap[0].patient_id} reached Root [0] (Highest Priority Patient)."
            )

    def extract_max(self) -> Optional[Patient]:
        """
        Removes and returns the highest-priority patient at root [0] in O(log n) time.
        Moves the last leaf to root [0] and performs Heapify-Down.
        """
        if self.is_empty():
            self.last_operation_steps = ["[EXTRACT] Queue is empty. No patient to extract."]
            return None

        start_exec = time.perf_counter()
        self.last_operation_steps = []
        self.total_extractions += 1

        root_patient = self.heap[0]

        # If only one patient is in the heap, pop and return directly
        if len(self.heap) == 1:
            self.heap.pop()
            end_exec = time.perf_counter()
            self.last_restructure_time_ms = 0.0
            self.last_execution_time_ms = (end_exec - start_exec) * 1000.0
            self.cumulative_execution_time_ms += self.last_execution_time_ms
            self.last_operation_steps.append(
                f"[EXTRACT] Removed last remaining patient {root_patient.patient_id} from Root [0]. Queue is now empty."
            )
            return root_patient

        # Move the last element to the root position
        last_patient = self.heap.pop()
        self.heap[0] = last_patient
        self.last_operation_steps.append(
            f"[EXTRACT] Removed Root [0] {root_patient.patient_id} (Score={root_patient.priority_score}). "
            f"Moved last leaf {last_patient.patient_id} (Score={last_patient.priority_score}) to Root [0]."
        )

        # Restore Max-Heap property via Heapify-Down
        start_restructure = time.perf_counter()
        self._heapify_down(0)
        end_restructure = time.perf_counter()

        end_exec = time.perf_counter()

        self.last_restructure_time_ms = (end_restructure - start_restructure) * 1000.0
        self.last_execution_time_ms = (end_exec - start_exec) * 1000.0
        self.cumulative_execution_time_ms += self.last_execution_time_ms

        return root_patient

    def _heapify_down(self, index: int) -> None:
        """
        Sinks a node downward by swapping it with its highest-priority child
        until the Max-Heap property is restored.
        """
        n = len(self.heap)
        while True:
            highest = index
            left = self._left_child(index)
            right = self._right_child(index)

            # Compare with left child
            if left < n:
                self.total_comparisons += 1
                if self.heap[left].has_higher_priority_than(self.heap[highest]):
                    highest = left

            # Compare with right child
            if right < n:
                self.total_comparisons += 1
                if self.heap[right].has_higher_priority_than(self.heap[highest]):
                    highest = right

            # If one of the children has higher priority than current node, swap and continue
            if highest != index:
                self.heapify_down_count += 1
                curr_p = self.heap[index]
                child_p = self.heap[highest]
                self.last_operation_steps.append(
                    f"  -> Heapify-Down Swap: Child [{highest}] {child_p.patient_id} (Score {child_p.priority_score}) "
                    f"has higher priority than [{index}] {curr_p.patient_id} (Score {curr_p.priority_score}). Swapping."
                )
                self._swap(index, highest)
                index = highest
            else:
                self.last_operation_steps.append(
                    f"  -> Heapify-Down Stop: Node [{index}] {self.heap[index].patient_id} "
                    f"(Score {self.heap[index].priority_score}) >= its children. Max-Heap property restored."
                )
                break

    def peek(self) -> Optional[Patient]:
        """Returns the highest priority patient at Root [0] in O(1) time without removing them."""
        if self.is_empty():
            return None
        return self.heap[0]

    def get_all_patients_heap_order(self) -> List[Patient]:
        """Returns a shallow copy of the current underlying heap array (level-order)."""
        return list(self.heap)

    def get_sorted_priority_queue(self) -> List[Patient]:
        """
        Returns all waiting patients ordered strictly from highest priority to lowest
        for readable queue display without modifying the actual heap.
        """
        # Using Python's functools.cmp_to_key with our custom tie-breaking comparator
        from functools import cmp_to_key

        def compare_patients(p1: Patient, p2: Patient) -> int:
            if p1.has_higher_priority_than(p2):
                return -1  # p1 comes first
            elif p2.has_higher_priority_than(p1):
                return 1   # p2 comes first
            return 0

        return sorted(self.heap, key=cmp_to_key(compare_patients))

    def verify_max_heap_property(self) -> bool:
        """
        Diagnostic verification method for testing: checks every parent-child pair
        in the array to verify that the Max-Heap invariant holds 100%.
        """
        n = len(self.heap)
        for i in range(n):
            left = self._left_child(i)
            right = self._right_child(i)
            if left < n and self.heap[left].has_higher_priority_than(self.heap[i]):
                return False
            if right < n and self.heap[right].has_higher_priority_than(self.heap[i]):
                return False
        return True

    def reset(self) -> None:
        """Clears the heap and resets all performance counters."""
        self.heap.clear()
        self.total_insertions = 0
        self.total_extractions = 0
        self.heapify_up_count = 0
        self.heapify_down_count = 0
        self.total_comparisons = 0
        self.last_restructure_time_ms = 0.0
        self.last_execution_time_ms = 0.0
        self.cumulative_execution_time_ms = 0.0
        self.last_operation_steps = ["[RESET] Triage queue and performance counters cleared."]

    @property
    def total_heapify_operations(self) -> int:
        return self.heapify_up_count + self.heapify_down_count


# Self-test block when running this file directly
if __name__ == "__main__":
    print("=== Testing Manual Binary Max Heap Implementation ===")
    heap = BinaryMaxHeap()

    sample_patients = [
        Patient("P101", "Ramesh (Mild)", 30, 78, 120, 80, 37.0, 98, "Mild Fever / Cough / Cold", "09:00:00"),
        Patient("P102", "Suresh (High Fever)", 52, 115, 145, 92, 39.6, 93, "High Fever with Chills", "09:02:00"),
        Patient("P103", "Lakshmi (Cardiac Critical)", 68, 138, 185, 112, 37.2, 84, "Chest Pain / Cardiac Arrest Risk", "09:05:00"),
        Patient("P104", "Meena (Equal Tie w/ Suresh)", 52, 115, 145, 92, 39.6, 93, "High Fever with Chills", "09:08:00"),
    ]

    for p in sample_patients:
        heap.insert(p)
        print(f"\nInserted {p.patient_id} (Score={p.priority_score}):")
        for step in heap.last_operation_steps:
            print(" ", step)
        print("  Max-Heap Property Valid?", heap.verify_max_heap_property())

    print("\n--- Peek Highest Priority Patient ---")
    print("Root [0]:", heap.peek())

    print("\n--- Extracting All Patients in Priority Order ---")
    while not heap.is_empty():
        extracted = heap.extract_max()
        print(f"Extracted -> {extracted.patient_id} ({extracted.name}) | Score: {extracted.priority_score} | Arrived: {extracted.arrival_time}")
        print("  Max-Heap Property Valid?", heap.verify_max_heap_property())