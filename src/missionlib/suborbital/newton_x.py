"""Newton Experimental

https://ksp.rhahi.space/mission/plans/suborbital/newton
"""

import asyncio
from spacelib.telemetry import colorlog
from spacelib.time import timer
from missionlib.commons import Spacecraft
logging = colorlog.getLogger(__name__, colorlog.ALL)


async def main(s: Spacecraft):
    logging.info("Setting throttle")
    s.ves.control.throttle = 1.0
    logging.info("Ignition")
    logging.debug("%f before ignition", s.sc.ut)
    s.ves.control.activate_next_stage()
    logging.debug("%f after ignition, before timer (expect 0)", s.sc.ut)
    await timer(s, 0.1)
    logging.debug("%f after timer, before release (expect 0.1)", s.sc.ut)
    logging.info("Relase")
    s.ves.control.activate_next_stage()
    logging.debug("%f after release (expect 0)", s.sc.ut)
    

if __name__ == "__main__":
    spacecraft = Spacecraft("Newton I")
    good_termination = False
    try:
        asyncio.run(main(spacecraft))
        good_termination = True
        logging.system("End of instructions reached, terminated")
    finally:
        if not good_termination:
            logging.system("Errors occured, terminated.")
        spacecraft.conn.close()
