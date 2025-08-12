import pytest
import math
from calculations import (
    calculate_C1_crit_ratio_constant,
    get_x_from_z,
    get_y_from_z,
    calculate_damage_p,
    get_quadratic_coefficients,
    solve_quadratic,
    best_integer_allocation,
    find_global_optimal_build
)

# Test data for a specific scenario
TEST_PARAMS = {
    'K': 1000,
    'I': 60,
    'F': 100,
    'S': 40,
    'CR0': 5,
    'CD0': 50
}

# --- Test Core Calculation Functions ---
def test_calculate_C1_crit_ratio_constant():
    cr0_test = 50
    cd0_test = 100
    expected_c1 = (100 - 2 * 50 + 40) / 4.8
    assert calculate_C1_crit_ratio_constant(cr0_test, cd0_test) == pytest.approx(expected_c1)
    
def test_get_x_from_z():
    S, C1, z = 40, 10, 5
    expected_x = 40 - 10 - 2*5
    assert get_x_from_z(S, C1, z) == expected_x

def test_get_y_from_z():
    C1, z = 10, 5
    expected_y = 5 + 10
    assert get_y_from_z(C1, z) == expected_y

# --- Test Main Optimization Logic ---
def test_get_quadratic_coefficients():

    a_final, b_final, c_final = get_quadratic_coefficients(**TEST_PARAMS)
    assert a_final == pytest.approx(-0.20736)
    assert b_final == pytest.approx(-0.2304)
    assert c_final == pytest.approx(25.2)

def test_solve_quadratic():
    roots = solve_quadratic(1, -3, 2)
    assert set(roots) == set([1.0, 2.0])
    
    roots = solve_quadratic(1, 1, 1)
    assert roots == []

# --- Test Integer Allocation Logic ---
def test_best_integer_allocation_valid_search():
    # A valid continuous solution for a different set of parameters
    params_with_interior_opt = {
        'K': 1000, 'I': 300, 'F': 100, 'CR0': 100, 'CD0': 100
    }
    x_cont, y_cont, z_cont = 20, 30.5, 49.5 # A hypothetical interior optimum
    
    damage_fn = lambda x, y, z: calculate_damage_p(**params_with_interior_opt, x=x, y=y, z=z)
    best_sol = best_integer_allocation(x_cont, y_cont, z_cont, 100, damage_fn, 'Test')
    
    assert best_sol is not None
    # Check that the sum constraint is met and it's an integer solution
    assert best_sol['x'] + best_sol['y'] + best_sol['z'] == 100
    assert isinstance(best_sol['x'], int)
    assert isinstance(best_sol['y'], int)
    assert isinstance(best_sol['z'], int)
    
    # Don't know the exact value, but we can verify it's a valid point
    assert best_sol['x'] >= 0
    assert best_sol['y'] >= 0
    assert best_sol['z'] >= 0

# --- Test End-to-End Logic ---
def test_find_global_optimal_build():
    optimal_build = find_global_optimal_build(**TEST_PARAMS)
    
    assert optimal_build is not None
    assert 'damage' in optimal_build
    assert 'x' in optimal_build
    assert 'y' in optimal_build
    assert 'z' in optimal_build
    assert optimal_build['x'] + optimal_build['y'] + optimal_build['z'] == TEST_PARAMS['S']
    assert optimal_build['x'] >= 0
    assert optimal_build['y'] >= 0
    assert optimal_build['z'] >= 0

def test_best_integer_allocation_new_params():
    # verified floating point solution
    x_cont = 2.368537237
    y_cont = 27.14906571
    z_cont = 10.4823905
    S = TEST_PARAMS['S']

    #FP damage
    expected_fp_damage = 3771.88487
    
    # We create a specific damage function for this test case
    damage_fn = lambda x, y, z: calculate_damage_p(K=TEST_PARAMS['K'],
        I=TEST_PARAMS['I'],
        F=TEST_PARAMS['F'],
        CR0=TEST_PARAMS['CR0'],
        CD0=TEST_PARAMS['CD0'], x=x, y=y, z=z)

    # Perform the integer allocation based on solution
    best_sol = best_integer_allocation(x_cont, y_cont, z_cont, S, damage_fn, 'Test')

    # Now we can make some specific assertions based on data
    assert best_sol is not None
    assert isinstance(best_sol['x'], int)
    assert isinstance(best_sol['y'], int)
    assert isinstance(best_sol['z'], int)
    assert best_sol['x'] + best_sol['y'] + best_sol['z'] == S
    
    best_integer_damage = best_sol['damage']
    assert best_integer_damage == pytest.approx(expected_fp_damage, rel=0.01) # 1% tolerance
    
    assert abs(best_sol['x'] - x_cont) <= 2
    assert abs(best_sol['y'] - y_cont) <= 2
    assert abs(best_sol['z'] - z_cont) <= 2

# --- Test End-to-End Logic Parameters ---
def test_find_global_optimal_build_new_params():

    # The nearby integer points that sum to 40 are:
    # (2, 27, 11), (2, 28, 10), (3, 27, 10), etc.
    # A quick manual calculation with damage formula shows that
    # the solution (3, 27, 10) yields the highest damage.
    
    optimal_build = find_global_optimal_build(**TEST_PARAMS)
    
    assert optimal_build is not None
    assert 'damage' in optimal_build
    assert optimal_build['x'] + optimal_build['y'] + optimal_build['z'] == TEST_PARAMS['S']
    
    # verify solution
    assert optimal_build['damage'] == pytest.approx(3771.8596, rel=0.01)
    
    
    assert optimal_build['x'] == 3
    assert optimal_build['y'] == 27
    assert optimal_build['z'] == 10