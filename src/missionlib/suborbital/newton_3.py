"""Newton 2

Extended main engine
Two SRB stages, no payload.
Intended for 140 km altitude with no extra payload

https://ksp.rhahi.space/mission/plans/suborbital/newton
"""

import asyncio
from enum import IntEnum
from missionlib.commons import Spacecraft
from spacelib.time import timer
from spacelib.telemetry import colorlog
logging = colorlog.getLogger(__name__, colorlog.ALL)


async def main(s: Spacecraft):
    s.ves.control.throttle = 1.0
    s.ves.control.toggle_action_group(ActionGroup.IGNITE_0A_RELEASE)
    await timer(s, 1.5)
    s.ves.control.toggle_action_group(ActionGroup.IGNITE_0B_DECOUPLE)
    await timer(s, 1.3)
    s.ves.control.toggle_action_group(ActionGroup.IGNITE_1A)
    await timer(s, 0.1)
    s.ves.control.toggle_action_group(ActionGroup.DECOUPLE_0)
    await timer(s, 47)
    s.ves.control.toggle_action_group(ActionGroup.IGNITE_1B)
    await timer(s, 0.1)
    s.ves.control.toggle_action_group(ActionGroup.DECOUPLE_1A)

class ActionGroup(IntEnum):
    # Stage 0
    IGNITE_0A_RELEASE = 11
    IGNITE_0B_DECOUPLE = 12
    
    # Stage 1
    IGNITE_1A = 21
    DECOUPLE_0 = 22
    IGNITE_1B = 23
    DECOUPLE_1A = 24
    

if __name__ == "__main__":
    spacecraft = Spacecraft("Newton 2")
    try:
        asyncio.run(main(spacecraft))
        logging.system("End of instructions reached")
    finally:
        logging.system("Terminated")
        spacecraft.conn.close()
