#!/usr/bin/env python3
"""Recompute projective base strata and their payoff jets over prime fields."""
from collections import Counter
from itertools import product

ROW = (0, 1, 2, 3)
COLUMN = (0, 2, 1, 3)


def rank(vectors, p):
    rows = [[entry % p for entry in row] for row in vectors]
    pivot = 0
    for j in range(len(rows[0]) if rows else 0):
        index = next((i for i in range(pivot, len(rows)) if rows[i][j]), None)
        if index is None:
            continue
        rows[pivot], rows[index] = rows[index], rows[pivot]
        leading = rows[pivot]
        scale = pow(leading[j], -1, p)
        for i in range(pivot + 1, len(rows)):
            multiplier = rows[i][j] * scale
            rows[i] = [(a - multiplier*b) % p for a, b in zip(rows[i], leading)]
        pivot += 1
    return pivot


def payoff_jets(point, order, pivot, p):
    """Return the four jets in a normalized projective chart if all values vanish."""
    first, last = order[:2], order[2:]
    row_sums = (sum(point[j] for j in first), sum(point[j] for j in last))
    chart = [j for j in range(4) if j != pivot]
    jets = []
    for action, indices in enumerate((first, last)):
        other = (last, first)[action]
        sign = (-1)**action
        opposite_sum = row_sums[1 - action]
        for k in indices:
            if point[k] * opposite_sum % p:
                return None
            jets.append(tuple(
                sign * (opposite_sum*(j == k) + point[k]*(j in other)) % p
                for j in chart
            ))
    return jets


def projective_points(p):
    for pivot in range(4):
        for tail in product(range(p), repeat=3-pivot):
            yield (0,)*pivot + (1,) + tail, pivot


def plane(vectors, p):
    basis = []
    for v in vectors:
        if rank(basis + [v], p) > len(basis):
            basis.append(v)
    return {
        tuple(sum(a*v[j] for a, v in zip(coeffs, basis)) % p for j in range(3))
        for coeffs in product(range(p), repeat=len(basis))
    }


def check_mixed(row_jets, column_jets, p):
    assert (rank(row_jets, p), rank(column_jets, p)) == (2, 2)
    assert rank(row_jets + column_jets, p) == 3
    row_plane, column_plane = plane(row_jets, p), plane(column_jets, p)
    common = row_plane & column_plane
    assert len(common) == p
    zero = (0, 0, 0)
    bad_count = 0
    for u, v in product(row_plane, column_plane):
        dependent = rank([u, v], p) < 2
        assert dependent == (u == zero or v == zero or (u in common and v in common))
        bad_count += dependent
    assert bad_count == 2*p*p - 1 + (p - 1)**2
    return bad_count


def check_projection_and_jets(p):
    counts = Counter()
    bad_count = None
    for point, pivot in projective_points(p):
        row_jets = payoff_jets(point, ROW, pivot, p)
        column_jets = payoff_jets(point, COLUMN, pivot, p)
        if row_jets is not None and column_jets is not None:
            assert sum(bool(x) for x in point) == 1 or point == (1, p-1, p-1, 1)
            bad_count = check_mixed(row_jets, column_jets, p)
            counts["mixed"] += 1
        elif row_jets is not None or column_jets is not None:
            counts[f"rank-{rank(row_jets or column_jets, p)}"] += 1
        else:
            counts["outside"] += 1
    assert counts["mixed"] == 5
    assert counts["rank-1"] == 4
    assert counts["rank-2"] == 6*(p-2)
    assert counts["outside"] == p**3+p**2+p+1 - 9 - 6*(p-2)
    print(f"F_{p}: 5 mixed points, 4 rank-one points, {counts['rank-2']} open-line points, "
          f"{counts['outside']} outside; {bad_count} of {p**4} mixed pairs dependent.")


for prime in (3, 5, 7):
    check_projection_and_jets(prime)
print("PASS: local base geometry and rank-loss diagnostics.")
