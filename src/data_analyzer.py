import copy

import pandas as pd

from distance_utils import eucledian_distance_in_meters


class DataAnalyzer:
    """Given some tracking data, this class is responsible to analyze and extract meaningful insights from them"""
    def __init__(self, merged_dataset: pd.DataFrame):
        self.merged = merged_dataset

    def calculate_initial_ball_trajectory(self) -> int:
        """
        Calculates the length of the ball trajectory from the initial kickoff to the first "Ball Out of Play"
        event. Returns the distance in meters.
        """
        first_out_of_play_index = self.merged[self.merged['event'] == 'Ball Out of Play'].index.values[0]
        df = copy.deepcopy(self.merged[:first_out_of_play_index + 1])

        df['next_x'] = df['x'].shift(-1)
        df['next_y'] = df['y'].shift(-1)

        df['distance_to_next_event'] = df.apply(
            lambda row: eucledian_distance_in_meters(x1=row['x'], y1=row['y'], x2=row['next_x'], y2=row['next_y']),
            axis=1
        )
        return round(df['distance_to_next_event'].sum(), 2)

    def get_player_with_most_passes(self) -> int:
        """Returns the player with the most passes"""
        return int(self.merged[self.merged['event'] == 'Pass']['player_id'].mode())

    def get_player_with_best_pass_completion_rate_pct(self) -> float:
        """Returns the player with best pass completion rate in percentage"""
        pass_completion_rate_by_player = \
            self.merged[self.merged['event'] == 'Pass']\
                .groupby('player_id')\
                .apply(lambda a: a.was_pass_successful.mean())\
                .reset_index()
        # note: there are some players with 100% completion rate, therefore returning the whole dataframe
        #       instead of just picking one with the highest
        return pass_completion_rate_by_player