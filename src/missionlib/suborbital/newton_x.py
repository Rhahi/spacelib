"""Newton Experimental

https://ksp.rhahi.space/mission/plans/suborbital/newton
"""

import asyncio
from spacelib.telemetry import colorlog
from spacelib.time import timer
from missionlib.commons import Spacecraft
logging = colorlog.getLogger(__name__, colorlog.DEBUG)


async def main(s: Spacecraft):
    logging.info("Setting throttle")
    s.ves.control.throttle = 1.0
    logging.info("Ignition")
    s.ves.control.activate_next_stage()
    await timer(s, 0.1)
    logging.info("Relase")
    s.ves.control.activate_next_stage()
    

if __name__ == "__main__":
    spacecraft = Spacecraft("Newton I")
    try:
        asyncio.run(main(spacecraft))
        logging.info("End of instructions reached")
    finally:
        logging.info("Terminated")
        spacecraft.conn.close()
