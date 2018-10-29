import requests
import sys

import pandas as pd


def main(value):
    value = int(value)
    url = 'https://fantasy.premierleague.com/drf/bootstrap-static'

    r = requests.get(url)

    data = r.json()

    players_df = pd.DataFrame(data['elements'])

    players_df = players_df[
        [
            'web_name',
            'now_cost',
            'points_per_game',
            'element_type',
            'value_form',
            'value_season',
            'form',
            'bps'
        ]
    ]

    players_df['form'] = players_df['form'].map(lambda x: float(x))
    players_df['points_per_game'] = players_df['points_per_game'].map(lambda x: float(x))
    players_df['value_form'] = players_df['value_form'].map(lambda x: float(x))
    players_df['value_season'] = players_df['value_season'].map(lambda x: float(x))
    players_df['form'] = players_df['form'].map(lambda x: float(x))
    players_df['now_cost'] = players_df['now_cost'].map(lambda x: float(x))

    positions = _get_position_names(data)

    players_df['position'] = players_df['element_type'].map(lambda x: positions[x])

    players_df['form/cost'] = players_df['form'] / players_df['now_cost'] * 10
    players_df['ppg/cost'] = players_df['points_per_game'] / players_df['now_cost'] * 10

    print("Goalkeepers:")
    print(players_df[(players_df['position'] == 'GKP') &
                     (players_df['now_cost'] >= value)].sort_values(['form/cost', 'ppg/cost'],
                                                                    ascending=False).head())

    print("Defenders:")
    print(players_df[(players_df['position'] == 'DEF') &
                     (players_df['now_cost'] >= value)].sort_values(['form/cost', 'ppg/cost'],
                                                                    ascending=False).head())

    print("Midfielders:")
    print(players_df[(players_df['position'] == 'MID') &
                     (players_df['now_cost'] >= value)].sort_values(['form/cost', 'ppg/cost'],
                                                                    ascending=False).head())

    print("Forwards:")
    print(players_df[(players_df['position'] == 'GKP') &
                     (players_df['now_cost'] >= value)].sort_values(['form/cost', 'ppg/cost'],
                                                                    ascending=False).head())


def _get_position_names(data):
    return {element['id']: element['singular_name_short'] for element in data['element_types']}


if __name__ == '__main__':
    main(sys.argv[1])
