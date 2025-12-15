"""
MLQ Scheduler Implementation
Implements Multilevel Queue scheduling with:
- Queue 1: Preemptive Priority (System Processes)
- Queue 2: FCFS (User Processes)
"""

class MLQScheduler:
    """
    Multilevel Queue Scheduler with static priority
    """
    
    def __init__(self, processes):
        """
        Initialize the MLQ scheduler
        
        Args:
            processes: List of Process objects
        """
        self.processes = processes
        self.current_time = 0
        
        # Two queues: Queue 1 (System - Priority 1-2), Queue 2 (User - Priority 3-5)
        self.queue1 = []  # System processes - Preemptive Priority
        self.queue2 = []  # User processes - FCFS
        
        # Currently executing process
        self.current_process = None
        
        # Execution log for Gantt chart (list of tuples: (pid, start_time, end_time))
        self.execution_log = []
        
        # Completed processes
        self.completed_processes = []
        
        print("[DEBUG] MLQ Scheduler initialized")
        print(f"[DEBUG] Total processes to schedule: {len(processes)}")
        self._print_initial_assignments()
    
    def _print_initial_assignments(self):
        """
        Print initial queue assignments for all processes
        """
        print("\n[DEBUG] Initial Queue Assignments:")
        queue1_procs = [p.pid for p in self.processes if p.queue == 1]
        queue2_procs = [p.pid for p in self.processes if p.queue == 2]
        print(f"  Queue 1 (System - Preemptive Priority): {queue1_procs}")
        print(f"  Queue 2 (User - FCFS): {queue2_procs}")
        print()
    
    def add_arriving_processes(self):
        """
        Check for processes arriving at current_time and add to appropriate queues
        """
        arriving = [p for p in self.processes 
                   if p.arrival_time == self.current_time and not p.is_completed]
        
        for process in arriving:
            if process.queue == 1:
                self.queue1.append(process)
                print(f"[DEBUG] Time {self.current_time}: {process.pid} arrived → Queue 1")
            else:
                self.queue2.append(process)
                print(f"[DEBUG] Time {self.current_time}: {process.pid} arrived → Queue 2")
    
    def sort_queue1_by_priority(self):
        """
        Sort Queue 1 by priority (lower number = higher priority)
        This is needed for Preemptive Priority scheduling
        """
        self.queue1.sort(key=lambda p: (p.priority, p.arrival_time))
    
    def get_next_process(self):
        """
        Get the next process to execute based on MLQ rules:
        1. Queue 1 (System) has absolute priority over Queue 2 (User)
        2. Queue 1 uses Preemptive Priority (lowest priority number first)
        3. Queue 2 uses FCFS (first arrival first)
        
        Returns:
            Process object to execute, or None if no process available
        """
        # Always check Queue 1 first (static priority)
        if self.queue1:
            # Queue 1: Preemptive Priority - get highest priority process
            self.sort_queue1_by_priority()
            return self.queue1[0]
        
        # If Queue 1 is empty, check Queue 2
        elif self.queue2:
            # Queue 2: FCFS - get first process in queue
            return self.queue2[0]
        
        # No process available
        return None
    
    def remove_from_queue(self, process):
        """
        Remove a process from its queue
        
        Args:
            process: Process object to remove
        """
        if process in self.queue1:
            self.queue1.remove(process)
            print(f"[DEBUG] Time {self.current_time}: {process.pid} removed from Queue 1")
        elif process in self.queue2:
            self.queue2.remove(process)
            print(f"[DEBUG] Time {self.current_time}: {process.pid} removed from Queue 2")
    
    def check_preemption(self):
        """
        Check if current process should be preempted
        Used for Queue 1 (Preemptive Priority) and Queue 2 (when Queue 1 arrives)
        
        Returns:
            True if preemption should occur, False otherwise
        """
        if self.current_process is None:
            return False
        
        # If Queue 1 has a process and current is from Queue 2
        # Queue 2 must be preempted (static priority)
        if self.queue1 and self.current_process.queue == 2:
            print(f"[DEBUG] Time {self.current_time}: {self.current_process.pid} "
                  f"preempted by Queue 1 process")
            return True
        
        # If current process is in Queue 1, check for higher priority arrival
        if self.current_process.queue == 1 and self.queue1:
            self.sort_queue1_by_priority()
            highest_priority = self.queue1[0]
            
            # Preempt if a higher priority process is waiting
            if highest_priority.priority < self.current_process.priority:
                print(f"[DEBUG] Time {self.current_time}: {self.current_process.pid} "
                      f"preempted by higher priority {highest_priority.pid}")
                return True
        
        return False
    
    def print_queue_status(self):
        """
        Print current status of both queues (for debugging)
        """
        q1_status = [p.pid for p in self.queue1]
        q2_status = [p.pid for p in self.queue2]
        current = self.current_process.pid if self.current_process else "None"
        
        print(f"[DEBUG] Time {self.current_time} | Current: {current} | "
              f"Q1: {q1_status} | Q2: {q2_status}")
    
    def execute_queue1_process(self, process):
        """
        Execute a Queue 1 (System) process with Preemptive Priority logic
        Executes for 1 time unit, then checks for preemption
        
        Args:
            process: Process object from Queue 1
        
        Returns:
            True if process completed, False otherwise
        """
        # Set start time if this is first execution
        if process.start_time is None:
            process.start_time = self.current_time
            print(f"[DEBUG] Time {self.current_time}: {process.pid} gets CPU for first time (RT will be {self.current_time - process.arrival_time})")
        
        # Execute for 1 time unit
        execution_start = self.current_time
        process.execute(1)
        self.current_time += 1
        
        # Log execution for Gantt chart
        self.execution_log.append((process.pid, execution_start, self.current_time))
        print(f"[DEBUG] Time {execution_start}-{self.current_time}: {process.pid} executing (Remaining: {process.remaining_time})")
        
        # Check if process completed
        if process.is_completed:
            process.completion_time = self.current_time
            self.remove_from_queue(process)
            self.completed_processes.append(process)
            print(f"[DEBUG] Time {self.current_time}: {process.pid} COMPLETED (CT={process.completion_time})")
            return True
        
        return False
    
    def handle_queue1_scheduling(self):
        """
        Handle Queue 1 (Preemptive Priority) scheduling logic
        This method manages:
        1. Adding new arrivals to Queue 1
        2. Checking for preemption
        3. Executing highest priority process
        
        Returns:
            True if a process was executed, False if Queue 1 is empty
        """
        # Add any arriving processes
        self.add_arriving_processes()
        
        # If no processes in Queue 1, return False
        if not self.queue1:
            return False
        
        # Check if current process should be preempted
        if self.current_process and self.check_preemption():
            # Put current process back in its queue if not completed
            if not self.current_process.is_completed:
                if self.current_process.queue == 1:
                    # Already in queue1, just reset current_process
                    pass
                else:
                    # Queue 2 process being preempted, put back in queue2
                    if self.current_process not in self.queue2:
                        self.queue2.insert(0, self.current_process)  # Put back at front (FCFS preservation)
            self.current_process = None
        
        # Get highest priority process from Queue 1
        next_process = self.get_next_process()
        
        if next_process and next_process.queue == 1:
            self.current_process = next_process
            
            # Execute the process for 1 time unit
            completed = self.execute_queue1_process(next_process)
            
            if completed:
                self.current_process = None
            
            return True
        
        return False
    
    def execute_queue2_process(self, process):
        """
        Execute a Queue 2 (User) process with FCFS logic
        Executes for 1 time unit, but can be preempted by Queue 1 arrivals
        
        Args:
            process: Process object from Queue 2
        
        Returns:
            True if process completed, False otherwise
        """
        # Set start time if this is first execution
        if process.start_time is None:
            process.start_time = self.current_time
            print(f"[DEBUG] Time {self.current_time}: {process.pid} gets CPU for first time (RT will be {self.current_time - process.arrival_time})")
        
        # Execute for 1 time unit
        execution_start = self.current_time
        process.execute(1)
        self.current_time += 1
        
        # Log execution for Gantt chart
        self.execution_log.append((process.pid, execution_start, self.current_time))
        print(f"[DEBUG] Time {execution_start}-{self.current_time}: {process.pid} executing (Remaining: {process.remaining_time})")
        
        # Check if process completed
        if process.is_completed:
            process.completion_time = self.current_time
            self.remove_from_queue(process)
            self.completed_processes.append(process)
            print(f"[DEBUG] Time {self.current_time}: {process.pid} COMPLETED (CT={process.completion_time})")
            return True
        
        return False
    
    def handle_queue2_scheduling(self):
        """
        Handle Queue 2 (FCFS) scheduling logic
        Queue 2 only executes when Queue 1 is empty
        This method manages:
        1. Checking Queue 1 is empty (static priority rule)
        2. Executing first process in Queue 2 (FCFS order)
        3. Handling preemption if Queue 1 process arrives
        
        Returns:
            True if a process was executed, False if Queue 2 is empty or Queue 1 has processes
        """
        # Add any arriving processes
        self.add_arriving_processes()
        
        # CRITICAL: Queue 2 can only run if Queue 1 is empty (static priority)
        if self.queue1:
            print(f"[DEBUG] Time {self.current_time}: Queue 2 blocked - Queue 1 has processes")
            return False
        
        # If no processes in Queue 2, return False
        if not self.queue2:
            return False
        
        # Get first process from Queue 2 (FCFS - First Come First Served)
        next_process = self.queue2[0]
        self.current_process = next_process
        
        print(f"[DEBUG] Time {self.current_time}: Executing {next_process.pid} from Queue 2 (FCFS)")
        
        # Execute the process for 1 time unit
        completed = self.execute_queue2_process(next_process)
        
        if completed:
            self.current_process = None
        
        return True
    
    def run(self):
        """
        Execute the MLQ scheduling simulation
        Main scheduling loop that combines Queue 1 and Queue 2 logic
        
        Returns:
            List of completed processes with calculated metrics
        """
        print("\n" + "="*60)
        print("STARTING MLQ SCHEDULING SIMULATION")
        print("="*60 + "\n")
        
        # Calculate maximum possible time (sum of all burst times + max arrival time)
        max_time = sum(p.burst_time for p in self.processes) + max(p.arrival_time for p in self.processes) + 10
        
        # Main scheduling loop
        while len(self.completed_processes) < len(self.processes):
            
            # Safety check to prevent infinite loop
            if self.current_time > max_time:
                print(f"[ERROR] Exceeded maximum time ({max_time}). Breaking loop.")
                break
            
            print(f"\n{'='*50}")
            print(f"TIME: {self.current_time}")
            print(f"{'='*50}")
            
            # Add arriving processes at current time
            self.add_arriving_processes()
            
            # Print current queue status
            self.print_queue_status()
            
            # Flag to track if any process executed this time unit
            process_executed = False
            
            # STEP 1: Try to execute Queue 1 (System - Preemptive Priority)
            # Queue 1 has absolute priority over Queue 2
            if self.queue1:
                print(f"[DECISION] Queue 1 has processes - executing Queue 1")
                process_executed = self.handle_queue1_scheduling()
            
            # STEP 2: If Queue 1 is empty, try Queue 2 (User - FCFS)
            elif self.queue2:
                print(f"[DECISION] Queue 1 empty - executing Queue 2")
                process_executed = self.handle_queue2_scheduling()
            
            # STEP 3: If no process executed (CPU idle)
            if not process_executed:
                # Check if we're waiting for processes to arrive
                waiting_processes = [p for p in self.processes if not p.is_completed]
                
                if waiting_processes:
                    # Find next arrival time
                    next_arrival = min(p.arrival_time for p in waiting_processes if p.arrival_time > self.current_time)
                    print(f"[IDLE] CPU idle - waiting for next arrival at time {next_arrival}")
                    
                    # Jump to next arrival time
                    self.current_time = next_arrival
                else:
                    # All processes completed
                    print(f"[COMPLETE] All processes finished!")
                    break
        
        print("\n" + "="*60)
        print("SCHEDULING COMPLETE")
        print("="*60 + "\n")
        
        # Calculate metrics for all completed processes
        print("[CALCULATING METRICS]")
        for process in self.completed_processes:
            process.calculate_metrics()
        
        return self.completed_processes