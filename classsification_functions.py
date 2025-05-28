import numpy as np
import pandas as pd

def sample_unique_tracks_per_cluster(df, cluster_col='cluster', track_col='track_id', artist_col='artist', n=2):
    sampled_tracks = []
    used_track_ids = set()
    used_artist_names = set()

    for cluster in sorted(df[cluster_col].unique()):
        cluster_df = df[df[cluster_col] == cluster]

        available_df = cluster_df[
            ~cluster_df[track_col].isin(used_track_ids) &
            ~cluster_df[artist_col].isin(used_artist_names)
        ]

        cluster_samples = []

        while len(cluster_samples) < min(n, len(available_df)):
            sample = available_df.sample(n=1)

            cluster_samples.append(sample)

            used_track_ids.update(sample[track_col])
            used_artist_names.update(sample[artist_col])

            available_df = available_df[
                ~available_df[track_col].isin(used_track_ids) &
                ~available_df[artist_col].isin(used_artist_names)
            ]

        if cluster_samples:
            sampled_tracks.append(pd.concat(cluster_samples))

    if sampled_tracks:
        return pd.concat(sampled_tracks).reset_index(drop=True)
    else:
        return pd.DataFrame(columns=df.columns)




def classify_user_by_preferences(df, like_dislike_col='like/dislike', weights_col='weights'):
    if like_dislike_col not in df.columns or weights_col not in df.columns:
        raise ValueError(f"DataFrame must contain '{like_dislike_col}' and '{weights_col}' columns.")

    for row in df[weights_col]:
        if isinstance(row, list):
            n_clusters = len(row)
            break
    else:
        raise ValueError("No valid list found in 'weights' column to determine number of clusters.")

    cluster_scores = [0.0] * n_clusters

    for _, row in df.iterrows():
        weights = row[weights_col]

        if not isinstance(weights, list) or len(weights) != n_clusters:
            return 99, 1
            continue
        if row[like_dislike_col][0] == 1:
            for i in range(n_clusters):
                cluster_scores[i] += weights[i]
        elif row[like_dislike_col][0] == 0:
            for i in range(n_clusters):
                cluster_scores[i] -= weights[i]
        else:
            continue

    best_cluster = int(np.argmax(cluster_scores))
    return best_cluster, cluster_scores