"""Collect sensor values and store them for science."""
import asyncio
import pandas as pd
from spacelib.types import Spacecraft, FlightProperty
from spacelib.telemetry.colorlog import getLogger
logger = getLogger(__name__)


async def collect_flight_data(s: Spacecraft, *args, duration=None, file_output=None):
    logger.trace("initializing data collection")
    flight = s.ves.flight()
    keywords = [k for k in args if k is str and hasattr(FlightProperty, k)]
    time = s.conn.add_stream(getattr, s.sc, 'ut')
    call = {k: s.conn.add_stream(getattr, flight, k) for k in keywords}
    data = {k: [] for k in keywords}
    data['time'] = []
    
    last_time = 0
    start_time = time()
    try:
        logger.info("starting data collection")
        while True:
            t = time()
            if start_time + duration > t:
                break  # check for timeout
            if not last_time < t:
                continue  # do not parse more than once a tick
            last_time = t
            
            try:
                # use a try-finally block here to ensure that the data is complete
                pass
            finally:
                data['time'].append(t)
                for k in keywords:
                    data[k].append(call[k]())
            asyncio.sleep(0)
    except (asyncio.CancelledError, asyncio.TimeoutError):
        if file_output:
            save_flight_data(file_output, data)
        return data
    if file_output:
        save_flight_data(file_output, data)
    return data


def save_flight_data(file, data):
    logger.warning("Starting data save, this may take some time...")
    if len(data) > 0:
        df = pd.DataFrame.from_dict(data)
        df.to_csv(file, sep=';')
        logger.info("data saved at %s", file)
    else:
        logger.warning("sensor data is empty, no data is saved")
