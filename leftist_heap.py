# Filename: leftist_heap.py
"""
Manual Leftist Max Heap Implementation for Hospital Triage System.
Demonstrates Node structure, Null Path Length (NPL), and O(log n) Merge operation
for combining two separate emergency triage queues (e.g., Main ER + Ambulance Queue).
"""

from typing import Optional, List
from patient import Patient


class LeftistNode:
    """Node structure for a Leftist Max Heap."""
    def __init__(self, patient: Patient):
        self.patient: Patient = patient
        self.left: Optional["LeftistNode"] = None
        self.right: Optional["LeftistNode"] = None
        # Null Path Length (NPL): length of the shortest path from this node
        # to a node without two children (a null pointer). Leaf nodes have NPL = 0.
        self.npl: int = 0


class LeftistMaxHeap:
    def __init__(self):
        self.root: Optional[LeftistNode] = None
        self.count: int = 0
        self.merge_steps_log: List[str] = []

    def is_empty(self) -> bool:
        return self.root is None

    def size(self) -> int:
        return self.count

    def _get_npl(self, node: Optional[LeftistNode]) -> int:
        """Returns -1 for None (empty child pointer), or the node's stored NPL."""
        if node is None:
            return -1
        return node.npl

    def merge_roots(self, h1: Optional[LeftistNode], h2: Optional[LeftistNode]) -> Optional[LeftistNode]:
        """
        Core O(log n) Leftist Heap Merge Operation.
        Recursively merges along the short right spines and swaps left/right children
        whenever NPL(left) < NPL(right) to maintain the Leftist property.
        """
        if h1 is None:
            return h2
        if h2 is None:
            return h1

        # Ensure h1 has the higher priority root; if h2 has higher priority, swap h1 and h2
        if h2.patient.has_higher_priority_than(h1.patient):
            h1, h2 = h2, h1

        # Recursively merge h1's right subtree with h2
        h1.right = self.merge_roots(h1.right, h2)

        # Enforce Leftist Property: NPL(left) must be >= NPL(right)
        if self._get_npl(h1.left) < self._get_npl(h1.right):
            h1.left, h1.right = h1.right, h1.left
            self.merge_steps_log.append(
                f"  -> Leftist Swap at Node {h1.patient.patient_id} (Score {h1.patient.priority_score}): "
                f"Swapped children to keep NPL(left) >= NPL(right)."
            )

        # Update Null Path Length: NPL = 1 + NPL(right child)
        h1.npl = self._get_npl(h1.right) + 1
        return h1

    def merge_with(self, other_heap: "LeftistMaxHeap") -> None:
        """Merges another LeftistMaxHeap into this heap in O(log n) time."""
        self.merge_steps_log = [
            f"[LEFTIST MERGE] Merging Primary Heap (size={self.count}) with Secondary Heap (size={other_heap.count})..."
        ]
        self.root = self.merge_roots(self.root, other_heap.root)
        self.count += other_heap.count
        other_heap.root = None
        other_heap.count = 0
        if self.root:
            self.merge_steps_log.append(
                f"[LEFTIST MERGE COMPLETE] New Root is {self.root.patient.patient_id} "
                f"(Score={self.root.patient.priority_score}, Root NPL={self.root.npl}). Total Size={self.count}."
            )

    def insert(self, patient: Patient) -> None:
        """Inserts a new patient by creating a 1-node Leftist Heap and merging in O(log n) time."""
        new_node = LeftistNode(patient)
        self.root = self.merge_roots(self.root, new_node)
        self.count += 1

    def peek(self) -> Optional[Patient]:
        """Returns the highest-priority patient at the root in O(1) time."""
        if self.root is None:
            return None
        return self.root.patient

    def extract_max(self) -> Optional[Patient]:
        """
        Extracts the root patient and merges its left and right subtrees in O(log n) time.
        """
        if self.root is None:
            return None

        max_patient = self.root.patient
        self.root = self.merge_roots(self.root.left, self.root.right)
        self.count -= 1
        return max_patient

    def get_preorder_nodes_with_npl(self) -> List[str]:
        """Returns a formatted list of nodes and their NPL values for educational inspection."""
        result = []

        def _traverse(node: Optional[LeftistNode], depth: int, relation: str):
            if node is None:
                return
            indent = "  " * depth
            result.append(
                f"{indent}[{relation}] {node.patient.patient_id} ({node.patient.name}) | "
                f"Score: {node.patient.priority_score} | NPL: {node.npl}"
            )
            _traverse(node.left, depth + 1, "L")
            _traverse(node.right, depth + 1, "R")

        _traverse(self.root, 0, "ROOT")
        return result


# Self-test block when running this file directly
if __name__ == "__main__":
    print("=== Testing Manual Leftist Max Heap & O(log n) Queue Merging ===")

    er_heap = LeftistMaxHeap()
    er_heap.insert(Patient("ER1", "Anand", 40, 88, 125, 82, 37.8, 96, "Moderate Abdominal Pain", "10:00:00"))
    er_heap.insert(Patient("ER2", "Priya", 66, 120, 160, 98, 38.8, 91, "Severe Breathing Difficulty", "10:02:00"))

    ambulance_heap = LeftistMaxHeap()
    ambulance_heap.insert(Patient("AMB1", "Vikram (Trauma)", 35, 136, 82, 48, 36.2, 83, "Severe Trauma / Heavy Bleeding", "10:04:00"))
    ambulance_heap.insert(Patient("AMB2", "Sita (Fracture)", 29, 92, 128, 84, 37.1, 97, "Minor Fracture / Sprain", "10:04:30"))

    print("\n1. Main ER Leftist Heap before merge:")
    for line in er_heap.get_preorder_nodes_with_npl():
        print(" ", line)

    print("\n2. Incoming Ambulance Leftist Heap before merge:")
    for line in ambulance_heap.get_preorder_nodes_with_npl():
        print(" ", line)

    print("\n3. Executing O(log n) Leftist Merge...")
    er_heap.merge_with(ambulance_heap)
    for log in er_heap.merge_steps_log:
        print(" ", log)

    print("\n4. Combined Leftist Heap Structure (with NPL values):")
    for line in er_heap.get_preorder_nodes_with_npl():
        print(" ", line)

    print("\n5. Extracting all patients in priority order:")
    while not er_heap.is_empty():
        p = er_heap.extract_max()
        print(f"  Extracted -> {p.patient_id} ({p.name}) | Score: {p.priority_score}")