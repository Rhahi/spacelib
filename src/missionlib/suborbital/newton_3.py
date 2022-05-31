"""Newton 3

Two stages, with two SRB zeroth stage.
170 sounding rocket payload
Intended for 70 km altitude.
Record atmospheric data

https://ksp.rhahi.space/mission/plans/suborbital/newton
"""

import asyncio
from enum import IntEnum
from missionlib.commons import Spacecraft
from spacelib.timing import timer, until
from spacelib.telemetry import colorlog, flightlog
from spacelib.types import FlightProperty
logging = colorlog.getLogger(__name__, colorlog.ALL)


async def main(s: Spacecraft):
    s.ves.control.throttle = 1.0
    collector = flightlog.FlightDataCollector(s,
        FlightProperty.atmosphere_density,
        FlightProperty.drag,
        FlightProperty.bedrock_altitude,
        FlightProperty.true_air_speed)
    collector.start()
    s.ves.control.toggle_action_group(ActionGroup.IGNITE_0A_RELEASE)
    await timer(s, 1.5)
    s.ves.control.toggle_action_group(ActionGroup.IGNITE_0B_DECOUPLE)
    await timer(s, 1.3)
    s.ves.control.toggle_action_group(ActionGroup.IGNITE_1)
    await timer(s, 0.1)
    s.ves.control.toggle_action_group(ActionGroup.DECOUPLE_0)
    await timer(s, 47)
    s.ves.control.toggle_action_group(ActionGroup.IGNITE_2)
    await timer(s, 0.1)
    s.ves.control.toggle_action_group(ActionGroup.DECOUPLE_1)
    await until(s, 70e+3, flight=FlightProperty.bedrock_altitude)
    collector.stop()
    collector.save('data/Newton3.csv')
    

class ActionGroup(IntEnum):
    IGNITE_0A_RELEASE = 11
    IGNITE_0B_DECOUPLE = 12
    IGNITE_1 = 21
    DECOUPLE_0 = 22
    IGNITE_2 = 23
    DECOUPLE_1 = 24
    

if __name__ == "__main__":
    spacecraft = Spacecraft("Newton 3")
    try:
        asyncio.run(main(spacecraft))
        logging.system("End of instructions reached")
    finally:
        logging.system("Terminated")
        spacecraft.conn.close()
