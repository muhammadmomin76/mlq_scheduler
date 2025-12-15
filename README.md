# Multilevel Queue (MLQ) CPU Scheduler

## Overview

This project implements a **Multilevel Queue (MLQ) CPU Scheduling Algorithm** with two static priority queues:

- **Queue 1 (System Processes)**: Uses Preemptive Priority Scheduling
- **Queue 2 (User Processes)**: Uses FCFS Scheduling

The scheduler follows a strict priority rule: Queue 1 always executes before Queue 2.

## Author

**Student #7 - Advanced Operating Systems**  
Assignment: MLQ Scheduling Implementation

## Project Structure

```
mlq_scheduler/
├── main.py              # Entry point - runs the simulation
├── process.py           # Process class definition
├── mlq_scheduler.py     # MLQ scheduling logic
├── utils.py             # Helper functions and metrics calculation
├── requirements.txt     # Python dependencies (empty - uses standard library)
├── test_case.csv        # Example test case file (optional)
└── README.md            # This file
```

## Requirements

- Python 3.8 or higher
- No external libraries required (uses only standard Python)

## Setup Instructions

### Step 1: Clone Repository

```bash
git clone https://github.com/muhammadmomin76/mlq_scheduler.git
cd mlq_scheduler
```

### Step 2: Create Virtual Environment (Optional but Recommended)

#### On Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Verify Setup

```bash
# Check Python version (requires 3.8+)
python --version

# Run with default test case
python main.py
# Just press Enter when prompted
```

### Step 4: Deactivate Virtual Environment (When Done)

```bash
deactivate
```

## Quick Start Guide

```bash
# Clone and navigate to project
git clone <your-repo-url>
cd mlq_scheduler

# Run with default test case (easiest)
python main.py
# Press Enter when prompted

# OR run with your own test case (for evaluators)
python main.py your_test.csv
```

That's it! The program will run and display complete results.

## Test Data Used

| PID | Arrival Time | Burst Time | Priority | Queue Assignment |
|-----|-------------|------------|----------|------------------|
| P1  | 0           | 10         | 3        | System (Q1)      |
| P2  | 2           | 5          | 1        | System (Q1)      |
| P3  | 4           | 3          | 4        | User (Q2)        |
| P4  | 6           | 8          | 2        | System (Q1)      |
| P5  | 8           | 1          | 5        | User (Q2)        |

**Queue Assignment Rule**: Priority 1-2 → System (Queue 1), Priority 3-5 → User (Queue 2)

## Algorithm Details

### Queue 1: Preemptive Priority Scheduling

- Lower priority number = Higher priority (1 is highest)
- Processes can be preempted by higher priority arrivals
- Always executes before Queue 2

### Queue 2: FCFS Scheduling

- First-Come, First-Served order
- No preemption within this queue
- Only runs when Queue 1 is empty

### Static Priority Rule

Queue 1 has absolute priority over Queue 2. If a Queue 1 process arrives while a Queue 2 process is running, the Queue 2 process is immediately preempted.

## Metrics Calculated

- **Completion Time (CT)**: When the process finishes
- **Turnaround Time (TAT)**: CT - Arrival Time
- **Waiting Time (WT)**: TAT - Burst Time
- **Response Time (RT)**: First CPU allocation - Arrival Time

## For Evaluators - Testing with Custom Data

This implementation is designed for easy testing with new test cases. **No code modification required!**

### Recommended Method for Evaluation

The fastest way to test with your own data:

```bash
# Step 1: Create your test case CSV file
cat > evaluator_test.csv << EOF
P1,0,5,1
P2,1,3,2
P3,2,8,3
P4,3,4,4
EOF

# Step 2: Run directly (no prompts!)
python main.py evaluator_test.csv
```

This will:

- Load your test case automatically
- Run the complete MLQ simulation  
- Display results table with all metrics
- Show Gantt chart for verification
- Calculate and display averages

### Alternative: Interactive Testing

```bash
python main.py
# Select option 2 for manual input
# Enter processes one by one
# Type 'done' when finished
```

### Input Validation

The program automatically validates:

- ✅ Arrival Time >= 0
- ✅ Burst Time > 0
- ✅ Priority between 1-5
- ✅ Proper CSV format
- ✅ File existence

If validation fails, it provides clear error messages and falls back to the default test case.

### Example Test Cases for Different Scenarios

#### Test Case 1: Heavy System Load (Tests Queue 1 Priority)

```csv
P1,0,15,1
P2,1,10,1
P3,2,5,2
P4,3,8,2
```

Expected: Queue 1 processes execute by priority, Queue 2 starves.

#### Test Case 2: User Process Starvation (Tests Static Priority)

```csv
P1,0,20,4
P2,5,5,1
P3,10,5,1
P4,15,5,1
```

Expected: P1 starts but gets preempted repeatedly by System processes.

#### Test Case 3: Mixed Workload (Tests Both Queues)

```csv
S1,0,10,1
S2,2,8,2
U1,4,12,3
U2,6,6,4
U3,8,4,5
```

Expected: System processes complete first, then User processes in FCFS order.

#### Test Case 4: Simultaneous Arrivals (Tests Tie-Breaking)

```csv
P1,0,5,3
P2,0,8,1
P3,0,3,2
P4,0,10,4
```

Expected: Queue 1 processes (P2, P3) execute by priority before Queue 2.

### Output Format

The simulator produces:

1. **Detailed execution log** - Shows every time unit with decisions
2. **Results table** - CT, TAT, WT, RT for each process
3. **Gantt chart** - Visual timeline of execution
4. **Summary statistics** - Averages and queue distributions

All output is clearly formatted and ready to copy into reports.

## Submission Date

December 20, 2025
