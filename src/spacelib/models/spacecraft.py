from spacelib.types import Client, Vessel, Part
from spacelib.rocketry import safe_deltav


class UnknownStageError(Exception):
    pass


class SpaceCraft():
    """Model spacecraft's macroscopic features with simplified parameters"""
    def __init__(self) -> None:
        self.stages = []
        self.mass = 0
        self.dry_mass = 0

    def add(self, stage: 'Stage') -> None:
        """Add a stage into spacecraft model
        
        Adding a stage must be done from final stage -> initial stage order.
        """
        self.stages.append(stage)
        
    def deltav(self, stage_number: int) -> float:
        """DeltaV of a given stage"""
        pass
    
def load_vehicle_from_krpc(ves: 'Vessel') -> 'SpaceCraft':
    """
    using stage that is going to be decoupled,
    if the decoupled stage has more than 100 m/s dV then treat it as a full stage.
    otherwise, save the stage information for total mass but discard for staging.
    Next stage that has enough dV will be treated as a full stage.
    When the rocket reaches the final stage, the mass shall be treated as payload.
    """
    num_stages = ves.control.current_stage()
    spacecraft = SpaceCraft()
    parked_stage = None
    for s in reversed(range(num_stages)):
        parts = ves.parts.in_decouple_stage(s)
        stage = _parse_stage(parts)
        if stage.thrust > 0:
            if parked_stage is None:
                spacecraft.add(stage)
            else:
                spacecraft.add(parked_stage + stage)
                parked_stage = None
            continue
        if stage.thrust == 0:
            if parked_stage is None:
                parked_stage = stage
            else:
                parked_stage += stage
            continue
        raise UnknownStageError

def _parse_stage(parts: "list['Part']") -> 'Stage':
    mass = 0
    dry_mass = 0
    engine_mass = 0
    max_isp = 0
    total_thrust = 0
    for p in parts:
        mass += p.mass
        dry_mass += p.dry_mass
        if p.engine is not None:
            isp = p.engine.vacuum_specific_impulse
            if isp > max_isp:
                max_isp = isp
            total_thrust += p.engine.max_thrust
            engine_mass += p.mass
    return Stage(mass, dry_mass, engine_mass)

class Stage():
    """Python object for rocket stage"""
    def __init__(self,
                 mass: float = 0,
                 dry_mass: float = 0,
                 engine_mass: float = 0,
                 thrust: float = 0,
                 isp: float = 0) -> None:
        self.mass = mass
        self.dry_mass = dry_mass
        self.thrust = thrust
        self.isp = isp
        self.engine_mass = engine_mass
        self.structural_ratio = self._calculate_structural_ratio(mass, dry_mass, engine_mass)
        self.deltav = None

    def __add__(self, other: 'Stage'):
        self.mass += other.mass
        self.dry_mass += other.dry_mass
        self.thrust += other.thrust
        self.isp = max(other.isp, self.isp)
        self.engine_mass += other.engine_mass
        self.structural_ratio = self._calculate_structural_ratio(self.mass, self.dry_mass, self.engine_mass)
        self.deltav = None

    def __iadd__(self, other: 'Stage'):
        return self.__add__(other)

    def _calculate_structural_ratio(self, mass, dry_mass, engine_mass):
        """Calculate structural ratio
        
        Structrual ratio is used to calculate how much fuel and dead weight would be added
        to a spacecraft if the spacecraft were to be expanded (adding fuel tanks).
        when mass of X is being added, newly added fuel is (1-S)*X where S is the structural ratio.
        """
        if mass - engine_mass > 0:
            return (dry_mass - engine_mass) / (mass - engine_mass)
        return 0.15  # default structural ratio when it is not calculatable
