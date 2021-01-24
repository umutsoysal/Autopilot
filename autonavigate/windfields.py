from typing import Tuple, Dict
from utils import polygon2axis_parallel_bbox, regularly_sampled_coords_in_polygon
from sympy import Polygon, Point2D
import math


class WindAtPoint:
    def __init__(self, twa: float, tws: float) -> None:
        self.tws = tws
        self.twa = twa


class WindField:
    def wind_at(self, coordinates: Point2D, time: float) -> WindAtPoint:
        """Get TWA and TWS at a specific location and time"""
        raise NotImplementedError

    def get_wind_data_for_viz(self, time: float) -> Dict[Point2D, WindAtPoint]:
        raise NotImplementedError

    def get_field_bounds(self) -> Dict[str, float]:
        raise NotImplementedError


class StaticInSpaceAndTimeWindField(WindField):
    def __init__(self, config: dict) -> None:
        super().__init__()
        self.field = Polygon(*map(Point2D, config["windfield"]["field"]["vertices"]))
        self.regularly_sampled_coords_in_polygon = regularly_sampled_coords_in_polygon(
            self.field
        )
        self.twa, self.tws = (
            config["windfield"]["wind"]["params"]["TWA"]
            / 360
            * (2 * math.pi),  # TODO: is this a good practice
            config["windfield"]["wind"]["params"]["TWS"],
        )

    def wind_at(self, coordinates: Point2D, time: float) -> WindAtPoint:
        return WindAtPoint(twa=self.twa, tws=self.tws)

    def get_wind_data_for_viz(self, time: float) -> Dict[Point2D, WindAtPoint]:
        return {
            coords: self.wind_at(coords, time)
            for coords in self.regularly_sampled_coords_in_polygon
        }

    def get_field_bounds(self) -> Dict[str, float]:
        x_min, x_max, y_min, y_max = polygon2axis_parallel_bbox(self.field)
        return {"x-left": x_min, "x-right": x_max, "y-bot": y_min, "y-top": y_max}


class WindFieldFactory:
    supported_wind_field_types = {"StaticInSpaceAndTime"}

    def make_wind_field(self, config: dict) -> WindField:
        wind_field_type = config["windfield"]["type"]
        if not wind_field_type in self.supported_wind_field_types:
            raise ValueError(
                f"{wind_field_type} is not one of the supported wind field types, which are: {self.supported_wind_field_types}"
            )

        if wind_field_type == "StaticInSpaceAndTime":
            return StaticInSpaceAndTimeWindField(config=config)
