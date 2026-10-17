"""Pure structural checks and PyPhi-gated IIT integration checks."""
import pytest
from org_frontier.studies.six_of_eight_identifiability.experiment import (
    ALL_STATES, OBSERVED, UNOBSERVED, COMPLETIONS,
    step, trajectory, observed_witness, signatures, name, minimum_queries,
    structural, exact,
)


def test_reference_truth_tables():
    expected = {
        "000": "000", "001": "000", "010": "101", "011": "101",
        "100": "000", "101": "010", "110": "101", "111": "111",
    }
    assert {s: step(s, 0, 0) for s in ALL_STATES} == expected
    assert {s: step(s, 1, 1) for s in ALL_STATES} == (expected | {"100": "010", "110": "111"})


def test_observation_support_closed():
    assert len(observed_witness()) == 6
    for a, b in COMPLETIONS:
        assert {step(s, a, b) for s in OBSERVED} <= set(OBSERVED)
        for s in OBSERVED:
            assert trajectory(s, a, b, 100) == trajectory(s, 0, 0, 100)


def test_reachable_state_set_and_hidden_states():
    assert set(ALL_STATES) - set(OBSERVED) == set(UNOBSERVED)
    assert set(UNOBSERVED) == {"100", "110"}
    for a, b in COMPLETIONS:
        assert {step(s, a, b) for s in ALL_STATES} == {"000", "010", "101", "111"}


def test_four_completion_signatures():
    assert len(COMPLETIONS) == 4
    tables = {tuple(step(s, a, b) for s in ALL_STATES) for a, b in COMPLETIONS}
    assert len(tables) == 4
    assert len(set(signatures(("100",)).values())) == 2
    assert len(set(signatures(("110",)).values())) == 2


def test_minimal_diagnostics():
    ids = {name(a, b): (a, b) for a, b in COMPLETIONS}
    assert minimum_queries(ids) == {"minimum_queries": 2, "query_sets": [["100", "110"]]}
    assert minimum_queries({k: "same" for k in ids})["minimum_queries"] == 0
    assert minimum_queries({name(a, b): a for a, b in COMPLETIONS}) == {
        "minimum_queries": 1, "query_sets": [["100"]]}
    assert minimum_queries({name(a, b): a ^ b for a, b in COMPLETIONS})["minimum_queries"] == 2


def test_structural_output():
    r = structural()
    assert r["observed_rows"]["010"] == "101"
    assert r["A_B_distinguishing_interventions"] == ["100", "110"]
    assert r["full_rule_identification"]["minimum_queries"] == 2


def test_exact_iit_controls_with_pyphi():
    pytest.importorskip("pyphi")
    r = exact()
    models = r["exact_iit_4"]["models"]
    assert len(models) == 4
    assert models["a0_b0"]["verdict"] == "triadic"
    assert models["a1_b1"]["verdict"] == "dyadic"
    assert r["exact_iit_4"]["minimum_queries_to_identify_verdict"] == {
        "minimum_queries": 1, "query_sets": [["110"]]}
    assert {k: (v["verdict"], v["max_phi"]) for k, v in models.items()} == {
        "a0_b0": ("triadic", 2.0), "a0_b1": ("dyadic", 0.0),
        "a1_b0": ("triadic", 2.0), "a1_b1": ("dyadic", 0.0),
    }
    assert models["a1_b0"]["major_complex"] == ["W", "S"]
    assert models["a0_b0"]["major_complex"] == ["W", "S", "C"]
