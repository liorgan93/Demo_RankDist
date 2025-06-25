import torch, numpy as np
from typing import List, Union, Tuple
from collections import Counter
from time import perf_counter

# -------------------------------------------------------------------
#  Monte-Carlo-Climbing U-Top-3  (works up to n≈800, r≤11, k fixed = 3)
# -------------------------------------------------------------------

def _sample_worlds(cat: torch.distributions.Categorical,
                   n_worlds: int,
                   batch: int,
                   k: int,
                   device: str) -> Counter:
    """
    Draw `n_worlds` complete worlds in `batch` chunks (GPU),
    return Counter mapping each unordered k-set → occurrence count.
    """
    counter = Counter()
    worlds_left = n_worlds
    while worlds_left:
        m = min(batch, worlds_left)
        worlds_left -= m

        sampled = cat.sample((m,))            # (m, n_items)  long
        scores = sampled.float()             # 0 … (r-1); higher wins
        eps = 1e-6
        jittered = scores + (torch.rand_like(scores) - 0.5) * eps
        topk = torch.topk(jittered, k, dim=1).indices
        topk_sorted = torch.sort(topk, dim=1).values.cpu().numpy()
        counter.update(map(tuple, topk_sorted))     # each tuple is a k-set
    return counter


def _estimate_set_prob(kset: Tuple[int, ...],
                       cat: torch.distributions.Categorical,
                       n_worlds: int,
                       batch: int,
                       k: int,
                       device: str) -> float:
    """
    Monte-Carlo estimate of probability that `kset`
    is exactly the Top-k set.
    """
    cnt = 0
    worlds_left = n_worlds
    kset = set(kset)
    while worlds_left:
        m = min(batch, worlds_left)
        worlds_left -= m

        sampled = cat.sample((m,))            # (m, n_items)
        scores = sampled.float()
        topk = torch.topk(scores, k, dim=1).indices
        for row in topk.cpu().numpy():
            if kset == set(row):
                cnt += 1
    return cnt / n_worlds


def u_topk_climb(distributions: Union[np.ndarray, torch.Tensor],
                 k: int = 3,
                 device: str = "cuda",
                 *,
                 max_candidates: int = 400,
                 big_worlds: int = 210_000,
                 small_worlds: int = 21_000,
                 batch: int = 4_096,
                 restarts: int = 8) -> List[int]:
    """
    Monte-Carlo climbing search for U-Top-k (k=3 default).
    Designed for n≤800, r≤11.  Runs comfortably in < 1 h on one GPU.

    Parameters
    ----------
    distributions : (n, r)  row-stochastic matrix of score probabilities
    k             : int     size of Top-k set (default 3)
    device        : str     'cuda' or 'cpu'
    max_candidates: int     how many items survive the pruning stage
    big_worlds    : int     #worlds for final probability confirmation
    small_worlds  : int     #worlds per neighbour during climbing
    batch         : int     GPU batch size
    restarts      : int     how many random restarts

    Returns
    -------
    List[int]     indices of the approximate U-Top-k set
    """
    # to torch & normalise
    probs = torch.as_tensor(distributions, dtype=torch.float32, device=device)
    probs = torch.nn.functional.normalize(probs, p=1, dim=1)

    n_items, r = probs.shape
    scores_numeric = torch.arange(r, device=device, dtype=torch.float32)  # 0 .. r-1
    expected = (probs @ scores_numeric)                                   # (n_items,)

    # ---- candidate pruning  -------------------------------------------------
    # keep top `max_candidates` by expected score
    keep = expected.topk(min(max_candidates, n_items)).indices
    probs = probs[keep]                   # (m, r)  m ≤ max_candidates
    id_map = keep.cpu().numpy()           # map back to original indices
    m = probs.shape[0]

    cat = torch.distributions.Categorical(probs)

    # ---- helper: evaluate probability of an unordered set -------------------
    def eval_set(kset_idx: Tuple[int, ...], N=small_worlds) -> float:
        return _estimate_set_prob(kset_idx, cat, N, batch, k, device)

    # ---- hill-climb with multiple restarts ----------------------------------
    best_set: Tuple[int, ...] = tuple(range(k))         # start with top-E scores
    best_prob = eval_set(tuple(range(k)))
    rng = np.random.default_rng()

    for _ in range(restarts):
        # random start
        current = tuple(np.sort(rng.choice(m, k, replace=False)))
        current_prob = eval_set(current)

        improved = True
        while improved:
            improved = False
            current_list = list(current)
            outside = sorted(set(range(m)) - set(current))
            for out_idx in outside:
                for in_pos in range(k):
                    candidate = current_list.copy()
                    candidate[in_pos] = out_idx
                    candidate_tuple = tuple(sorted(candidate))
                    cand_prob = eval_set(candidate_tuple)
                    if cand_prob > current_prob:
                        current, current_prob = candidate_tuple, cand_prob
                        improved = True

        # keep global best
        if current_prob > best_prob:
            best_set, best_prob = current, current_prob

    # ---- final high-precision estimate on best_set ---------------------------
    best_prob = _estimate_set_prob(best_set, cat, big_worlds, batch, k, device)

    # map back to original item IDs and return
    return [int(id_map[i]) for i in best_set]


# ------------------------------------------------------------------
# Example usage with random probabilities
# ------------------------------------------------------------------
if __name__ == "__main__":
    n, r = 800, 11               # after pruning from 800
    k = 3
    #np.random.seed(0)
    raw = np.random.rand(n, r)
    raw /= raw.sum(axis=1, keepdims=True)

    start = perf_counter()
    best_set = u_topk_climb(raw, k=k, device="cuda")
    print(perf_counter() - start)
    print("U-Top-3 set (indices):", best_set)

    for item in best_set:
        print(raw[item])

    print()
    print(raw[:10])
