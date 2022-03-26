import os
import pandas as pd
from data_analyzer import DataAnalyzer
from data_loader import DataLoader

pd.set_option('display.max_columns', None)

EVENTS_DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/events.csv')
TRACKING_DATA_PATH = os.path.join(os.path.dirname(__file__), '../data/tracking.csv')


def main():
    data_loader = DataLoader(events_path=EVENTS_DATA_PATH, tracking_path=TRACKING_DATA_PATH)
    merged = data_loader.merge_events_and_tracking()

    print('Merged dataset of events and tracking: ')
    print(merged.head(10))

    data_analyzer = DataAnalyzer(merged_dataset=merged)

    print(f'The length of ball trajectory from initial kick off to first ball out of play: '
          f'{data_analyzer.calculate_initial_ball_trajectory()}m', end='\n\n')
    print(f'The player with most passes is: {data_analyzer.get_player_with_most_passes()}', end='\n\n')

    print('List of players by pass completion rate: ')
    print(data_analyzer.get_player_with_best_pass_completion_rate_pct())


if __name__ == '__main__':
    main()
