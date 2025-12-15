"""
MLQ Scheduler - Main Entry Point
Student #7: Multilevel Queue Scheduling Implementation
Advanced Operating Systems - Week Assignment
"""

from process import Process
from mlq_scheduler import MLQScheduler
from utils import (
    calculate_metrics, 
    display_results, 
    print_gantt_chart,
    display_queue_assignment
)


def create_test_processes():
    """
    Create the test dataset as specified in the assignment
    
    Returns:
        List of Process objects
    """
    print("Creating test processes...")
    
    # Test data from assignment
    processes = [
        Process(pid="P1", arrival_time=0, burst_time=10, priority=3),
        Process(pid="P2", arrival_time=2, burst_time=5, priority=1),
        Process(pid="P3", arrival_time=4, burst_time=3, priority=4),
        Process(pid="P4", arrival_time=6, burst_time=8, priority=2),
        Process(pid="P5", arrival_time=8, burst_time=1, priority=5),
    ]
    
    print(f"Created {len(processes)} processes\n")
    return processes


def create_custom_processes():
    """
    Create custom test processes from user input
    Allows evaluator to test with different datasets
    
    Returns:
        List of Process objects
    """
    print("\n" + "="*60)
    print("CUSTOM TEST CASE INPUT")
    print("="*60)
    print("Enter process details (or press Enter to use default test case)")
    print("Format for each process: PID,ArrivalTime,BurstTime,Priority")
    print("Example: P1,0,10,3")
    print("Enter 'done' when finished\n")
    
    processes = []
    
    while True:
        user_input = input(f"Process {len(processes)+1} (or 'done'): ").strip()
        
        if user_input.lower() == 'done':
            if len(processes) == 0:
                print("No processes entered. Using default test case.")
                return create_test_processes()
            break
        
        if user_input == "":
            print("Using default test case.")
            return create_test_processes()
        
        try:
            # Parse input: PID,AT,BT,Priority
            parts = user_input.split(',')
            if len(parts) != 4:
                print("Error: Please enter exactly 4 values (PID,AT,BT,Priority)")
                continue
            
            pid = parts[0].strip()
            arrival_time = int(parts[1].strip())
            burst_time = int(parts[2].strip())
            priority = int(parts[3].strip())
            
            # Validate values
            if arrival_time < 0 or burst_time <= 0 or priority < 1 or priority > 5:
                print("Error: AT>=0, BT>0, Priority must be 1-5")
                continue
            
            # Create process
            process = Process(pid, arrival_time, burst_time, priority)
            processes.append(process)
            print(f"  ✓ Added {pid}")
            
        except ValueError:
            print("Error: Invalid input format. Use: PID,AT,BT,Priority")
            continue
    
    print(f"\nCreated {len(processes)} custom processes\n")
    return processes


def load_processes_from_file(filename):
    """
    Load processes from a CSV file
    File format: PID,ArrivalTime,BurstTime,Priority (one process per line)
    
    Args:
        filename: Path to CSV file
    
    Returns:
        List of Process objects
    """
    print(f"Loading processes from file: {filename}")
    
    try:
        processes = []
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse CSV line
                parts = line.split(',')
                if len(parts) != 4:
                    print(f"Warning: Skipping line {line_num} (invalid format)")
                    continue
                
                pid = parts[0].strip()
                arrival_time = int(parts[1].strip())
                burst_time = int(parts[2].strip())
                priority = int(parts[3].strip())
                
                # Create process
                process = Process(pid, arrival_time, burst_time, priority)
                processes.append(process)
        
        print(f"Loaded {len(processes)} processes from file\n")
        return processes
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found!")
        print("Using default test case instead.\n")
        return create_test_processes()
    except Exception as e:
        print(f"Error reading file: {e}")
        print("Using default test case instead.\n")
        return create_test_processes()


def get_processes():
    """
    Get processes based on user preference or command line argument
    
    Returns:
        List of Process objects
    """
    import sys
    
    # Check for command line argument
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        return load_processes_from_file(filename)
    
    # Ask user for input method
    print("\n" + "="*60)
    print("SELECT INPUT METHOD")
    print("="*60)
    print("1. Use default test case (from assignment)")
    print("2. Enter custom test case manually")
    print("3. Load from file")
    print("="*60)
    
    choice = input("Enter choice (1/2/3) [default: 1]: ").strip()
    
    if choice == "2":
        return create_custom_processes()
    elif choice == "3":
        filename = input("Enter filename: ").strip()
        return load_processes_from_file(filename)
    else:
        # Default or pressing Enter goes to option 1
        print("Using default test case.\n")
        return create_test_processes()


def print_header():
    """
    Print program header
    """
    print("\n" + "="*80)
    print(" "*20 + "MULTILEVEL QUEUE (MLQ) CPU SCHEDULER")
    print(" "*25 + "Student #7 Assignment")
    print(" "*20 + "Advanced Operating Systems Course")
    print("="*80)


def print_algorithm_info():
    """
    Print algorithm information
    """
    print("\nALGORITHM INFORMATION:")
    print("-" * 60)
    print("Queue 1 (System Processes - Priority 1-2):")
    print("  → Scheduling: Preemptive Priority")
    print("  → Rule: Lower priority number = Higher priority")
    print("  → Preemption: Can be preempted by higher priority arrivals")
    print()
    print("Queue 2 (User Processes - Priority 3-5):")
    print("  → Scheduling: First-Come, First-Served (FCFS)")
    print("  → Rule: Arrival order determines execution")
    print("  → Preemption: Preempted by ANY Queue 1 process")
    print()
    print("MLQ Static Priority Rule:")
    print("  → Queue 1 ALWAYS has priority over Queue 2")
    print("  → Queue 2 only executes when Queue 1 is empty")
    print("-" * 60)


def main():
    """
    Main function to run the MLQ scheduler simulation
    """
    # Print header
    print_header()
    
    # Print algorithm info
    print_algorithm_info()
    
    # Get processes (prompts user for input method or uses command line arg)
    processes = get_processes()
    
    # Create test processes section
    print("\n" + "="*80)
    print("STEP 1: PROCESS DATA LOADED")
    print("="*80 + "\n")
    
    # Display queue assignments
    display_queue_assignment(processes)
    
    # Create scheduler
    print("\n" + "="*80)
    print("STEP 2: INITIALIZING MLQ SCHEDULER")
    print("="*80 + "\n")
    
    scheduler = MLQScheduler(processes)
    
    # Run simulation
    print("\n" + "="*80)
    print("STEP 3: RUNNING SIMULATION")
    print("="*80)
    
    completed_processes = scheduler.run()
    
    # Calculate metrics
    print("\n" + "="*80)
    print("STEP 4: CALCULATING METRICS")
    print("="*80)
    
    metrics = calculate_metrics(completed_processes)
    
    # Display results
    print("\n" + "="*80)
    print("STEP 5: DISPLAYING RESULTS")
    print("="*80)
    
    display_results(completed_processes, metrics)
    
    # Display Gantt chart
    print_gantt_chart(scheduler.execution_log)
    
    # Print completion message
    print("\n" + "="*80)
    print("SIMULATION COMPLETE!")
    print("="*80)
    print("="*80 + "\n")


if __name__ == "__main__":
    main()