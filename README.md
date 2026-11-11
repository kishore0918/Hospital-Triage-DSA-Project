# Priority-Based Hospital Triage System Using Heap Data Structures

**Developer:** Kishore Kumar S  
**Registration Number:** 2026166027  
**Degree:** M.Tech Artificial Intelligence and Data Science  
**Course:**Advanced Data Structures and Algorithms (DSA) Mini-Project  

---

## Project Overview
In a standard emergency room, a First-In-First-Out (FIFO) queue can be dangerous. A patient arriving with cardiac arrest must be treated immediately, even if someone with a mild fever arrived an hour earlier. 

This project simulates a **Priority-Based Hospital Triage System**. It calculates a priority score for incoming patients based on vital signs (Heart Rate, Blood Pressure, $\text{SpO}_2$, Temperature) and reported symptoms. Instead of built-in libraries, this project implements a manual **Binary Max Heap** and **Leftist Max Heap** from scratch to maintain the queue dynamically and ensure the most critical patient is always extracted in $O(\log n)$ time.


---

## Core DSA Features

1. **Manual Binary Max Heap (Array-Based)**
   * **Insert Patient ($O(\log n)$):** Adds a patient to the leaf and performs `Heapify-Up`.
   * **Extract Highest Priority ($O(\log n)$):** Removes the root node, moves the last leaf to the root, and performs `Heapify-Down`.
   * **Peek ($O(1)$):** Identifies the next patient to be treated instantly.
   * **Custom Tie-Breaking:** If two patients have identical priority scores, the algorithm automatically prioritizes the patient with the earlier arrival time.

2. **Leftist Max Heap (Pointer-Based Extension)**
   * Implements a mergeable priority queue utilizing **Null Path Length (NPL)**.
   * Demonstrates how two separate emergency queues (e.g., Main ER Queue + Incoming Ambulance Transfer Queue) can be merged efficiently in **$O(\log n)$** time, compared to the $O(n)$ time required by standard arrays.

3. **Live Tkinter Dashboard & Visualizer**
   * Real-time Binary Tree Canvas that draws the exact node structure of the heap.
   * Step-by-Step Restructuring Log showing the exact parent/child comparisons and swaps during Heapify operations.

4. **Performance Benchmarking Suite**
   * Generates up to 10,000 synthetic patients and empirically measures insertion, extraction, and restructuring times.
   * Plots Matplotlib graphs proving logarithmic $O(\log n)$ scaling against an inefficient $O(n^2)$ linear list scan.

---

## 📊 Theoretical Time Complexity

| Operation | Binary Max Heap | Leftist Max Heap | Unsorted FIFO List |
| :--- | :---: | :---: | :---: |
| **Insert Patient** | $O(\log n)$ | $O(\log n)$ | $O(1)$ |
| **Extract Highest Priority** | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| **Peek Highest Priority** | $O(1)$ | $O(1)$ | $O(n)$ |
| **Merge Two Queues** | $O(n)$ | $O(\log n)$ | $O(1)$ |

---

## Project Structure

* `patient.py`: Data model for patient records and custom tie-breaking logic.
* `priority_scorer.py`: Rule engine calculating the educational triage score.
* `binary_max_heap.py`: Core algorithm for array-based heapification and metrics tracking.
* `leftist_heap.py`: Advanced extension demonstrating $O(\log n)$ NPL queue merging.
* `performance_analyzer.py`: Automated benchmarking scaling from $N=10$ to $N=10000$.
* `main_gui.py`: The main executable Tkinter dashboard connecting all modules.

---

## How to Run the Application Locally

**Requirements:** Windows OS, Python 3.x

1. Clone or download this repository to your local machine.
2. Open the project folder in Visual Studio Code.
3. Open the VS Code integrated terminal and create a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```
4. Install the required visualization library:
   ```powershell
   pip install matplotlib
   ```
5. Launch the application:
   ```powershell
   python main_gui.py
   ```