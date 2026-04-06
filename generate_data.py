import pandas as pd
import numpy as np

def generate_accident_data(n_per_class=1500):
    np.random.seed(42)
    frames = []

    # ── Class 0: SAFE ─────────────────────────────────────────
    n = n_per_class
    safe = pd.DataFrame({
        'lat': np.random.uniform(17.30, 17.55, n),
        'lon': np.random.uniform(78.30, 78.60, n),
        'driver_age': np.random.randint(25, 55, n),
        'driver_experience': np.random.randint(5, 40, n),
        'vehicle_age': np.random.randint(0, 8, n),
        'vehicle_type': np.random.randint(0, 4, n),
        'speed': np.random.randint(20, 55, n),
        'weather': np.zeros(n, dtype=int),
        'road_type': np.random.randint(0, 2, n),
        'light_condition': np.zeros(n, dtype=int),
        'traffic_density': np.random.randint(0, 2, n),
        'surface_condition': np.zeros(n, dtype=int),
        'hour_of_day': np.random.randint(6, 20, n),
        'accident_count': np.random.randint(0, 5, n),   # Low historical accidents (0-4)
        'risk': 0
    })
    frames.append(safe)

    # ── Class 1: LESS RISKY ───────────────────────────────────
    less = pd.DataFrame({
        'lat': np.random.uniform(17.30, 17.55, n),
        'lon': np.random.uniform(78.30, 78.60, n),
        'driver_age': np.random.randint(20, 65, n),
        'driver_experience': np.random.randint(2, 20, n),
        'vehicle_age': np.random.randint(5, 15, n),
        'vehicle_type': np.random.randint(0, 4, n),
        'speed': np.random.randint(55, 85, n),
        'weather': np.random.randint(0, 2, n),
        'road_type': np.random.randint(0, 3, n),
        'light_condition': np.random.randint(0, 2, n),
        'traffic_density': np.random.randint(1, 3, n),
        'surface_condition': np.random.randint(0, 2, n),
        'hour_of_day': np.random.randint(0, 24, n),
        'accident_count': np.random.randint(5, 20, n),  # Medium historical accidents (5-19)
        'risk': 1
    })
    frames.append(less)

    # ── Class 2: RISKY ────────────────────────────────────────
    risky = pd.DataFrame({
        'lat': np.random.uniform(17.30, 17.55, n),
        'lon': np.random.uniform(78.30, 78.60, n),
        'driver_age': np.random.choice(list(range(18, 23)) + list(range(60, 70)), n),
        'driver_experience': np.random.randint(0, 3, n),
        'vehicle_age': np.random.randint(12, 20, n),
        'vehicle_type': np.random.randint(0, 4, n),
        'speed': np.random.randint(85, 120, n),
        'weather': np.random.randint(1, 4, n),
        'road_type': np.full(n, 2, dtype=int),
        'light_condition': np.ones(n, dtype=int),
        'traffic_density': np.full(n, 2, dtype=int),
        'surface_condition': np.random.randint(1, 3, n),
        'hour_of_day': np.random.choice(list(range(0, 5)) + list(range(22, 24)), n),
        'accident_count': np.random.randint(20, 60, n), # High historical accidents (20-59)
        'risk': 2
    })
    frames.append(risky)

    df = pd.concat(frames, ignore_index=True).sample(frac=1, random_state=42).reset_index(drop=True)
    df.to_csv('accident_data_v2.csv', index=False)

    print(f"Dataset saved: {len(df)} total samples")
    print("Class distribution:")
    print(df['risk'].value_counts())

if __name__ == "__main__":
    generate_accident_data()
