from utils import cart2pol
from windfields import WindField
from sympy import Point2D


class AutoNavigator:
    def __init__(self, wind_forecast_model: WindField) -> None:
        self.wind_forecast_model = wind_forecast_model

    def suggested_heading(
        self, coords_now: Point2D, coords_target: Point2D, t_now: float
    ):
        raise NotImplementedError


class BasicAutoNavigator(AutoNavigator):
    """So basic that it literally returns the direct heading from
    the current coordinates to the target as if this is not a boat but a car.
    """

    def suggested_heading(
        self, coords_now: Point2D, coords_target: Point2D, t_now: float
    ) -> float:
        coords_to_target = coords_target - coords_now
        _, heading_in_radians = cart2pol(coords_to_target.x, coords_to_target.y)
        return heading_in_radians
