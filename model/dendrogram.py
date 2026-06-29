import pandas as pd
import scipy.cluster.hierarchy as sch
import matplotlib.pyplot as plt
import os

def generate_dendrogram(input_path, output_image_path):
    print(f"Loading preprocessed data from {input_path}...")
    df = pd.read_csv(input_path)
    
    features = ['energy_scaled', 'valence_scaled', 'tempo_scaled', 'danceability_scaled', 'loudness_scaled']
    X_scaled = df[features]
    
    print("Generating dendrogram... this might take a while.")
    plt.figure(figsize=(15, 10))
    plt.title('Hierarchical Clustering Dendrogram')
    plt.xlabel('Songs')
    plt.ylabel('Euclidean distances')
    
    linkage_matrix = sch.linkage(X_scaled, method='ward')
    sch.dendrogram(linkage_matrix, truncate_mode='lastp', p=50, leaf_rotation=90., leaf_font_size=8., show_contracted=True)
    
    print(f"Saving dendrogram to {output_image_path}...")
    plt.savefig(output_image_path)
    plt.close()
    print("Dendrogram complete.")

if __name__ == "__main__":
    input_file = os.path.join("data", "processed_data.csv")
    output_image = os.path.join("model", "dendrogram.png")
    generate_dendrogram(input_file, output_image)
