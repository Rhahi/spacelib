"""Newton 2

Extended main engine
Two SRB stages, no payload.
Intended for 140 km altitude with no extra payload

https://ksp.rhahi.space/mission/plans/suborbital/newton
"""

import asyncio
from enum import IntEnum
from missionlib.commons import Spacecraft
from spacelib.timing import timer, until
from spacelib.types import FlightProperty
from spacelib.telemetry import colorlog
logging = colorlog.getLogger(__name__, colorlog.ALL)


async def main(s: Spacecraft):
    s.ves.control.throttle = 1.0
    s.ves.control.toggle_action_group(ActionGroup.IGNITE_0A_DECOUPLE_BASE)
    await timer(s, 1.4)
    s.ves.control.toggle_action_group(ActionGroup.IGNITE_0B_DECOUPLE_0A)
    await timer(s, 1.1)
    s.ves.control.toggle_action_group(ActionGroup.IGNITE_1A)
    await timer(s, 0.3)
    s.ves.control.toggle_action_group(ActionGroup.DECOUPLE_0B)
    await timer(s, 44)
    s.ves.control.toggle_action_group(ActionGroup.IGNITE_1B)
    await timer(s, 0.1)
    s.ves.control.toggle_action_group(ActionGroup.DECOUPLE_1A)
    await until(s, target=140e+3, flight=FlightProperty.bedrock_altitude)
    s.ves.control.toggle_action_group(ActionGroup.DECOUPLE_1B)
    await until(s, target=140e+3, decreasing=True, flight=FlightProperty.bedrock_altitude)
    s.ves.control.toggle_action_group(ActionGroup.ARM_CHUTE)


class ActionGroup(IntEnum):
    IGNITE_0A_DECOUPLE_BASE = 1
    IGNITE_0B_DECOUPLE_0A = 2
    IGNITE_1A = 3
    DECOUPLE_0B = 4
    IGNITE_1B = 5
    DECOUPLE_1A = 6
    DECOUPLE_1B = 7
    ARM_CHUTE = 8
    

if __name__ == "__main__":
    spacecraft = Spacecraft("Newton 2")
    try:
        asyncio.run(main(spacecraft))
        good_termination = True
        logging.system("End of instructions reached")
    except KeyboardInterrupt as e:
        good_termination = True
        logging.system("Cancelled by user")
        raise e
    finally:
        logging.system("Terminated")
        spacecraft.conn.close()
