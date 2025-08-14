from calculations import (
    calculate_damage_p
)

def generate_alloc_points(S, K, I, F, CR0, CD0):
    """
    Generates all non-negative integer point allocations (x, y, z) that sum to S,
    calculates the damage for each, and returns the results.
    """
    results = []

    for x in range(S + 1):
        for y in range(S - x + 1):
            z = S - x - y
            dmg = calculate_damage_p(K, I, F, CR0, CD0, x, y, z)

            # Results as input to heat map
            results.append({
                'x': x,
                'y': y,
                'z': z,
                'damage': dmg
            })
    return results