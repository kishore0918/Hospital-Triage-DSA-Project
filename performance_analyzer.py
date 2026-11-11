# Filename: performance_analyzer.py
"""
Performance Benchmarking and Complexity Analysis Module.
Tests Binary Max Heap across N = [10, 100, 1000, 10000] synthetic patients,
measures execution times, heapify-up/down operations, and comparisons,
and generates Matplotlib visualization charts comparing empirical measurements
against theoretical O(log n) complexity and O(n) linear list scanning.
"""

import random
import math
import time
from typing import List, Dict, Any
import matplotlib.pyplot as plt

from patient import Patient
from priority_scorer import SYMPTOM_WEIGHTS
from binary_max_heap import BinaryMaxHeap

# Predefined lists for generating realistic synthetic patients
SAMPLE_NAMES = [
    "Arun", "Divya", "Karthik", "Priya", "Suresh", "Lakshmi", "Vikram",
    "Meena", "Ramesh", "Anitha", "Sanjay", "Kavitha", "Rajesh", "Deepa",
    "Prakash", "Nithya", "Gopal", "Swathi", "Manoj", "Revathi"
]
SYMPTOM_LIST = list(SYMPTOM_WEIGHTS.keys())


def generate_random_patient(index: int) -> Patient:
    """Generates a single synthetic patient with randomized vital signs and symptoms."""
    name = f"{random.choice(SAMPLE_NAMES)}_{index}"
    age = random.randint(2, 88)
    heart_rate = random.randint(42, 150)
    systolic_bp = random.randint(78, 195)
    diastolic_bp = random.randint(45, 125)
    temperature = round(random.uniform(34.8, 40.4), 1)
    spo2 = random.randint(80, 100)
    symptoms = random.choice(SYMPTOM_LIST)

    return Patient(
        patient_id=f"P{index:05d}",
        name=name,
        age=age,
        heart_rate=heart_rate,
        systolic_bp=systolic_bp,
        diastolic_bp=diastolic_bp,
        temperature=temperature,
        spo2=spo2,
        symptoms=symptoms
    )


def run_scaling_benchmarks(sizes: List[int] = None) -> List[Dict[str, Any]]:
    """
    Runs performance benchmarks for each queue size in `sizes` (default: 10, 100, 1000, 10000).
    Measures insertion time, extraction time, heapify operations, comparisons,
    restructuring time, and compares against an O(n) linear list priority scan.
    """
    if sizes is None:
        sizes = [10, 100, 1000, 10000]

    random.seed(42)  # Fixed seed for reproducible benchmark comparisons
    results = []

    for n in sizes:
        patients = [generate_random_patient(i + 1) for i in range(n)]
        heap = BinaryMaxHeap()

        # 1. Measure N Insertions into Binary Max Heap
        total_insert_restructure_ms = 0.0
        start_insert = time.perf_counter()
        for p in patients:
            heap.insert(p)
            total_insert_restructure_ms += heap.last_restructure_time_ms
        end_insert = time.perf_counter()

        total_insert_time_ms = (end_insert - start_insert) * 1000.0
        avg_insert_time_us = (total_insert_time_ms * 1000.0) / n  # in microseconds
        heapify_up_ops = heap.heapify_up_count
        insert_comparisons = heap.total_comparisons

        # Verify heap invariant holds before extraction
        heap_valid = heap.verify_max_heap_property()

        # 2. Measure N Extractions from Binary Max Heap
        total_extract_restructure_ms = 0.0
        start_extract = time.perf_counter()
        while not heap.is_empty():
            heap.extract_max()
            total_extract_restructure_ms += heap.last_restructure_time_ms
        end_extract = time.perf_counter()

        total_extract_time_ms = (end_extract - start_extract) * 1000.0
        avg_extract_time_us = (total_extract_time_ms * 1000.0) / n  # in microseconds
        heapify_down_ops = heap.heapify_down_count
        total_heapify_ops = heap.total_heapify_operations
        total_comparisons = heap.total_comparisons
        total_restructure_ms = total_insert_restructure_ms + total_extract_restructure_ms

        # 3. Compare with Naive Unsorted Queue (O(n) linear scan per extraction)
        # For N=10000, we measure 200 extractions and scale proportionally so the GUI never freezes,
        # or run full extractions for N <= 1000.
        naive_queue = list(patients)
        start_naive = time.perf_counter()
        if n <= 1000:
            while naive_queue:
                best_idx = 0
                for i in range(1, len(naive_queue)):
                    if naive_queue[i].has_higher_priority_than(naive_queue[best_idx]):
                        best_idx = i
                naive_queue.pop(best_idx)
            naive_extract_ms = (time.perf_counter() - start_naive) * 1000.0
        else:
            sample_runs = 200
            for _ in range(sample_runs):
                best_idx = 0
                for i in range(1, len(naive_queue)):
                    if naive_queue[i].has_higher_priority_than(naive_queue[best_idx]):
                        best_idx = i
                naive_queue.pop(best_idx)
            elapsed_sample_ms = (time.perf_counter() - start_naive) * 1000.0
            # Extrapolate full N extractions (average list length is N/2)
            naive_extract_ms = elapsed_sample_ms * (n / sample_runs) * 0.5

        results.append({
            "n": n,
            "log2_n": round(math.log2(n), 2),
            "insert_total_ms": round(total_insert_time_ms, 3),
            "insert_avg_us": round(avg_insert_time_us, 3),
            "extract_total_ms": round(total_extract_time_ms, 3),
            "extract_avg_us": round(avg_extract_time_us, 3),
            "restructure_total_ms": round(total_restructure_ms, 3),
            "heapify_up": heapify_up_ops,
            "heapify_down": heapify_down_ops,
            "total_heapify": total_heapify_ops,
            "insert_comparisons": insert_comparisons,
            "total_comparisons": total_comparisons,
            "naive_extract_ms": round(naive_extract_ms, 3),
            "heap_valid": heap_valid
        })

    return results


