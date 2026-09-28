import heapq
from dataclasses import dataclass,field
@dataclass(order=True)
class QItem:
 sort:tuple; job:object=field(compare=False)
@dataclass
class Job:
 id:str; arrival:float; duration:float; priority:int=0; fail_attempts:int=0; max_retries:int=0; backoff:float=1.0; attempts:int=0; first_start:float|None=None; completed:float|None=None

def simulate(rows,workers=2,starvation=10):
 jobs=[Job(**r) for r in rows]; events=[]; seq=0
 for j in jobs: heapq.heappush(events,(j.arrival,0,seq,'arrival',j)); seq+=1
 ready=[]; running={}; now=0.; busy=0.; waits=[]; exhausted=[]
 while events or ready or running:
  if not ready or len(running)>=workers:
   if not events: break
   now=max(now,events[0][0])
   same=[]
   while events and events[0][0]<=now: same.append(heapq.heappop(events))
   for t,_,_,kind,j in same:
    if kind in ('arrival','retry'): heapq.heappush(ready,QItem((-j.priority,t,j.id),j))
    elif kind=='done':
     running.pop(j.id,None); busy+=j.duration; failed=j.attempts<=j.fail_attempts
     if failed and j.attempts<=j.max_retries:
      delay=j.backoff*(2**(j.attempts-1)); heapq.heappush(events,(now+delay,1,seq,'retry',j)); seq+=1
     elif failed: exhausted.append(j.id); j.completed=now
     else: j.completed=now
  while ready and len(running)<workers:
   item=heapq.heappop(ready); j=item.job; j.attempts+=1
   if j.first_start is None: j.first_start=now; waits.append(now-j.arrival)
   running[j.id]=j; heapq.heappush(events,(now+j.duration,2,seq,'done',j)); seq+=1
 makespan=max([j.completed or 0 for j in jobs],default=0)-min([j.arrival for j in jobs],default=0)
 completed=sum(1 for j in jobs if j.completed is not None and j.id not in exhausted)
 return {'jobs':len(jobs),'completed':completed,'exhausted':exhausted,'makespan':makespan,'throughput_per_time':completed/makespan if makespan>0 else 0,'mean_queue_latency':sum(waits)/len(waits) if waits else 0,'max_queue_latency':max(waits,default=0),'utilization':busy/(workers*makespan) if makespan>0 else 0,'starved':[j.id for j in jobs if j.first_start is not None and j.first_start-j.arrival>starvation],'attempts':{j.id:j.attempts for j in jobs}}
