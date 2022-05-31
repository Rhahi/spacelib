"""Collect sensor values and store them for science."""
import time
from typing import TextIO
import pandas as pd
from spacelib.types import Spacecraft, FlightProperty, Stream, VesselProperty
from spacelib.telemetry.colorlog import getLogger
logger = getLogger(__name__)


class DataCollector():
    def __init__(self, s: Spacecraft, duration=None, **kwargs) -> None:
        self.spacecraft = s
        self.start_time = 0
        self.last_time = 0
        self.outfile = None
        self.trigger: Stream = None
        self.calls = {}
        self.running = False
        self.keywords = []
        self.duration = duration
        self.data = {'time': []}
        known_modules: 'dict[str, DataModule]' = {
            'flight': FlightDataModule,
            'vessel': VesselDataModule,
        }
        self.modules: 'dict[str, DataModule]'= {}
        for name, properties in kwargs.items():
            if name in known_modules:
                self.modules[name] = known_modules[name](s, *properties)
            else:
                logger.warning("Unknown modules %s ignored", name)

    
    def __enter__(self):
        self.start()
        return self
    
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
        self.save()


    def arm(self, outfile: TextIO):
        return self.arm_save(outfile)
    

    def arm_save(self, outfile: TextIO):
        self.outfile = outfile
        return self
    
    
    def set_duration(self, duration):
        self.duration = duration
    
    
    def start(self):
        logger.info("Starting data collection")
        s = self.spacecraft
        universal_time = s.conn.add_stream(getattr, s.sc, 'ut')
        self.trigger = universal_time
        # set up callbacks
        self.start_time = universal_time()
        self.last_time = self.start_time
        for module in self.modules.values():
            streams = module.get_streams()
            for property_name, func in streams.items():
                logger.info("recording %s", property_name)
                func()  # warm up call. Without this, kRPC does not give values.
                self.calls[property_name] = func
                self.data[property_name] = []
        
        # add callback to kRPC
        def log_data(now):
            if self.duration and self.start_time + self.duration < now:
                logger.trace("Data collection timeout")
                self.stop()
                return
            self.last_time = now
            self.data['time'].append(now)
            for key, func in self.calls.items():
                value = func()
                self.data[key].append(value)
        universal_time.add_callback(log_data)
        self.running = True
    
    
    def stop(self):
        if self.running:
            duration = self.last_time - self.start_time
            data_rows = len(self.data['time'])
            logger.info("%i data collected after %s seconds", data_rows, duration)
            for m in self.modules.values():
                m.remove_streams()
            self.trigger.remove()
            self.running = False
    
    
    def save(self, outfile=None):
        logger.system("Starting data save...")
        if not outfile:
            outfile = self.outfile if self.outfile else f'./data/data_{self.last_time}.csv'
        if len(self.data) > 0:
            t0 = time.time()
            df = pd.DataFrame.from_dict(self.data)
            df.to_csv(outfile, sep=';', index=False)
            tf = time.time()
            logger.ok("Data saved at %s. This operation took %f seconds", outfile, tf - t0)
        else:
            logger.warning("Data collection data is empty, skipping save")


class DataModule():
    def __init__(self, s: Spacecraft):
        self.spacecraft = s
        self.streams = []
        self.keywords = []
        self.source_name = 'Generic:'
        self.source = None
    
    def get_streams(self):
        s = self.spacecraft
        source = self.source
        self.streams = {
            self.source_name+k: s.conn.add_stream(getattr, source, k) for k in self.keywords
        }
        return self.streams
    
    def remove_streams(self):
        for c in self.streams.values():
            c.remove()


class FlightDataModule(DataModule):
    def __init__(self, s: Spacecraft, *args):
        super().__init__(s)
        self.source_name = 'Flight:'
        self.keywords = [k for k in args if hasattr(FlightProperty, k)]
        self.source = s.ves.flight()


class VesselDataModule(DataModule):
    def __init__(self, s: Spacecraft, *args):
        super().__init__(s)
        self.source_name = 'Vessel:'
        self.keywords = [k for k in args if hasattr(VesselProperty, k)]
        self.source = s.ves
