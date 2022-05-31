"""Bring out kRPC custom types for development environment to parse"""
from typing import TYPE_CHECKING
from spacelib.properties import *
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
