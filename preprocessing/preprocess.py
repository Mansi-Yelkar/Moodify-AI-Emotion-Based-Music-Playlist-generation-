import pandas as pd
from sklearn.preprocessing import StandardScaler
import os

def preprocess_data(input_path, output_path, sample_size=10000):
    print(f"Loading data from {input_path}...")
    df = pd.read_csv(input_path)
    
    # Cleaning
    print("Cleaning data...")
    df = df.dropna()
    df = df.drop_duplicates()
    
    features = ['energy', 'valence', 'tempo', 'danceability', 'loudness']
    
    # Check if we have missing features
    missing = [f for f in features if f not in df.columns]
    if missing:
        print(f"Missing features: {missing}")
        return None
    
    # Downsample
    if sample_size and len(df) > sample_size:
        print(f"Downsampling from {len(df)} to {sample_size} rows...")
        df = df.sample(n=sample_size, random_state=42).reset_index(drop=True)
    
    print("Scaling features...")
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[features])
    
    # Store scaled features back into the dataframe
    for i, col in enumerate(features):
        df[f"{col}_scaled"] = scaled_features[:, i]
        
    print(f"Saving preprocessed data to {output_path}...")
    df.to_csv(output_path, index=False)
    print("Preprocessing complete.")
    return df

if __name__ == "__main__":
    input_file = os.path.join("data", "SpotifyAudioFeaturesApril2019.csv")
    output_file = os.path.join("data", "processed_data.csv")
    preprocess_data(input_file, output_file)
