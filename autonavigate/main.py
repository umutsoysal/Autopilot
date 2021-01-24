from raceviz import MPLRaceViz
from agents import Boat
from pathlib import Path
from typing import List, Dict
from agents import make_boat
from windfields import WindField, WindFieldFactory, WindAtPoint
import yaml
from sympy import Point2D

SCENARIO_CONFIG_FILE = Path.cwd() / "configs" / "scenario_1.yaml"
RACE_ANIMATION_PATH = Path.cwd() / "animation.mp4"


class Environment:  # TODO: is race a better name?
    def __init__(self, config: dict) -> None:
        assert config["tmax"] > config["tzero"], AssertionError(
            f"tmax must be larger than tzero. tmax:{config['tmax']} tzero: {config['tzero']} were given"
        )
        assert config["dt"] > 0, AssertionError(
            f"dt must be a positive number, {config['dt']} were given"
        )
        self.t_max: float = config["tmax"]
        self.t_now: float = config["tzero"]
        self.dt: float = config["dt"]
        self.boats: List[Boat] = []
        self.wind_field: WindField = WindFieldFactory().make_wind_field(config=config)

    def advance(self) -> None:
        # Update Agents
        for agent in self.boats:
            wind_at_agent_coords = self.wind_field.wind_at(agent.coords, self.t_now)
            agent.sail(wind_at_agent_coords, self.dt)
            agent.update_heading(self.t_now)

        # Update clock
        self.t_now += self.dt

    def is_finished(self) -> bool:
        return self.t_now > self.t_max

    def register_boat(self, new_agent: Boat) -> None:
        self.boats.append(new_agent)

    def get_wind_data_for_viz(self) -> Dict[Point2D, WindAtPoint]:
        return self.wind_field.get_wind_data_for_viz(self.t_now)

    def get_field_bounds(self) -> Dict[str, float]:
        return self.wind_field.get_field_bounds()

    def get_boat_coord_data(self) -> Dict[str, Point2D]:
        return {boat.name: boat.coords for boat in self.boats}


def load_yaml(filepath: Path):
    with open(filepath) as f:
        return yaml.load(f)


def main():

    scenario_config = load_yaml(SCENARIO_CONFIG_FILE)

    # Initialize Environment with config
    env = Environment(scenario_config)
    for boat_name, boat_config in scenario_config["boats"].items():
        env.register_boat(
            make_boat(boat_name, boat_config, scenario_config["tzero"], env.wind_field)
        )

    raceviz = MPLRaceViz()
    raceviz.register_field_bounds(env.get_field_bounds())

    while not env.is_finished():
        raceviz.register_wind_data(env.get_wind_data_for_viz())
        raceviz.register_boat_coords(env.get_boat_coord_data())
        env.advance()

    raceviz.render_race_animation()
    raceviz.save_race_animation(RACE_ANIMATION_PATH)


if __name__ == "__main__":
    # import cProfile, pstats
    # profiler = cProfile.Profile()
    # profiler.enable()

    main()

    # profiler.disable()
    # with open("profilingStats.txt", "w") as f:
    #     stats = pstats.Stats(profiler, stream=f).sort_stats("tottime")
    #     # ps = pstats.Stats("profilingResults.cprof", stream=f)
    #     stats.sort_stats("cumulative")
    #     stats.print_stats()
