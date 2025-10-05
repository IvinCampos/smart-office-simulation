
# simulador_smart_office.py
# Gera dados simulados para sensores de temperatura, luminosidade e ocupação.
# Salva em smart_office_data.csv
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate(start, days=7, freq='15T'):
    timestamps = pd.date_range(start=start, periods=int((24*60)/15)*days, freq=freq)
    rooms = ['SalaA', 'SalaB', 'SalaC']
    sensor_defs = []
    for room in rooms:
        sensor_defs.append({'sensor_id': f'{room}_TEMP_1', 'type': 'temperature'})
        sensor_defs.append({'sensor_id': f'{room}_LUX_1', 'type': 'luminosity'})
        sensor_defs.append({'sensor_id': f'{room}_OCC_1', 'type': 'occupancy'})

    rows = []
    for ts in timestamps:
        hour = ts.hour
        weekday = ts.weekday()
        is_weekend = weekday >= 5
        for s in sensor_defs:
            if s['type'] == 'temperature':
                if 0 <= hour < 6:
                    base = 20.0
                elif 6 <= hour < 9:
                    base = 21.5
                elif 9 <= hour < 18:
                    base = 23.5
                elif 18 <= hour < 22:
                    base = 22.5
                else:
                    base = 20.5
                value = round(np.random.normal(loc=base, scale=0.7), 2)
            elif s['type'] == 'luminosity':
                if hour < 6 or hour >= 20:
                    value = 0.0
                else:
                    day_progress = (hour - 6) / 14.0
                    base = 100 + 700 * max(0, np.sin(day_progress * np.pi))
                    value = max(0.0, round(np.random.normal(loc=base, scale=80), 1))
            else:
                if not is_weekend and 8 <= hour < 18:
                    p = 0.75
                elif not is_weekend and (7 <= hour < 8 or 18 <= hour < 20):
                    p = 0.25
                elif is_weekend and 9 <= hour < 17:
                    p = 0.15
                else:
                    p = 0.05
                spike = np.random.rand() < 0.01
                value = int((np.random.rand() < p) or spike)
            rows.append({'timestamp': ts, 'sensor_id': s['sensor_id'], 'sensor_type': s['type'], 'value': value})
    return pd.DataFrame(rows)

if __name__ == '__main__':
    # Start 7 days ago at midnight local time
    start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=7)
    df = generate(start=start, days=7, freq='15T')
    csv_path = 'smart_office_data.csv'
    df.to_csv(csv_path, index=False)
    print(f'Arquivo gerado: {csv_path} com {len(df)} registros')
