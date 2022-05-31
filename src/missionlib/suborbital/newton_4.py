"""Newton 4

Two stages, with two SRB zeroth stage.
35 sounding rocket and small biological experiment
Intended for 100 km altitude.
Record atmospheric data

https://ksp.rhahi.space/mission/plans/suborbital/newton
"""
import asyncio
from enum import IntEnum
from missionlib.commons import Spacecraft
from spacelib.timing import timer, until
from spacelib.telemetry import colorlog, flightlog
from spacelib.types import FlightProperty, VesselProperty
logging = colorlog.getLogger(__name__, colorlog.ALL)


async def main(s: Spacecraft):
    s.ves.control.throttle = 1.0
    FDC = flightlog.DataCollector(s,
        flight=[FlightProperty.atmosphere_density,
                FlightProperty.drag,
                FlightProperty.bedrock_altitude,
                FlightProperty.true_air_speed],
        vessel=[VesselProperty.mass])
    with FDC.arm('data/newton4.csv'):
        s.ves.control.toggle_action_group(ActionGroup.IGNITE_1)
        await timer(s, 0.2)
        s.ves.control.toggle_action_group(ActionGroup.RELEASE)
        await timer(s, 32.7)
        s.ves.control.toggle_action_group(ActionGroup.IGNITE_2)
        await timer(s, 0.2)
        s.ves.control.toggle_action_group(ActionGroup.DECOUPLE_1)
        await until(s, 100e+3, flight=FlightProperty.bedrock_altitude)
    await until(s, 100e+3, flight=FlightProperty.bedrock_altitude, decreasing=True)
    s.ves.control.toggle_action_group(ActionGroup.DEPLOY)
    

class ActionGroup(IntEnum):
    RELEASE = 11
    IGNITE_1 = 21
    DECOUPLE_0 = 22
    IGNITE_2 = 23
    DECOUPLE_1 = 24
    DEPLOY = 31
    

if __name__ == "__main__":
    spacecraft = Spacecraft("Newton 3")
    try:
        asyncio.run(main(spacecraft))
        logging.system("End of instructions reached")
    finally:
        logging.system("Terminated")
        spacecraft.conn.close()
