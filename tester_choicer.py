import time
import pandas as pd
import ast
import numpy as np
import logging
import torch
from collections import Counter
from utils import generate_universe
#from tqdm import tqdm
from constants import *
import math
import csv
import math
from expected_precision_calculator import *
from constants import *

from typing import Dict, List
from rank_dist import RankDist
from testing_u_top_k import u_topk_climb


def build_score_probabilities(success_probs):
    """
    Builds a tensor of probabilities where each row contains:
    [probability of failure, probability of success].

    Args:
        success_probs (list or numpy.ndarray): List or NumPy array of probabilities of success.

    Returns:
        torch.Tensor: A tensor of shape (len(success_probs), 2).
    """
    # Ensure the input is a NumPy array
    success_probs = np.array(success_probs)

    # Calculate failure probabilities
    failure_probs = 1 - success_probs

    # Combine into a 2D array
    probabilities = np.stack((failure_probs, success_probs), axis=1)

    # Convert to a PyTorch tensor
    return torch.from_numpy(probabilities)

def prev_test():
    # Example usage
    success_probs = [0.6, 0.7, 0.8, 0.9, 0.5]
    score_probabilities = build_score_probabilities(success_probs)
    print(score_probabilities)

def randomList(size=50):
    probabilities = np.random.uniform(0.01, 0.99, size=size).tolist()
    return probabilities


def randProbsVals(vals=5, rows=50):
    # Generate a matrix of random weights
    weights = np.random.uniform(0, 1, size=(rows, vals))

    # Normalize each row to sum to 1
    probs = weights / weights.sum(axis=1, keepdims=True)

    # Convert to PyTorch tensor
    probsTensor = torch.tensor(probs, dtype=torch.float32)

    return probsTensor

def former():
    size = 10
    vals = 3
    score_values = torch.tensor([i + 1 for i in range(vals)])
    values_matrix = score_values.unsqueeze(0).repeat(size, 1)
    prr_threshold = 0.8 * vals
    device = 'cpu'
    top_k_max_size = 10
    top_k_size_options = range(5, top_k_max_size + 1, 5)
    score_probabilities = randProbsVals(vals, size)
    print('score probabilities')
    print(score_probabilities)

    print("------")
    rank_dist = RankDist(score_probabilities, values_matrix, device=device)
    batch_size = math.floor(math.sqrt(len(score_probabilities)))
    rank_dist_log_result = rank_dist.rank_dist_with_tiebreaking_batch(k=top_k_max_size,
                                                                    batch_size=batch_size).cpu().detach().numpy()
    print(rank_dist_log_result)


    rank_dist_log_result = np.logaddexp.reduce(rank_dist_log_result, axis=2)
    print("->")
    print(rank_dist_log_result)
    print("------")

    top_k_results = {}
    #print("expected_score")
    item_scores = torch.sum(score_probabilities * score_values, dim=1)
    top_k_results["expected_score"] = torch.argsort(item_scores, descending=True)[:top_k_max_size].tolist()

    #print("global_top_k")
    top_k_results["global_top_k"] = dict()
    for top_k_size in top_k_size_options:
        rank_dist_result_at_k = rank_dist_log_result[:, :top_k_size]
        tuples_prob_until_k = np.logaddexp.reduce(rank_dist_result_at_k, axis=1)
        top_k_results["global_top_k"][top_k_size] = np.argsort(tuples_prob_until_k)[::-1][:top_k_size].tolist()

    #print("probability_of_relevance_ranking")
    item_scores = torch.sum(score_probabilities[:, score_values >= prr_threshold], dim=1)
    top_k_results["probability_of_relevance_ranking"] = torch.argsort(item_scores, descending=True)[:top_k_max_size].tolist()

    """
    
    print("uncertainty_based_filtering - 1")
    percentile = 1
    top_k_item_ids = rec_items_by_preds[:top_k_max_size].index.tolist()
    top_k_results["uncertainty_based_filtering"] = [self.item_ids_to_item_idxs[item_id]
                                                    for item_id in top_k_item_ids]

    print("uncertainty_based_filtering - 0.8")
    percentile = 0.8
    top_k_item_ids = self.get_item_ids_after_ubf(percentile, self.top_k_max_size)
    top_k_results["uncertainty_based_filtering"] = [self.item_ids_to_item_idxs[item_id]
                                  for item_id in top_k_item_ids]
    """

    #print("U-k-ranks")
    top_k_results["U-k-ranks"] = np.argmax(rank_dist_log_result, axis=0)

    for method in top_k_results:
        print(method)
        ids = top_k_results[method]
        if isinstance(ids, dict):
            for key in ids:
                print(key, ":", ids[key])
                precisionCalculator = PrecisionCalculator(score_probabilities, values_matrix, device=device)
                log_expected_precision = \
                    precisionCalculator.calculate_expected_precision(ids[key])[1]
                expected_precision = np.exp(log_expected_precision)
                print(expected_precision)
        elif isinstance(ids, list):
            print(ids)
            precisionCalculator = PrecisionCalculator(score_probabilities, values_matrix, device=device)
            log_expected_precision = \
                precisionCalculator.calculate_expected_precision(ids)[1]
            expected_precision = np.exp(log_expected_precision)
            print(expected_precision)
        else:
            try:
                print(ids)
                precisionCalculator = PrecisionCalculator(score_probabilities, values_matrix, device=device)
                log_expected_precision = \
                    precisionCalculator.calculate_expected_precision(ids)[1]
                expected_precision = np.exp(log_expected_precision)
                print(expected_precision)
            except Exception as e:
                print("There was a problem:")
                print(e)
                print("next")
                print("C:\\Users\\USER\\Documents\\technion_stuff\\ml2_course\\hw3\\tiny-imagenet-200\\test\\images\\test_0.JPEG")



