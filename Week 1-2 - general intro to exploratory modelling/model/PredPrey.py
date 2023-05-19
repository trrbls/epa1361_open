"""
Python model 'PredPrey.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.statefuls import Integ
from pysd import Component

__pysd_version__ = "3.10.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 0,
    "final_time": lambda: 365,
    "time_step": lambda: 0.25,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL_TIME", units="Day", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL_TIME", units="Day", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="Day",
    limits=(0.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME_STEP",
    units="Day",
    limits=(0.0, np.nan),
    comp_type="Constant",
    comp_subtype="Normal",
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="predator_growth",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"predator_efficiency": 1, "predators": 1, "prey": 1},
)
def predator_growth():
    return predator_efficiency() * predators() * prey()


@component.add(
    name="predators",
    limits=(0.0, np.nan),
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_predators": 1},
    other_deps={
        "_integ_predators": {
            "initial": {"initial_predators": 1},
            "step": {"predator_growth": 1, "predator_loss": 1},
        }
    },
)
def predators():
    return _integ_predators()


_integ_predators = Integ(
    lambda: predator_growth() - predator_loss(),
    lambda: initial_predators(),
    "_integ_predators",
)


@component.add(
    name="prey",
    limits=(0.0, np.nan),
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_prey": 1},
    other_deps={
        "_integ_prey": {
            "initial": {"initial_prey": 1},
            "step": {"prey_growth": 1, "prey_loss": 1},
        }
    },
)
def prey():
    return _integ_prey()


_integ_prey = Integ(
    lambda: prey_growth() - prey_loss(), lambda: initial_prey(), "_integ_prey"
)


@component.add(
    name="prey_growth",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"prey_birth_rate": 1, "prey": 1},
)
def prey_growth():
    return prey_birth_rate() * prey()


@component.add(
    name="predator_loss",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"predator_loss_rate": 1, "predators": 1},
)
def predator_loss():
    return predator_loss_rate() * predators()


@component.add(name="predator_efficiency", comp_type="Constant", comp_subtype="Normal")
def predator_efficiency():
    return 0.002


@component.add(
    name="prey_loss",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"predation_rate": 1, "predators": 1, "prey": 1},
)
def prey_loss():
    return predation_rate() * predators() * prey()


@component.add(name="initial_predators", comp_type="Constant", comp_subtype="Normal")
def initial_predators():
    return 20


@component.add(name="initial_prey", comp_type="Constant", comp_subtype="Normal")
def initial_prey():
    return 50


@component.add(name="predator_loss_rate", comp_type="Constant", comp_subtype="Normal")
def predator_loss_rate():
    return 0.06


@component.add(name="prey_birth_rate", comp_type="Constant", comp_subtype="Normal")
def prey_birth_rate():
    return 0.025


@component.add(name="predation_rate", comp_type="Constant", comp_subtype="Normal")
def predation_rate():
    return 0.0015
