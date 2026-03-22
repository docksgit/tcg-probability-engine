"""
tcg-probability-engine/src/probability.py

Core probability calculations for TCG deck consistency analysis.
Uses multivariate hypergeometric distribution for exact combinatorial math.
"""

from scipy.stats import hypergeom
from typing import Dict, List, Union
import math


def calc_hypergeom_pmf(N: int, K: int, n: int, k: int) -> float:
    """
    Calculate P(X = k) for hypergeometric distribution.
    
    N: population size (deck size)
    K: success states in population (target cards)
    n: number of draws (hand size)
    k: number of observed successes
    """
    if k > K or k > n or (n - k) > (N - K):
        return 0.0
    return hypergeom.pmf(k, N, K, n)


def calc_hypergeom_cdf_ge(N: int, K: int, n: int, min_k: int = 1) -> float:
    """
    Calculate P(X >= min_k) for hypergeometric distribution.
    """
    return sum(calc_hypergeom_pmf(N, K, n, k) for k in range(min_k, min(K, n) + 1))


def calc_pocket_turn1_success(
    deck_size: int = 20,
    eb_count: int = 4,
    ex_count: int = 4,
    es_count: int = 1,
    ds_count: int = 2,
    other_count: int = 9,
    opening_hand: int = 5,
    turn_draw: int = 1,
    ds_draw_count: int = 2,
    verbose: bool = False
) -> Dict[str, Union[float, Dict]]:
    """
    Calculate Turn 1 success probability for Pokemon TCG Pocket combo.
    """
    # Validate deck composition
    assert eb_count + ex_count + es_count + ds_count + other_count == deck_size
    
    target_count = ex_count + es_count
    remaining_deck = deck_size - opening_hand
    
    # ========== EDGE CASE: No EB means 0% success ==========
    if eb_count == 0:
        result = {
            "total_success": 0.0,
            "total_fail": 1.0,
            "paths": {
                "A_combo_in_opening": 0.0,
                "B1_turn_draw_no_ds": 0.0,
                "B2_turn_draw_with_ds": 0.0,
                "C_ds_dig_success": 0.0,
                "fail_no_eb": 1.0,
                "fail_no_ds_turn_miss": 0.0,
                "fail_ds_dig_miss": 0.0,
            },
            "conditionals": {
                "p_eb_in_opening": 0.0,
                "p_target_given_eb": 0.0,
                "p_ds_given_missing_target": 0.0,
            }
        }
        if verbose:
            print("❌ No Energy Baby in deck — 0% success rate")
        return result
    
    # ========== EDGE CASE: All non-EB cards are targets ==========
    # If every card that isn't EB is a target, and we have EB, success = P(EB >= 1)
    if target_count + ds_count + other_count == deck_size - eb_count:
        # All non-EB cards are targets
        p_eb = 1 - calc_hypergeom_cdf_ge(deck_size, eb_count, opening_hand, min_k=0)
        p_eb = calc_hypergeom_cdf_ge(deck_size, eb_count, opening_hand, min_k=1)
        if p_eb > 0.999:  # Essentially guaranteed
            result = {
                "total_success": 1.0,
                "total_fail": 0.0,
                "paths": {
                    "A_combo_in_opening": p_eb,
                    "B1_turn_draw_no_ds": 0.0,
                    "B2_turn_draw_with_ds": 0.0,
                    "C_ds_dig_success": 0.0,
                    "fail_no_eb": 1 - p_eb,
                    "fail_no_ds_turn_miss": 0.0,
                    "fail_ds_dig_miss": 0.0,
                },
                "conditionals": {
                    "p_eb_in_opening": p_eb,
                    "p_target_given_eb": 1.0,
                    "p_ds_given_missing_target": 0.0,
                }
            }
            if verbose:
                print("✅ All non-EB cards are targets — success = P(EB >= 1)")
            return result
    
    # ========== EXACT MULTIVARIATE ENUMERATION ==========
    from itertools import product
    
    total_combinations = math.comb(deck_size, opening_hand)
    
    p_path_a = 0.0
    ds_split = {0: 0.0, 1: 0.0, 2: 0.0}
    
    for e in range(0, min(eb_count, opening_hand) + 1):
        for t in range(0, min(target_count, opening_hand - e) + 1):
            for d in range(0, min(ds_count, opening_hand - e - t) + 1):
                o = opening_hand - e - t - d
                if o < 0 or o > other_count:
                    continue
                
                ways = (
                    math.comb(eb_count, e) *
                    math.comb(target_count, t) *
                    math.comb(ds_count, d) *
                    math.comb(other_count, o)
                )
                prob = ways / total_combinations
                
                if e >= 1 and t >= 1:
                    p_path_a += prob
                elif e >= 1 and t == 0:
                    ds_split[d] += prob
    
    # ========== PATHS B & C: Dig after opening ==========
    p_path_b1 = 0.0
    p_path_b2 = 0.0
    p_path_c = 0.0
    p_fail_2a = 0.0
    p_fail_2b = 0.0
    
    for ds_in_hand, base_prob in ds_split.items():
        if base_prob < 1e-10:
            continue
        
        p_turn_hit = target_count / remaining_deck
        p_turn_miss = 1 - p_turn_hit
        
        if ds_in_hand == 0:
            p_path_b1 += base_prob * p_turn_hit
            p_fail_2a += base_prob * p_turn_miss
        else:
            p_path_b2 += base_prob * p_turn_hit
            deck_after_turn = remaining_deck - 1
            p_ds_dig_hit = calc_hypergeom_cdf_ge(deck_after_turn, target_count, ds_draw_count, min_k=1)
            p_path_c += base_prob * p_turn_miss * p_ds_dig_hit
            p_fail_2b += base_prob * p_turn_miss * (1 - p_ds_dig_hit)
    
    # ========== P(no EB) ==========
    p_no_eb = 1 - calc_hypergeom_cdf_ge(deck_size, eb_count, opening_hand, min_k=1)
    
    # ========== Aggregate ==========
    total_success = p_path_a + p_path_b1 + p_path_b2 + p_path_c
    total_fail = p_no_eb + p_fail_2a + p_fail_2b
    
    result = {
        "total_success": total_success,
        "total_fail": total_fail,
        "paths": {
            "A_combo_in_opening": p_path_a,
            "B1_turn_draw_no_ds": p_path_b1,
            "B2_turn_draw_with_ds": p_path_b2,
            "C_ds_dig_success": p_path_c,
            "fail_no_eb": p_no_eb,
            "fail_no_ds_turn_miss": p_fail_2a,
            "fail_ds_dig_miss": p_fail_2b,
        },
        "conditionals": {
            "p_eb_in_opening": 1 - p_no_eb,
            "p_target_given_eb": p_path_a / (1 - p_no_eb) if (1 - p_no_eb) > 0 else 0,
            "p_ds_given_missing_target": (ds_split[1] + ds_split[2]) / sum(ds_split.values()) if sum(ds_split.values()) > 0 else 0,
        }
    }
    
    if verbose:
        print(f"🎲 Turn 1 Success Rate: {total_success:.2%}")
        print("\n📊 Path Breakdown:")
        for path, prob in result["paths"].items():
            status = "✅" if "success" in path or path.startswith("A") or path.startswith("B") else "❌"
            print(f"  {status} {path}: {prob:.2%}")
    
    return result


def monte_carlo_sim(
    deck_config: Dict[str, int],
    success_condition: callable,
    n_simulations: int = 100_000,
    seed: int = 42
) -> float:
    """
    Fallback Monte Carlo simulation for complex rule interactions.
    
    deck_config: dict of {card_category: count}
    success_condition: function(hand: List[str], deck: List[str]) -> bool
    n_simulations: number of trials
    """
    import random
    random.seed(seed)
    
    # Build deck list
    deck = []
    for category, count in deck_config.items():
        deck.extend([category] * count)
    
    success_count = 0
    
    for _ in range(n_simulations):
        random.shuffle(deck)
        opening = deck[:5]
        remaining = deck[5:]
        
        if success_condition(opening, remaining):
            success_count += 1
    
    return success_count / n_simulations