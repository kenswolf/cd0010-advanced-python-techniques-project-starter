"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import datetime_to_str
import datetime


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, name='', diameter=float('nan'), pha=False):
        """Create a new `NearEarthObject`.

        :param info: The four keyword arguments supplied to the constructor are 
                     - its primary designation (required, unique), 
                     - IAU name (optional), 
                     - diameter in kilometers (optional - sometimes unknown), 
                     - whether it's marked as potentially hazardous to Earth  (optional)
        """
        self.designation = designation
        self.name = name
        self.diameter = diameter
        self.hazardous = pha

        #assert(type(self.designation) == str)
        #assert(self.name is None or type(self.name) == str)
        #assert(type(self.diameter) == float)
        #assert(type(self.hazardous) == bool)

        # Create an empty initial collection of linked approaches.
        self.approaches = set()

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return trim(self.designation + ' :  ' + name)

    def __str__(self):
        """Return `str(self)`, a humanreadable string representation of this object."""

        hazardous = 'is potentially hazardous' if self.hazardous else 'is not potentially hazardous'

        return f"NEO {self.designation!r} ({self.name!r}) has a diameter of {self.diameter:.3f} km and " + hazardous

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""

        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def to_json(self):
        """Return `to_json(self)`, a json string snippet representation of this object."""
        
        return {
            'designation': self.designation,
            'name': self.name,
            'diameter_km': self.diameter,
            'potentially_hazardous': self.hazardous
        }


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, time=None, distance=0.0, velocity=0.0):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        self._designation = designation
        self.time = time
        self.distance = distance
        self.velocity = velocity

        #assert(type(self._designation) == str)
        #assert(type(self.time) == datetime.datetime)
        #assert(type(self.distance) == float)
        #assert(type(self.velocity) == float)

        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`, a humanreadable string representation of this object."""

        return f"On {self.time_str!r}, NEO {self.neo.designation!r} ({self.neo.name!r})" \
               f" approaches Earth at a distance of {self.distance:.2f} and a velocity o {self.velocity:.2f}  km/s."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""

        return f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, " \
               f"velocity={self.velocity:.2f}, neo={self.neo!r})"

    def to_json(self):
        """Return `to_json(self)`, a json string snippet representation of this object."""
        
        return {
            'datetime_utc': datetime_to_str(self.time),
            'distance_au': self.distance,
            'velocity_km_s': self.velocity,
            'neo': self.neo.to_json()
        }
