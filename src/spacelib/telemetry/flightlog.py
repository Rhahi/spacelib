"""Collect sensor values and store them for science."""
import asyncio
import pandas as pd
from spacelib.types import Spacecraft, FlightProperty, Stream
from spacelib.telemetry.colorlog import getLogger
logger = getLogger(__name__)


class FlightDataCollector():
    def __init__(self, s: Spacecraft, *args) -> None:
        logger.trace("initializing flight data collection")
        self.keywords = [k for k in args if isinstance(k, str) and hasattr(FlightProperty, k)]
        logger.trace("number of flight keywords used: %d", len(self.keywords))
        self.spacecraft = s
        self.data = {k: [] for k in self.keywords}
        self.data['time'] = []
        self.collector: Stream = None
        self.call = None
        self.start_time = 0.
        self.last_time = 0.
        self.running = False


    def start(self, duration=None):
        logger.info("starting data collection")
        s = self.spacecraft
        flight = s.ves.flight()
        collector = s.conn.add_stream(getattr, s.sc, 'ut')
        self.start_time = collector()
        self.last_time = collector()
        self.running = True
        self.call = {k: s.conn.add_stream(getattr, flight, k) for k in self.keywords}
        
        logger.trace("initializing calls")
        for k in self.keywords:
            self.call[k]()
        
        def log_data(now):
            if duration and self.start_time + duration < now:
                logger.trace("flight data collection timeout")
                self.stop()
            self.last_time = now
            self.data['time'].append(now)
            for k in self.keywords:
                value = self.call[k]()
                self.data[k].append(value)
        collector.add_callback(log_data)
        self.collector = collector
        
    
    def stop(self):
        if self.running:
            duration = self.last_time - self.start_time
            logger.info("flight data collection stopped after %s seconds", duration)
            self.collector.remove()
            self.running = False
    
    
    def save(self, outfile):
        logger.system("Starting data save, this may take some time...")
        if len(self.data) > 0:
            df = pd.DataFrame.from_dict(self.data)
            df.to_csv(outfile, sep=';')
            logger.ok("data saved at %s", outfile)
        else:
            logger.warning("flight data collection data is empty, skipping save")


async def collect_flight_data(s: Spacecraft, *args, duration=None, file_output=None):
    logger.warning("This method of collecting data is deprecated. Use FlightDataCollector class.")
    logger.trace("initializing flight data collection (FDC)")
    flight = s.ves.flight()
    keywords = [k for k in args if isinstance(k, str) and hasattr(FlightProperty, k)]
    logger.trace("number of FDC keywords: %d", len(keywords))
    now = s.conn.add_stream(getattr, s.sc, 'ut')
    call = {k: s.conn.add_stream(getattr, flight, k) for k in keywords}
    data = {k: [] for k in keywords}
    data['time'] = []
    
    start_time = now()
    end_time = start_time + duration
    def send_log_output():
        if file_output:
            save_flight_data(file_output, data)
        return data
    
    try:
        await _log_flight_data(call, now, data, keywords, end_time)
    
    except (asyncio.CancelledError, asyncio.TimeoutError):
        logger.trace("flight data collection cancelled")
        return send_log_output()
    logger.trace("flight data collection finished")
    return send_log_output()


async def _log_flight_data(call, now, data, keywords, end_time):
    logger.info("starting data collection")
    duplicate_count = 0
    last_time = 0
    while True:
        time = now()
        if time > end_time:
            logger.trace("flight data collection timeout")
            break
        if not last_time < time:
            duplicate_count += 1
            continue
        last_time = time
        
        try:
            # use a try-finally block here to ensure that the data is complete
            pass
        finally:
            data['time'].append(time)
            for k in keywords:
                data[k].append(call[k]())
        await asyncio.sleep(0)
    logger.trace("flight data collection statistics")
    logger.trace("  duplicate count %d", duplicate_count)
    logger.trace("  duration %f", end_time - time)
    if end_time - time > 1:
        logger.trace("  duplicates per second %f", duplicate_count / end_time - time)

def save_flight_data(file, data):
    logger.warning("Starting data save, this may take some time...")
    if len(data) > 0:
        df = pd.DataFrame.from_dict(data)
        df.to_csv(file, sep=';')
        logger.info("data saved at %s", file)
    else:
        logger.warning("sensor data is empty, no data is saved")

