"""Handling of time"""
import asyncio
from typing import Coroutine
from missionlib.commons import Spacecraft
from spacelib.telemetry import colorlog
log = colorlog.getLogger(__name__)


def timer(s: Spacecraft, seconds) -> Coroutine:
    """Wait for specified in-game seconds.
    
    Since kRPC waits are blocking, waiting is done using an extra thread.
    
    Example uses:
        ```
        # wait asynchronously and proceed to the next line after the wait.
        await timer(s, seconds)
        
        # start the timer, and later make sure that the time has passed.
        timer_future = asyncio.create_task(timer(s, seconds))
        do_something_else()
        await timer_future
        
        
        ```

    Args:
        s (Spacecraft): Spacecraft object
        seconds (float): seconds to wait

    Returns:
        Coroutine: coroutine to wait
    """
    t0 = s.sc.ut
    log.debug('Timer starts with %s seconds', seconds)
    tf = t0 + float(seconds)
    t = s.conn.get_call(getattr, s.sc, 'ut')  # in-game universal time
    expr = s.conn.krpc.Expression.greater_than(
        s.conn.krpc.Expression.call(t),
        s.conn.krpc.Expression.constant_double(tf))
    def _wait():
        event = s.conn.krpc.add_event(expr)
        with event.condition:
            event.wait()
    return asyncio.to_thread(_wait)
