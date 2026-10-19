"""Structural tests and optional exact IIT-4.0 tests for the posthoc 64-model panel."""
import pytest
from org_frontier.studies.six_of_eight_identifiability.exploratory_full_rows import (
    enumerate_completions, model_id, query_analysis, rule_functions,
    structural, exact,
)
from org_frontier.studies.six_of_eight_identifiability.experiment import ALL_STATES, OBSERVED, UNOBSERVED, bits, label, rules, step


def test_sixty_four_distinct_models_agree_on_observed_transitions():
    models = enumerate_completions()
    assert len(models) == 64
    assert len({tuple(t[s] for s in ALL_STATES) for t in models.values()}) == 64
    for t in models.values():
        assert all(t[s] == step(s, 0, 0) for s in OBSERVED)
        assert {t[s] for s in OBSERVED} <= set(OBSERVED)


def test_models_and_bitwise_rule_construction_match():
    for key, table in enumerate_completions().items():
        fs = rule_functions(table)
        for s in ALL_STATES:
            assert label(fn(bits(s)) for fn in fs) == table[s]


def test_exploratory_contains_original_four_family():
    models = enumerate_completions()
    assert model_id("000", "101") in models
    assert model_id("000", "111") in models
    assert model_id("010", "101") in models
    assert model_id("010", "111") in models
    assert structural()["num_completions"] == 64


def test_query_optimizer_on_constructed_verdict_maps():
    models = enumerate_completions()
    constant = {k: "dyadic" for k in models}
    assert query_analysis(models, constant)["minimum_global_queries"] == 0
    depends_on_110 = {
        k: ("triadic" if t["110"][0] == "1" else "dyadic")
        for k, t in models.items()
    }
    assert query_analysis(models, depends_on_110)["sufficient_minimal_query_sets"] == [["110"]]
    depends_on_both = {
        k: ("triadic" if t["100"][0] == t["110"][0] else "dyadic")
        for k, t in models.items()
    }
    assert query_analysis(models, depends_on_both)["minimum_global_queries"] == 2


def test_actual_exact_sixty_four_completions():
    pytest.importorskip("pyphi")
    out = exact()
    assert len(out["exact_iit_4"]["models"]) == 64
    assert sum(out["exact_iit_4"]["verdict_counts"].values()) == 64
    assert out["exact_iit_4"]["verdict_counts"] == {"triadic": 48, "dyadic": 16}
    assert out["exact_iit_4"]["phi_min"] == 0.0
    assert out["exact_iit_4"]["phi_max"] == 2.0
    assert out["exact_iit_4"]["query_analysis"]["minimum_global_queries"] == 2
    assert out["exact_iit_4"]["query_analysis"]["sufficient_minimal_query_sets"] == [["100", "110"]]
    singleton = {tuple(x["states"]): x for x in out["exact_iit_4"]["query_analysis"]["candidate_subsets"]}
    assert singleton[("100",)]["ambiguous_outcome_groups"] == 8
    assert singleton[("110",)]["ambiguous_outcome_groups"] == 2
