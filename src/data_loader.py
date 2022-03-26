import pandas as pd


class DataLoader:
    """Responsible to load the data and process them (i.e. merge, clean, enrich)"""

    def __init__(self, events_path: str, tracking_path: str):
        self.events_df = pd.read_csv(events_path)
        self.tracking_df = pd.read_csv(tracking_path)

        # prepare events and tracking dataframe for further usage
        self._add_success_flag_to_pass_and_cross()
        self._add_time_in_seconds()

    def _add_success_flag_to_pass_and_cross(self):
        """Adds a 'was_successful' column to the events dataframe. This flag indicates whether events of type pass and
        cross were successful or misplaced"""
        self.events_df['next_event_type'] = self.events_df['event'].shift(-1)

        # a pass is successful if the current event is a pass followed by a reception. For non-pass events, we mark this
        # flag as none
        self.events_df['was_pass_successful'] = self.events_df.apply(
            lambda row: None if row['event'] != 'Pass' else row['next_event_type'] == 'Reception', axis=1
        )

        # a cross is successful if it was either followed by a reception from your own teammate, or an attempt to goal
        # happened. For non-cross events we mark this flag as none
        self.events_df['was_cross_successful'] = self.events_df.apply(
            lambda row: None if row['event'] != 'Cross' else row['next_event_type'] in ['Reception', 'Attempt at Goal'],
            axis=1
        )

    def _add_time_in_seconds(self):
        """Adds a column time in seconds to tracking dataframe"""
        # tracking df has time in milliseconds - we convert them to seconds and keep two decimals for merging
        self.tracking_df['time_in_seconds'] = round(self.tracking_df['t'] / 1000, 1)
        # TODO: asked Jaeson about this, but since I didn't hear back I implemented it like this (my assumption might be
        #       wrong here. Basically the time in the events dataframe is given in seconds, while the first event has a
        #       time of 625.68 and the last one 1225.25. Meanwhile, the time in tracking is given in milliseconds,
        #       where the maximum value of the time field is 600000 (which is 600 seconds).
        #       While trying to merge the datasets this becomes a bit problematic, since you want to use time as
        #       one of the columns that you join based on. In order to be similar, I subtract the time of the event
        #       with the time of the first event, so that the first event starts at zero as well
        self.events_df['time_in_seconds'] = round(self.events_df['time'] - 625.68, 1)

    def merge_events_and_tracking(self) -> pd.DataFrame:
        """Merges events and tracking dataframes and returns the merged one"""
        merged = pd.merge(
            self.events_df, self.tracking_df, how='left',
            left_on=['half_time', 'player_id', 'team_id', 'time_in_seconds'],
            right_on=['id_half', 'id_actor', 'id_team', 'time_in_seconds']
        )
        # keep one row for event
        merged = merged.drop_duplicates(subset=['event_id'])
        merged = merged[['event_id', 'half_time', 'player_id', 'team_id', 'event', 'time_in_seconds', 'x', 'y',
                         'was_pass_successful', 'was_cross_successful']]
        return merged.reset_index(drop=True)
