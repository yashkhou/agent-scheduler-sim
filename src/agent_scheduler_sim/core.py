from __future__ import annotations

from dataclasses import dataclass
import heapq
import math


@dataclass
class Job:
    id: str
    arrival: float
    duration: float
    priority: int = 0
    fail_attempts: int = 0
    max_retries: int = 0
    backoff: float = 1.0
    deadline: float | None = None
    attempts: int = 0
    first_start: float | None = None
    completed: float | None = None
    retry_delay_total: float = 0.0


def _percentile(values, percentile):
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(percentile * len(ordered)) - 1))
    return ordered[index]


def simulate(rows, workers=2, starvation=10, policy="priority"):
    if workers < 1:
        raise ValueError("workers must be >= 1")
    if policy not in {"priority", "fifo"}:
        raise ValueError("policy must be priority or fifo")
    jobs = [Job(**row) for row in rows]
    events = []
    seq = 0
    for job in jobs:
        heapq.heappush(events, (job.arrival, 0, seq, "arrival", job)); seq += 1
    ready = []; running = {}; now = 0.0; busy = 0.0; waits = []; exhausted = []
    worker_busy_time = 0.0
    def ready_key(item):
        enqueued, enqueue_seq, job = item
        if policy == "fifo":
            return (enqueued, enqueue_seq)
        return (-job.priority, enqueued, enqueue_seq)
    while events or ready or running:
        if not ready or len(running) >= workers:
            if not events:
                break
            now = max(now, events[0][0])
            same = []
            while events and events[0][0] <= now:
                same.append(heapq.heappop(events))
            for event_time, _, event_seq, kind, job in same:
                if kind in ("arrival", "retry"):
                    ready.append((event_time, event_seq, job))
                elif kind == "done":
                    running.pop(job.id, None)
                    busy += job.duration
                    worker_busy_time += job.duration
                    failed = job.attempts <= job.fail_attempts
                    if failed and job.attempts <= job.max_retries:
                        delay = job.backoff * (2 ** (job.attempts - 1))
                        job.retry_delay_total += delay
                        heapq.heappush(events, (now + delay, 1, seq, "retry", job)); seq += 1
                    else:
                        if failed:
                            exhausted.append(job.id)
                        job.completed = now
        while ready and len(running) < workers:
            ready.sort(key=ready_key)
            _, _, job = ready.pop(0)
            job.attempts += 1
            if job.first_start is None:
                job.first_start = now; waits.append(now - job.arrival)
            running[job.id] = job
            heapq.heappush(events, (now + job.duration, 2, seq, "done", job)); seq += 1
    makespan = max([job.completed or 0 for job in jobs], default=0) - min([job.arrival for job in jobs], default=0)
    completed = sum(1 for job in jobs if job.completed is not None and job.id not in exhausted)
    deadline_misses = [job.id for job in jobs if job.deadline is not None and (job.completed is None or job.completed > job.deadline)]
    return {
        "jobs": len(jobs),
        "completed": completed,
        "exhausted": exhausted,
        "makespan": makespan,
        "throughput_per_time": completed / makespan if makespan > 0 else 0,
        "mean_queue_latency": sum(waits) / len(waits) if waits else 0,
        "p50_queue_latency": _percentile(waits, 0.50),
        "p95_queue_latency": _percentile(waits, 0.95),
        "max_queue_latency": max(waits, default=0),
        "utilization": busy / (workers * makespan) if makespan > 0 else 0,
        "worker_busy_time": worker_busy_time,
        "starved": [job.id for job in jobs if job.first_start is not None and job.first_start - job.arrival > starvation],
        "deadline_misses": deadline_misses,
        "attempts": {job.id: job.attempts for job in jobs},
        "retry_delay_total": {job.id: job.retry_delay_total for job in jobs},
        "policy": policy,
    }
