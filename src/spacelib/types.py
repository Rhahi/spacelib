"""Bring out kRPC custom types for development environment to parse"""
from typing import TYPE_CHECKING
from dataclasses import dataclass
import krpc


if TYPE_CHECKING:
    from krpc.client import Client
    from krpc.stream import Stream
    from missionlib.commons import Spacecraft
    from krpc.spacecenter import SpaceCenter
    Part = SpaceCenter.Part
    Vessel = SpaceCenter.Vessel
    ReferenceFrame = SpaceCenter.ReferenceFrame
    CelestialBody = SpaceCenter.CelestialBody
    AutoPilot = SpaceCenter.AutoPilot
    Engine = SpaceCenter.Engine
else:
    Client = None
    Stream = None
    Spacecraft = None
    SpaceCenter = None
    Part = None
    Vessel = None
    ReferenceFrame = None
    CelestialBody = None
    AutoPilot = None
    Engine = None


@dataclass
class FlightProperty:
    """Keywords found in Vessel.flight()"""
    angle_of_attack = 'angle_of_attack'
    atmosphere_density = 'atmosphere_density'
    ballistic_coefficient = 'ballistic_coefficient'
    bedrock_altitude = 'bedrock_altitude'  # sealevel altitude
    drag = 'drag'
    drag_coefficient = 'drag_coefficient'
    dynamic_pressure = 'dynamic_pressure'
    elevation = 'elevation'
    equivalent_air_speed = 'equivalent_air_speed'
    g_force = 'g_force'
    heading = 'heading'
    latitude = 'latitude'
    lift = 'lift'
    lift_coefficient = 'lift_coefficient'
    longitude = 'longitude'
    mach = 'mach'
    mean_altitude = 'mean_altitude'
    pitch = 'pitch'
    reynolds_number = 'reynolds_number'
    roll = 'roll'
    sideslip_angle = 'sideslip_angle'
    speed_of_sound = 'speed_of_sound'
    stall_fraction = 'stall_fraction'
    static_air_temperature = 'static_air_temperature'
    static_pressure = 'static_pressure'
    static_pressure_at_msl = 'static_pressure_at_msl'
    surface_altitude = 'surface_altitude'
    terminal_velocity = 'terminal_velocity'
    thrust_specific_fuel_consumption = 'thrust_specific_fuel_consumption'
    total_air_temperature = 'total_air_temperature'
    true_air_speed = 'true_air_speed'

@dataclass
class OrbitProperty:
    """Properties found in Vessel.orbit, excluding ones that require reference frame"""
    apoapsis = 'apoapsis'
    apoapsis_altitude = 'apoapsis_altitude'
    argument_of_periapsis = 'argument_of_periapsis'
    eccentric_anomaly = 'eccentric_anomaly'
    eccentricity = 'eccentricity'
    epoch = 'epoch'
    inclination = 'inclination'
    longitude_of_ascending_node = 'longitude_of_ascending_node'
    mean_anomaly = 'mean_anomaly'
    mean_anomaly_at_epoch = 'mean_anomaly_at_epoch'
    orbital_speed = 'orbital_speed'
    periapsis = 'periapsis'
    periapsis_altitude = 'periapsis_altitude'
    period = 'period'
    radius = 'radius'
    semi_major_axis = 'semi_major_axis'
    speed = 'speed'
    time_to_apoapsis = 'time_to_apoapsis'
    time_to_soi_change = 'time_to_soi_change'
    true_anomaly = 'true_anomaly'
