# Architecture

The simulator advances to the next arrival/completion/backoff event. Jobs enter a priority queue, consume one worker, and may deterministically fail a configured number of attempts before succeeding or exhausting retries.

## Design constraints

- deterministic offline behavior
- explicit machine-readable inputs and outputs
- small standard-library surface area
- failures are surfaced rather than hidden

## V1 limitation

V1 uses identical worker slots and one-resource jobs; heterogeneous resources and lock graphs are intentionally separate extensions.
