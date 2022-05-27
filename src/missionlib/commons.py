"""Common utility functions and classes shared between all missions"""
import krpc
from spacelib import control


class Spacecraft():
    """A collection of objects to be shared accross a mission"""
    def __init__(self, title: str=None) -> None:
        self.conn = krpc.connect(name=title)
        self.sc = self.conn.space_center
        self.ves = self.sc.active_vessel
        self.events = {}
        self.parts = {}
        self.control = Control(self)

        
class Control():
    def __init__(self, s: Spacecraft) -> None:
        self.SASS = control.SASS(s)
