"""Handling of time"""
import asyncio
from typing import Coroutine
from spacelib.types import FlightProperty, OrbitProperty, Spacecraft
from spacelib.telemetry import colorlog
logger = colorlog.getLogger(__name__)


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
        Coroutine: coroutine to wait or create a task
    """
    t0 = s.sc.ut
    logger.timing('Timer starts with %s seconds', seconds)
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


def until(s: Spacecraft, target:float, decreasing=False, **kwargs) -> Coroutine:
    """wait until (greater than or equal) target condition is met.

    Args:
        s (Spacecraft): Spacecraft object
        target (float): wait until this value is reached
        flight (str): keywords found in spacelib.types.FlightProperty
        time (str): relative, absolute
        orbit (str): keywords found in spacelib.types.OrbitProperty

    Returns:
        Coroutine: Coroutine to await or create a task
    """
    source = None
    if 'flight' in kwargs:
        flight = s.ves.flight()
        keyword = kwargs['flight']
        if keyword not in dir(FlightProperty):
            raise KeyError('Unknown flight keyword:', keyword)
        source = s.conn.get_call(getattr, flight, keyword)
    
    elif 'orbit' in kwargs:
        orbit = s.ves.orbit
        keyword = kwargs['orbit']
        if keyword not in dir(OrbitProperty):
            raise KeyError('Unknown orbit keyword:', keyword)
        source = s.conn.get_call(getattr, orbit, keyword)
    
    elif 'time' in kwargs:
        t0 = s.sc.ut
        keyword = 'time'
        if kwargs['time'] == 'relative':
            target = t0 + target
        elif kwargs['time'] == 'absolute':
            raise NotImplementedError
        else:
            raise KeyError("Source not found")
        source = s.conn.get_call(getattr, s.sc, 'ut')
    
    else:
        raise KeyError("Source not found")
    
    if decreasing:
        expr = s.conn.krpc.Expression.less_than_or_equal(
            s.conn.krpc.Expression.call(source),
            s.conn.krpc.Expression.constant_double(float(target))
        )
    else:
        expr = s.conn.krpc.Expression.greater_than_or_equal(
            s.conn.krpc.Expression.call(source),
            s.conn.krpc.Expression.constant_double(float(target))
        )
    
    def _wait():
        event = s.conn.krpc.add_event(expr)
        logger.timing('Waiting for %s to be %f', keyword, target)
        with event.condition:
            event.wait()
    return asyncio.to_thread(_wait)
