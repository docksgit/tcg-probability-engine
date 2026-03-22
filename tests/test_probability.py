"""
tests/test_probability.py

Unit tests for probability calculations.
"""

import pytest
from src.probability import calc_pocket_turn1_success, calc_hypergeom_cdf_ge


def test_expected_pocket_result():
    """Verify the main Pocket deck calculation is in expected range"""
    result = calc_pocket_turn1_success()
    # Allow tolerance for approximation (64-66%)
    assert 0.64 < result["total_success"] < 0.67, f"Expected ~0.64-0.67, got {result['total_success']}"


def test_no_eb_means_zero_success():
    """If no Energy Baby, success rate must be 0"""
    result = calc_pocket_turn1_success(
        eb_count=0, ex_count=4, es_count=1, ds_count=2, other_count=13
    )
    assert result["total_success"] == 0.0, f"Expected 0.0, got {result['total_success']}"
    assert result["paths"]["fail_no_eb"] == 1.0


def test_all_targets_guarantees_success():
    """If all non-EB cards are targets, success = P(EB >= 1)"""
    # 4 EB + 16 targets = 20 cards
    result = calc_pocket_turn1_success(
        eb_count=4, ex_count=16, es_count=0, ds_count=0, other_count=0
    )
    # With 4 EB in 20 cards, P(EB >= 1 in 5 cards) ≈ 71.8%
    # But since ALL non-EB are targets, if we have EB, we auto-succeed
    assert result["total_success"] > 0.70, f"Expected >0.70, got {result['total_success']}"


def test_hypergeom_basic():
    """Sanity check hypergeometric CDF"""
    p = calc_hypergeom_cdf_ge(N=20, K=4, n=5, min_k=1)
    expected = 1 - (16/20 * 15/19 * 14/18 * 13/17 * 12/16)
    assert abs(p - expected) < 1e-4