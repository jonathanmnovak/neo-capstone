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
from helpers import cd_to_datetime, datetime_to_str


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

    def __init__(self, designation, name=None, diameter=float('nan'), hazardous=False):
        """Create a new `NearEarthObject`.

        :param designation: The primary designation for this NearEarthObject. Required and string value
        :param name: The IAU name for this NearEarthObject. Optional and string value with a default of None.
        :param diameter: The diameter, in kilometers, of this NearEarthObject. A float value with a default of None.
        :param hazardous: Whether or not this NearEarthObject is potentially hazardous. Default of False.
        """

        assert type(designation) == str, f'{designation} is not a string value'
        assert (type(name) == str) or (name is None), f'{name} is not a string value'
        assert type(diameter) == float, f'{diameter} is not a float value'
        assert type(hazardous) == bool, f'{hazardous} is not a boolean value'

        self.designation = designation
        self.name = name
        self.diameter = diameter
        self.hazardous = hazardous

        # Create an empty initial collection of linked approaches.
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""

        if self.name is not None:
            fullname = f'{self.designation} ({self.name})'
        else:
            fullname = self.designation
        return fullname

    def __str__(self):
        """Return `str(self)`."""

        if self.hazardous:
            is_hazardous = 'is'
        else:
            is_hazardous = 'is not'

        return f'NEO {self.fullname} has diameter of {self.diameter:.3f} km and {is_hazardous} potentially hazardous'

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")

    def serialize(self, csv_output=True):
        """Serialize objects to better support writing to CSV and JSON. Returns a dictionary with the correctly
        formatted output
        :param csv_output: Boolean to serialize based on the csv output rules if True. If False, then assumes json rules
        """

        d = {'designation': self.designation}

        if self.name is None:
            d['name'] = ''
        else:
            d['name'] = self.name

        if self.diameter == float('nan') and csv_output:
            d['diameter_km'] = ''
        else:
            d['diameter_km'] = self.diameter
        if self.hazardous is False and csv_output:
            d['potentially_hazardous'] = 'False'
        elif self.hazardous is True and csv_output:
            d['potentially_hazardous'] = 'True'
        else:
            d['potentially_hazardous'] = self.hazardous

        return d


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, time, distance, velocity, designation=''):
        """Create a new `CloseApproach`.

        :param time: The date and time, in UTC, at which the NEO passes closest to Earth.
        :param distance: The nominal approach distance, in astronomical units, of the NEO to Earth at the closest point.
        :param velocity: The velocity, in kilometers per second, of the NEO relative to Earth at the closest point.
        :param designation: Referenced NEO
        """

        self._designation = designation
        self.time = cd_to_datetime(time)
        self.distance = distance
        self.velocity = velocity

        # Create an attribute for the referenced NEO, originally None.
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
        """Return `str(self)`."""

        return f'On {self.time_str}, "{self.neo.fullname}" approaches Earth at a distance of {self.distance:.2f} au ' \
               f'and a velocity of {self.velocity:.2f} km/s. '

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

    def serialize(self):
        """Returns a dictionary with the correctly formatted output"""

        return{'datetime_utc': datetime_to_str(self.time), 'distance_au': self.distance, 'velocity_km_s': self.velocity}
