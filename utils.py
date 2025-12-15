"""
Utility Functions
Helper functions for metrics calculation and output formatting
"""

def calculate_metrics(processes):
    """
    Calculate CT, TAT, WT, RT for all processes and compute averages
    
    Args:
        processes: List of completed Process objects with execution data
        
    Returns:
        Dictionary with individual and average metrics
    """
    print("\n" + "="*60)
    print("CALCULATING METRICS FOR ALL PROCESSES")
    print("="*60 + "\n")
    
    if not processes:
        print("[ERROR] No processes to calculate metrics for!")
        return None
    
    # Lists to store individual metrics for average calculation
    completion_times = []
    turnaround_times = []
    waiting_times = []
    response_times = []
    
    # Calculate metrics for each process
    for process in processes:
        # Ensure metrics are calculated
        if process.completion_time is None:
            print(f"[WARNING] {process.pid} has no completion time!")
            continue
        
        # Get individual metrics
        ct = process.completion_time
        tat = process.turnaround_time
        wt = process.waiting_time
        rt = process.response_time
        
        # Add to lists for averaging
        completion_times.append(ct)
        turnaround_times.append(tat)
        waiting_times.append(wt)
        response_times.append(rt)
        
        print(f"{process.pid}: CT={ct}, TAT={tat}, WT={wt}, RT={rt}")
    
    # Calculate averages
    num_processes = len(processes)
    avg_ct = sum(completion_times) / num_processes if num_processes > 0 else 0
    avg_tat = sum(turnaround_times) / num_processes if num_processes > 0 else 0
    avg_wt = sum(waiting_times) / num_processes if num_processes > 0 else 0
    avg_rt = sum(response_times) / num_processes if num_processes > 0 else 0
    
    print(f"\nAverages: CT={avg_ct:.2f}, TAT={avg_tat:.2f}, WT={avg_wt:.2f}, RT={avg_rt:.2f}")
    
    # Return structured metrics
    metrics = {
        'processes': [],
        'averages': {
            'completion_time': avg_ct,
            'turnaround_time': avg_tat,
            'waiting_time': avg_wt,
            'response_time': avg_rt
        }
    }
    
    # Add individual process metrics
    for process in processes:
        metrics['processes'].append({
            'pid': process.pid,
            'arrival_time': process.arrival_time,
            'burst_time': process.burst_time,
            'priority': process.priority,
            'queue': process.queue,
            'completion_time': process.completion_time,
            'turnaround_time': process.turnaround_time,
            'waiting_time': process.waiting_time,
            'response_time': process.response_time
        })
    
    return metrics


def display_results(processes, metrics):
    """
    Display formatted results table and summary
    
    Args:
        processes: List of completed Process objects
        metrics: Dictionary with calculated metrics
    """
    print("\n" + "="*80)
    print("FINAL RESULTS - MLQ SCHEDULING")
    print("="*80 + "\n")
    
    if not processes or not metrics:
        print("[ERROR] No data to display!")
        return
    
    # Header
    print(f"{'PID':<6} {'AT':<6} {'BT':<6} {'Priority':<10} {'Queue':<8} {'CT':<6} {'TAT':<6} {'WT':<6} {'RT':<6}")
    print("-" * 80)
    
    # Sort processes by PID for display
    sorted_processes = sorted(processes, key=lambda p: p.pid)
    
    # Display each process
    for process in sorted_processes:
        queue_name = f"Q{process.queue}"
        print(f"{process.pid:<6} "
              f"{process.arrival_time:<6} "
              f"{process.burst_time:<6} "
              f"{process.priority:<10} "
              f"{queue_name:<8} "
              f"{process.completion_time:<6} "
              f"{process.turnaround_time:<6} "
              f"{process.waiting_time:<6} "
              f"{process.response_time:<6}")
    
    # Display averages
    print("-" * 80)
    avg = metrics['averages']
    print(f"{'AVERAGE':<6} {'':<6} {'':<6} {'':<10} {'':<8} "
          f"{avg['completion_time']:<6.2f} "
          f"{avg['turnaround_time']:<6.2f} "
          f"{avg['waiting_time']:<6.2f} "
          f"{avg['response_time']:<6.2f}")
    print("="*80)
    
    # Display summary
    print("\nSUMMARY:")
    print(f"  Total Processes: {len(processes)}")
    print(f"  Queue 1 (System - Preemptive Priority): {len([p for p in processes if p.queue == 1])} processes")
    print(f"  Queue 2 (User - FCFS): {len([p for p in processes if p.queue == 2])} processes")
    print(f"\n  Average Turnaround Time: {avg['turnaround_time']:.2f}")
    print(f"  Average Waiting Time: {avg['waiting_time']:.2f}")
    print(f"  Average Response Time: {avg['response_time']:.2f}")


def print_gantt_chart(execution_log):
    """
    Display Gantt chart representation from execution log
    
    Args:
        execution_log: List of tuples (process_id, start_time, end_time)
    """
    print("\n" + "="*80)
    print("GANTT CHART")
    print("="*80 + "\n")
    
    if not execution_log:
        print("[ERROR] No execution log available!")
        return
    
    # Merge consecutive executions of same process
    merged_log = []
    for pid, start, end in execution_log:
        if merged_log and merged_log[-1][0] == pid and merged_log[-1][2] == start:
            # Extend the last entry
            merged_log[-1] = (pid, merged_log[-1][1], end)
        else:
            # Add new entry
            merged_log.append((pid, start, end))
    
    # Print Gantt chart
    print("Process Execution Timeline:")
    print()
    
    # Top border
    chart_line = "|"
    time_line = "0"
    
    for pid, start, end in merged_log:
        duration = end - start
        # Each time unit represented by 4 characters
        chart_line += f" {pid:^{duration*4-2}} |"
        time_line += " " * (duration*4-1) + str(end)
    
    print(chart_line)
    print(time_line)
    print()
    
    # Detailed execution log
    print("Detailed Execution Log:")
    print(f"{'Process':<10} {'Start Time':<12} {'End Time':<12} {'Duration':<10}")
    print("-" * 50)
    
    for pid, start, end in merged_log:
        duration = end - start
        print(f"{pid:<10} {start:<12} {end:<12} {duration:<10}")
    
    print("="*80)


def display_queue_assignment(processes):
    """
    Display how processes are assigned to queues
    
    Args:
        processes: List of Process objects
    """
    print("\n" + "="*60)
    print("QUEUE ASSIGNMENTS")
    print("="*60 + "\n")
    
    queue1_processes = [p for p in processes if p.queue == 1]
    queue2_processes = [p for p in processes if p.queue == 2]
    
    print("Queue 1 (System Processes - Preemptive Priority):")
    print("  Priority 1-2 → Preemptive Priority Scheduling")
    if queue1_processes:
        for p in sorted(queue1_processes, key=lambda x: x.pid):
            print(f"    {p.pid}: Priority={p.priority}, AT={p.arrival_time}, BT={p.burst_time}")
    else:
        print("    (None)")
    
    print("\nQueue 2 (User Processes - FCFS):")
    print("  Priority 3-5 → First-Come, First-Served")
    if queue2_processes:
        for p in sorted(queue2_processes, key=lambda x: x.pid):
            print(f"    {p.pid}: Priority={p.priority}, AT={p.arrival_time}, BT={p.burst_time}")
    else:
        print("    (None)")
    
    print("\nStatic Priority Rule:")
    print("  → Queue 1 ALWAYS executes before Queue 2")
    print("  → Queue 2 can only run when Queue 1 is empty")
    print("="*60)