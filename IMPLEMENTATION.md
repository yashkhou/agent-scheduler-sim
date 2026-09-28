# Implementation note

Working V1 scope: A deterministic discrete-event simulator for multi-agent queues, constrained workers, retries and exponential backoff.

Verified with `python -m unittest discover -s tests -v`.

Known boundary: V1 uses identical worker slots and one-resource jobs; heterogeneous resources and lock graphs are intentionally separate extensions.
