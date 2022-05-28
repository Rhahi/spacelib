"""Newton 1

Two SRB stages, no payload.
Intended for 100 km altitude with no extra payload

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
    logging.info("Booster ignition and release")
    s.ves.control.activate_next_stage()
    await timer(s, 0.8)
    logging.info("Second booster ignition and separation")
    s.ves.control.activate_next_stage()
    await timer(s, 0.6)
    logging.info("Main engine ignition")
    s.ves.control.activate_next_stage()
    await timer(s, 0.2)
    logging.info("Decouple")
    s.ves.control.activate_next_stage()
    

if __name__ == "__main__":
    spacecraft = Spacecraft("Newton 1")
    good_termination = False
    try:
        asyncio.run(main(spacecraft))
        good_termination = True
        logging.system("End of instructions reached, terminated")
    finally:
        if not good_termination:
            logging.system("Errors occured, terminated.")
        spacecraft.conn.close()
