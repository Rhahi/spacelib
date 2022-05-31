"""Newton Experimental

Not designed for efficient flight; for testing purposes only.

https://ksp.rhahi.space/mission/plans/suborbital/newton
"""

import asyncio
from spacelib.telemetry import colorlog
from spacelib.timing import timer
from missionlib.commons import Spacecraft
logging = colorlog.getLogger(__name__, colorlog.ALL)


async def main(s: Spacecraft):
    logging.info("Setting throttle")
    s.ves.control.throttle = 1.0
    logging.info("Ignition")
    s.ves.control.activate_next_stage()
    await timer(s, 0.1)
    logging.info("Relase")
    s.ves.control.activate_next_stage()
    

if __name__ == "__main__":
    spacecraft = Spacecraft("Newton X")
    good_termination = False
    try:
        asyncio.run(main(spacecraft))
        good_termination = True
        logging.system("End of instructions reached, terminated")
    finally:
        if not good_termination:
            logging.system("Errors occured, terminated.")
        spacecraft.conn.close()
