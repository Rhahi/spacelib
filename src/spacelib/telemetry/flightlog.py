"""Collect sensor values and store them for science."""
import asyncio
import pandas as pd
from spacelib.types import Spacecraft, FlightProperty
from spacelib.telemetry.colorlog import getLogger
logger = getLogger(__name__)


async def collect_flight_data(s: Spacecraft, *args, duration=None, file_output=None):
    logger.trace("initializing flight data collection (FDC)")
    flight = s.ves.flight()
    keywords = [k for k in args if type(k) is str and hasattr(FlightProperty, k)]
    logger.trace("number of FDC keywords: %d", len(keywords))
    time = s.conn.add_stream(getattr, s.sc, 'ut')
    call = {k: s.conn.add_stream(getattr, flight, k) for k in keywords}
    data = {k: [] for k in keywords}
    data['time'] = []
    
    last_time = 0
    start_time = time()
    dupliate_count = 0
    
    def send_log_output():
        duration = last_time - start_time
        logger.trace("flight data collection statistics")
        logger.trace("  duplicate count %d", dupliate_count)
        logger.trace("  duration %f", duration)
        if duration > 1:
            logger.trace("  duplicates per second %f", dupliate_count / duration)
        if file_output:
            save_flight_data(file_output, data)
        return data
    
    try:
        logger.info("starting data collection")
        while True:
            t = time()
            if start_time + duration < t:
                logger.trace("flight data collection timeout")
                break
            if not last_time < t:
                dupliate_count += 1
                continue
            last_time = t
            
            try:
                # use a try-finally block here to ensure that the data is complete
                pass
            finally:
                data['time'].append(t)
                for k in keywords:
                    data[k].append(call[k]())
            await asyncio.sleep(0)
    
    except (asyncio.CancelledError, asyncio.TimeoutError):
        logger.trace("flight data collection cancelled")
        return send_log_output()
    logger.trace("flight data collection finished")
    return send_log_output()


def save_flight_data(file, data):
    logger.warning("Starting data save, this may take some time...")
    if len(data) > 0:
        df = pd.DataFrame.from_dict(data)
        df.to_csv(file, sep=';')
        logger.info("data saved at %s", file)
    else:
        logger.warning("sensor data is empty, no data is saved")
