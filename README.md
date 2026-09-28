# agent-scheduler-sim

A deterministic discrete-event simulator for multi-agent queues, constrained workers, retries and exponential backoff.

## What it does

- simulates worker capacity without sleeping in wall-clock time
- supports job arrival time, duration, priority, failure count and retry limit
- models exponential backoff and measures queue latency, throughput and utilization
- flags starvation candidates that waited beyond a configurable threshold

## Quick start

```bash
PYTHONPATH=src python -m agent_scheduler_sim examples/scenario.json
```

No model API, network service, or third-party package is required.

## Architecture

The simulator advances to the next arrival/completion/backoff event. Jobs enter a priority queue, consume one worker, and may deterministically fail a configured number of attempts before succeeding or exhausting retries.

See [`docs/architecture.md`](docs/architecture.md) for the data model and trade-offs.

## V1 boundary

V1 uses identical worker slots and one-resource jobs; heterogeneous resources and lock graphs are intentionally separate extensions.

## Development

```bash
python -m unittest discover -s tests -v
```

MIT licensed.


## v0.1.1

**Policy comparison, deadlines and retry economics.** The simulator now compares FIFO vs priority scheduling and reports deadline misses, queue percentiles, worker busy time, and accumulated exponential retry delay.

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```
