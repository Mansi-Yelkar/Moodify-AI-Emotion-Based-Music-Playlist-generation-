import pandas as pd
from sklearn.cluster import AgglomerativeClustering
import os
import pickle

def perform_clustering(input_path, output_path, model_path):
    print(f"Loading preprocessed data from {input_path}...")
    df = pd.read_csv(input_path)
    
    features = ['energy_scaled', 'valence_scaled', 'tempo_scaled', 'danceability_scaled', 'loudness_scaled']
    X_scaled = df[features]
    
    print("Applying Agglomerative Hierarchical Clustering (Ward linkage, 5 clusters)...")
    model = AgglomerativeClustering(n_clusters=5, linkage='ward')
    labels = model.fit_predict(X_scaled)
    
    df['cluster'] = labels
    
    print(f"Saving clustered data to {output_path}...")
    df.to_csv(output_path, index=False)
    
    print(f"Saving model to {model_path}...")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    print("\nCluster Characteristics (Means):")
    cluster_means = df.groupby('cluster')[['energy', 'valence', 'tempo', 'danceability', 'loudness']].mean()
    print(cluster_means)
    
    print("\nClustering complete.")

if __name__ == "__main__":
    input_file = os.path.join("data", "processed_data.csv")
    output_file = os.path.join("data", "clustered_data.csv")
    model_file = os.path.join("model", "clustering_model.pkl")
    perform_clustering(input_file, output_file, model_file)
