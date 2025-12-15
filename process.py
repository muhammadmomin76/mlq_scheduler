"""
Process Class Definition
Represents a single process with all its attributes and metrics
"""

class Process:
    """
    Process class to store process information and calculate metrics
    """
    
    def __init__(self, pid, arrival_time, burst_time, priority):
        """
        Initialize a process with basic attributes
        
        Args:
            pid: Process ID (e.g., "P1", "P2")
            arrival_time: When the process arrives in the ready queue
            burst_time: Total CPU time required
            priority: Priority level (1 = highest priority)
        """
        # Basic process attributes
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        
        # Queue assignment (will be set by scheduler)
        # Priority 1-2 = System (Queue 1), Priority 3-5 = User (Queue 2)
        self.queue = 1 if priority <= 2 else 2
        
        # Execution tracking
        self.remaining_time = burst_time  # Time left to execute
        self.start_time = None            # When process first gets CPU
        self.completion_time = None       # When process finishes
        self.is_completed = False         # Completion status
        
        # Metrics (calculated after execution)
        self.turnaround_time = 0  # TAT = CT - AT
        self.waiting_time = 0     # WT = TAT - BT
        self.response_time = 0    # RT = First CPU time - AT
        
        print(f"[DEBUG] Created {self.pid}: AT={arrival_time}, BT={burst_time}, "
              f"Priority={priority}, Queue={self.queue}")
    
    def execute(self, time_units=1):
        """
        Execute the process for given time units
        
        Args:
            time_units: Number of time units to execute (default 1)
        
        Returns:
            Time units actually executed
        """
        if self.is_completed:
            return 0
        
        # Track first CPU allocation (for response time)
        if self.start_time is None:
            self.start_time = None  # Will be set by scheduler
        
        # Execute for the given time or remaining time, whichever is smaller
        executed = min(time_units, self.remaining_time)
        self.remaining_time -= executed
        
        # Check if process completed
        if self.remaining_time == 0:
            self.is_completed = True
        
        return executed
    
    def calculate_metrics(self):
        """
        Calculate all metrics after process completion
        Must be called after completion_time is set
        """
        if self.completion_time is None:
            print(f"[ERROR] Cannot calculate metrics for {self.pid} - completion_time not set")
            return
        
        # TAT = Completion Time - Arrival Time
        self.turnaround_time = self.completion_time - self.arrival_time
        
        # WT = Turnaround Time - Burst Time
        self.waiting_time = self.turnaround_time - self.burst_time
        
        # RT = First CPU Time - Arrival Time
        if self.start_time is not None:
            self.response_time = self.start_time - self.arrival_time
        
        print(f"[DEBUG] {self.pid} Metrics: CT={self.completion_time}, "
              f"TAT={self.turnaround_time}, WT={self.waiting_time}, RT={self.response_time}")
    
    def __repr__(self):
        """
        String representation of the process
        """
        return (f"Process({self.pid}, AT={self.arrival_time}, BT={self.burst_time}, "
                f"Priority={self.priority}, Queue={self.queue})")
    
    def __str__(self):
        """
        User-friendly string representation
        """
        status = "Completed" if self.is_completed else f"Running (Remaining: {self.remaining_time})"
        return f"{self.pid} [{status}]"