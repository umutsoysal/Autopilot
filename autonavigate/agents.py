from autonavigators import AutoNavigator, BasicAutoNavigator
from utils import pol2cart
from windfields import WindAtPoint
import math
from sympy import Point2D


class PolarDiagram:
    def __call__(self, angle_to_wind: float, wind_speed: float) -> float:
        raise NotImplementedError


class UniformPolarDiagram(PolarDiagram):
    """A simple polar diagram that returns the same speed in knots, regardless of wind conditions"""

    static_speed: float

    def __init__(self, static_speed: float) -> None:
        self.static_speed = static_speed

    def __call__(self, angle_to_wind: float, wind_speed: float) -> float:
        return self.static_speed


class PolarDiagramFactory:
    supported_wind_field_types = {"Uniform"}

    def make_polar_diagram(self, config: dict) -> PolarDiagram:
        wind_field_type = config["type"]
        if not wind_field_type in self.supported_wind_field_types:
            raise ValueError(
                f"{wind_field_type} is not one of the supported wind field types, which are: {self.supported_wind_field_types}"
            )

        if wind_field_type == "Uniform":
            return UniformPolarDiagram(static_speed=config["sog"])


class Boat:
    name: str
    heading: float
    coords: Point2D
    target_coords: Point2D  # TODO: In the future, this can be a list of checkpoints
    polar_diagram: PolarDiagram
    autonavigator: AutoNavigator
    t_now: float
    # TODO: move this to autonavigator heading_plan: Dict[float, Tuple[float, Point2D]]

    def __init__(
        self,
        name: str,
        coords_zero: Point2D,
        target_coords: Point2D,
        polar_diagram: PolarDiagram,
        autonavigator: AutoNavigator,
        t_zero: float,
    ) -> None:
        self.name = name
        self.coords = coords_zero
        self.target_coords = target_coords
        self.polar_diagram = polar_diagram
        self.autonavigator = autonavigator
        self.update_heading(t_zero)

    def sail(self, wind_at_agent_coords: WindAtPoint, dt: float) -> None:
        boat_speed = self.polar_diagram(
            self._angle_to_wind(wind_at_agent_coords.twa), wind_at_agent_coords.tws
        )
        self.coords += Point2D(*pol2cart(boat_speed * dt, self.heading))

    def _angle_to_wind(self, twa: float):
        # Both heading and twa has to be in radians
        return abs(self.heading - twa) % math.pi

    def update_heading(self, t_now: float) -> None:
        self.heading = self.autonavigator.suggested_heading(
            self.coords, self.target_coords, t_now
        )


def make_boat(name, config, tzero, wind_field):
    return Boat(
        name,
        coords_zero=Point2D(config["init_coords"]),
        polar_diagram=PolarDiagramFactory().make_polar_diagram(config["polar_diagram"]),
        t_zero=tzero,
        target_coords=Point2D(config["target_coords"]),
        autonavigator=BasicAutoNavigator(wind_field),
    )