def expected_score_method(top_k_results: Dict, score_probabilities, score_values, top_k_max_size: int):
    item_scores = torch.sum(score_probabilities * score_values, dim=1)
    top_k_results["expected_score"] = torch.argsort(item_scores, descending=True)[:top_k_max_size].tolist()

def global_top_k_method(top_k_results: Dict, rank_dist_log_result, top_k_max_size: int):
    rank_dist_result_at_k = rank_dist_log_result[:, :top_k_max_size]
    tuples_prob_until_k = np.logaddexp.reduce(rank_dist_result_at_k, axis=1)
    top_k_results["global_top_k_" + str(top_k_max_size)] = np.argsort(tuples_prob_until_k)[::-1][
                                                           :top_k_max_size].tolist()

def u_top_k_method(top_k_results: Dict, score_probabilities, score_values, prr_threshold, top_k_min_size: int):
    item_scores = torch.sum(score_probabilities[:, score_values >= prr_threshold], dim=1)
    pruned_item_indexes = torch.argsort(item_scores, descending=True)[
                          :len(item_scores) // 2].tolist()
    scores_probabilities_pruned = score_probabilities[pruned_item_indexes]
    convertion_pruned_indexes = {newIndex: oldIndex for newIndex, oldIndex in enumerate(pruned_item_indexes)}

    score_probs_np = scores_probabilities_pruned.cpu().numpy()
    u_results = u_topk_climb(score_probs_np, k=top_k_min_size, device=device)
    top_k_results["u_topk_" + str(top_k_min_size)] = [convertion_pruned_indexes[score] for score in u_results]

def retrieveTopKMeasurements(predictions, top_k_min_size=3, top_k_max_size=3, prr=0.5, methods=None):
    size = len(predictions)
    vals = len(predictions[0])

    score_values = torch.tensor([i + 1 for i in range(vals)])
    values_matrix = score_values.unsqueeze(0).repeat(size, 1)
    # score_values = torch.tensor([i + 1 for i in range(vals)])
    # values_matrix = score_values.unsqueeze(0).repeat(size, 1)
    device = 'cpu'

    # top_k_size_options = range(top_k_min_size, top_k_max_size + 1, 1)

    predictions_array = np.array(predictions.tolist(), dtype=np.float32)
    score_probabilities = torch.from_numpy(predictions_array)



    top_k_results = {}
    if "expected_score" in methods:
        expected_score_method(top_k_results, score_probabilities, score_values, top_k_max_size)

    if "global_top_k" in methods:
        rank_dist = RankDist(score_probabilities, values_matrix, device=device)
        batch_size = math.floor(math.sqrt(len(score_probabilities)))
        rank_dist_log_result = rank_dist.rank_dist_with_tiebreaking_batch(k=top_k_max_size,
                                                                          batch_size=batch_size).cpu().detach().numpy()
        rank_dist_log_result = np.logaddexp.reduce(rank_dist_log_result, axis=2)
        global_top_k_method(top_k_results, rank_dist_log_result, top_k_max_size)

    # convert once from CUDA → CPU → NumPy
    if "u_topk" in methods:
        prr_threshold = prr * vals
        u_top_k_method(top_k_results, score_probabilities, score_values, prr_threshold, top_k_min_size)

    for method in top_k_results:
        print(method)
        ids = top_k_results[method]
        if isinstance(ids, dict):
            for key in ids:
                print(key, ":", ids[key])
                precisionCalculator = PrecisionCalculator(score_probabilities, values_matrix, device=device)
                log_expected_precision = \
                    precisionCalculator.calculate_expected_precision(ids[key])[1]
                expected_precision = np.exp(log_expected_precision)
                print(expected_precision)
        elif isinstance(ids, list):
            print(ids)
            precisionCalculator = PrecisionCalculator(score_probabilities, values_matrix, device=device)
            log_expected_precision = \
                precisionCalculator.calculate_expected_precision(ids)[1]
            expected_precision = np.exp(log_expected_precision)
            print(expected_precision)
        else:
            try:
                print(ids)
                precisionCalculator = PrecisionCalculator(score_probabilities, values_matrix, device=device)
                log_expected_precision = \
                    precisionCalculator.calculate_expected_precision(ids)[1]
                expected_precision = np.exp(log_expected_precision)
                print(expected_precision)
            except Exception as e:
                print("There was a problem:")
                print(e)
                print("next")
    return ids



def main():
    methods = ["expected_score", "global_top_k", "u_topk"]
    folder_path = "C:\\Users\\USER\\Documents\\technion_stuff\\final\\omri_thing\\als data\\"
    num_cols = ['1', '2', '3', '4', '5']
    for i in range(5):
        print("cluster " + str(i))
        csv_path = folder_path + "als_min_clustered_" + str(i) + ".csv"
        averagedDf = pd.read_csv(csv_path)
        predictions = averagedDf.apply(lambda row: [row[i] for i in num_cols], axis=1)
        retrieveTopKMeasurements(predictions=predictions, top_k_min_size=3, top_k_max_size=5 ,methods=methods)
        print("-------------------------")

def run_cluster(df: pd.DataFrame):
    methods = ["expected_score", "global_top_k", "u_topk"]
    num_cols = ['0', '1', '2', '3', '4']
    df = df.rename(columns={f"prob_{n}": n for n in num_cols})
    print(df)
    predictions = df.apply(lambda row: [row[i] for i in num_cols], axis=1)
    show_order_by_total_playcount(df)

    return retrieveTopKMeasurements(predictions=predictions, top_k_min_size=3, top_k_max_size=3, methods=methods)

from tabulate import tabulate

def show_order_by_total_playcount(df):
    print("Real order by playcount:\n")
    sorted_df = df.sort_values(by='playcount', ascending=False)

    table_data = []
    for index, row in sorted_df.iterrows():
        table_data.append([index, row['track_id'], row['track_name'], row['playcount'], row['predicted_probabilities']])

    headers = ["Index", "track id", "Track ID", "Playcount", "Predicted Probabilities"]
    print(tabulate(table_data, headers=headers, tablefmt="pretty"))


def run_clusters():
    folder_path = "C:\\Users\\USER\\Desktop\\תרגילי בית להגשה\\פרוייקט גמר\\Datasets\\Kaggle datasets\\dataset with playcount\\coralgorithm\\Coralgorithm\\relevant_dfs\\"
    #csv_files = [f"results_df_cluster{i}.csv" for i in range(1, 5)]
    csv_files = []
    csv_files = csv_files + [f"reduced_results_df_cluster{i}.csv" for i in range(1, 5)]

    for csv_file in csv_files:

        df = pd.read_csv('results_for_lior.csv')

        #working only when len(df)>5 and includes index 0 - why???
        #run_cluster(df[1:7].reset_index())
        for i in range(5):
            df_run = df
            aaa = run_cluster(df_run)
            print("aaa", aaa)

            print()
            print("*" * 150)
            print("*" * 150)
            #print("*" * 150)
            print()
        return aaa
        break;

if __name__ == '__main__':
    #print(torch.cuda.is_available())
    run_clusters()