def print_benchmark_table(results: List[Dict[str, Any]]) -> str:
    """Formats the benchmark results as a clean ASCII table for console & GUI display."""
    lines = []
    header = (
        f"{'N (Size)':>8} | {'Insert(ms)':>10} | {'Extract(ms)':>11} | "
        f"{'Restruct(ms)':>12} | {'Heapify-Up':>10} | {'Heapify-Down':>12} | "
        f"{'Total Heapify':>13} | {'Comparisons':>11} | {'Naive O(n^2)(ms)':>16}"
    )
    sep = "-" * len(header)
    lines.append(sep)
    lines.append(header)
    lines.append(sep)

    for r in results:
        row = (
            f"{r['n']:>8} | {r['insert_total_ms']:>10.3f} | {r['extract_total_ms']:>11.3f} | "
            f"{r['restructure_total_ms']:>12.3f} | {r['heapify_up']:>10} | {r['heapify_down']:>12} | "
            f"{r['total_heapify']:>13} | {r['total_comparisons']:>11} | {r['naive_extract_ms']:>16.2f}"
        )
        lines.append(row)
    lines.append(sep)
    return "\n".join(lines)


def plot_performance_graphs(results: List[Dict[str, Any]], save_path: str = "heap_performance_analysis.png") -> None:
    """
    Plots a 4-panel Matplotlib dashboard comparing empirical Binary Max Heap measurements
    with theoretical O(log n) complexity and naive O(n) list extraction.
    """
    sizes = [r["n"] for r in results]
    size_labels = [str(n) for n in sizes]
    insert_ms = [r["insert_total_ms"] for r in results]
    extract_ms = [r["extract_total_ms"] for r in results]
    avg_extract_us = [r["extract_avg_us"] for r in results]
    log2_n = [r["log2_n"] for r in results]
    heapify_up = [r["heapify_up"] for r in results]
    heapify_down = [r["heapify_down"] for r in results]
    naive_ms = [r["naive_extract_ms"] for r in results]

    fig, axes = plt.subplots(2, 2, figsize=(13, 8.5))
    fig.suptitle(
        "Binary Max Heap Triage System — Empirical vs. Theoretical Performance Analysis\n"
        "Kishore Kumar S (Reg No: 2026166027) — M.Tech AI & DS DSA Mini-Project",
        fontsize=12, fontweight="bold"
    )

    # Panel 1: Total Insertion vs Extraction Execution Time (ms)
    ax1 = axes[0, 0]
    ax1.plot(sizes, insert_ms, marker="o", linewidth=2, color="#1f77b4", label="Total Insertion Time (ms)")
    ax1.plot(sizes, extract_ms, marker="s", linewidth=2, color="#d62728", label="Total Extraction Time (ms)")
    ax1.set_title("1. Total Execution Time vs. Queue Size (N)", fontweight="bold")
    ax1.set_xlabel("Number of Patients (N)")
    ax1.set_ylabel("Execution Time (milliseconds)")
    ax1.grid(True, linestyle="--", alpha=0.6)
    ax1.legend()

    # Panel 2: Per-Operation Extraction Time (us) vs Theoretical O(log2 N) Curve
    ax2 = axes[0, 1]
    ax2.plot(size_labels, avg_extract_us, marker="o", linewidth=2, color="#2ca02c", label="Measured Avg Extract (μs/patient)")
    # Scale theoretical log2(N) to first datapoint for visual curve comparison
    scale_factor = avg_extract_us[0] / log2_n[0] if log2_n[0] > 0 else 1.0
    theoretical_curve = [val * scale_factor for val in log2_n]
    ax2.plot(size_labels, theoretical_curve, marker="^", linestyle="--", linewidth=2, color="#ff7f0e", label="Theoretical O(log₂ n) Reference")
    ax2.set_title("2. Single Operation Scaling: Measured vs. Theoretical O(log n)", fontweight="bold")
    ax2.set_xlabel("Queue Size Category (N)")
    ax2.set_ylabel("Time per Patient (microseconds)")
    ax2.grid(True, linestyle="--", alpha=0.6)
    ax2.legend()

    # Panel 3: Heapify-Up vs Heapify-Down Operations Count
    ax3 = axes[1, 0]
    x_pos = range(len(size_labels))
    width = 0.35
    ax3.bar([p - width / 2 for p in x_pos], heapify_up, width=width, color="#4c72b0", label="Heapify-Up (Insertions)")
    ax3.bar([p + width / 2 for p in x_pos], heapify_down, width=width, color="#dd8452", label="Heapify-Down (Extractions)")
    ax3.set_xticks(list(x_pos))
    ax3.set_xticklabels(size_labels)
    ax3.set_title("3. Structural Operations: Heapify-Up vs. Heapify-Down", fontweight="bold")
    ax3.set_xlabel("Queue Size (N)")
    ax3.set_ylabel("Number of Swaps / Heapify Operations")
    ax3.grid(True, axis="y", linestyle="--", alpha=0.6)
    ax3.legend()

    # Panel 4: Binary Max Heap O(N log N) vs Unsorted FIFO Scan O(N^2) (Log Scale)
    ax4 = axes[1, 1]
    ax4.plot(size_labels, extract_ms, marker="o", linewidth=2.5, color="#2ca02c", label="Binary Max Heap Extract All: O(N log N)")
    ax4.plot(size_labels, naive_ms, marker="X", linewidth=2.5, color="#c44e52", label="Unsorted List Linear Scan: O(N²)")
    ax4.set_yscale("log")
    ax4.set_title("4. Triage Extraction Speedup: Binary Heap vs. Linear Scan (Log Scale)", fontweight="bold")
    ax4.set_xlabel("Queue Size (N)")
    ax4.set_ylabel("Total Extraction Time (ms - Log Scale)")
    ax4.grid(True, which="both", linestyle="--", alpha=0.6)
    ax4.legend()

    plt.tight_layout(rect=[0, 0.02, 1, 0.93])
    plt.savefig(save_path, dpi=150)
    print(f"\n[INFO] Saved high-resolution benchmark chart to: {save_path}")
    plt.show()


# Self-test block when running this file directly
if __name__ == "__main__":
    print("=== Running Hospital Triage Heap Scaling Benchmarks (N = 10, 100, 1000, 10000) ===")
    benchmark_results = run_scaling_benchmarks([10, 100, 1000, 10000])
    print(print_benchmark_table(benchmark_results))
    print("\nOpening Matplotlib Performance Analysis Window... (Close the graph window to return to terminal)")
    plot_performance_graphs(benchmark_results)