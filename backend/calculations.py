import math

# Constants and point allocation formulas
def calculate_C1_crit_ratio_constant(CR0, CD0):
    """
    Calculates the C1 constant, which represents a critical ratio used in
    the allocation of points for x, y, and z. This constant helps normalize
    the relationship between initial Crit Damage (CD0) and Crit Rate (CR0).

    Args:
        CD0 (float): Initial Critical Damage percentage.
        CR0 (float): Initial Critical Rate percentage.

    Returns:
        float: The calculated C1 critical ratio constant, how much more cdmg than crate above the 1:2 ratio.
    """
    return (CD0 - 2 * CR0 + 40) / 4.8

def get_x_from_z(S, C1_crit_ratio_constant, z):
    """
    Determines the value of 'x' (points allocated to Attack) based on
    the total available points 'S', the C1 constant, and the 'z' value
    (points allocated to Crit Damage). This formula ensures that the
    total points distributed (x + y + z) sum up to S, given the relationship
    between y and z.

    Args:
        S (float): Total available points to distribute.
        C1_crit_ratio_constant (float): The C1 constant, how much more cdmg than crate above the 1:2 ratio.
        z (float): Points allocated to Critical Damage.

    Returns:
        float: The calculated value for 'x'.
    """
    return S - C1_crit_ratio_constant - 2 * z

def get_y_from_z(C1_crit_ratio_constant, z):
    """
    Determines the value of 'y' (points allocated to Crit Rate) based on
    the C1 constant and the 'z' value (points allocated to Crit Damage).
    This formula maintains a specific ratio between 'y' and 'z' based on C1.

    Args:
        C1_crit_ratio_constant (float): The C1 constant, how much more cdmg than crate above the 1:2 ratio.
        z (float): Points allocated to Critical Damage.

    Returns:
        float: The calculated value for 'y'.
    """
    return z + C1_crit_ratio_constant

# Base L-coefficients
def calculate_base_L_coefficients(K, I, F, CR0, CD0):
    """
    Calculates the base 'L' coefficients for Attack, Crit Rate, and Crit Damage.
    These coefficients represent the inherent scaling and initial values for
    each stat before point allocation. They are fundamental building blocks
    for the subsequent calculations.

    Args:
        K (float): Base Attack multiplier.
        I (float): Attack scaling from an investment stat (e.g., character level, weapon).
        F (float): Flat Attack bonus.
        CR0 (float): Initial Critical Rate percentage.
        CD0 (float): Initial Critical Damage percentage.

    Returns:
        dict: A dictionary containing the base L-coefficients for ATK, CR, and CD.
              Keys include:
              - 'ATK_Base_Flat_Const': Base Attack constant.
              - 'ATK_Points_x_Coeff': Coefficient for Attack scaling with 'x' points.
              - 'CR_Base_Flat_Const': Base Crit Rate constant.
              - 'CR_Points_y_Coeff': Coefficient for Crit Rate scaling with 'y' points.
              - 'CD_Base_Flat_Const': Base Crit Damage constant.
              - 'CD_Points_z_Coeff': Coefficient for Crit Damage scaling with 'z' points.
    """
    # Dictionary to store for easy access
    base_L_coeffs = {
        'ATK_Base_Flat_Const': K + K * I / 100 + F,
        'ATK_Points_x_Coeff': K * 3 / 100,
        'CR_Base_Flat_Const': (CR0 + 5) / 100,
        'CR_Points_y_Coeff': 2.4 / 100,
        'CD_Base_Flat_Const': (CD0 + 50) / 100,
        'CD_Points_z_Coeff': 4.8 / 100
    }
    return base_L_coeffs

# Component Terms (A(z), CR(z), CD(z)) coefficients
def calculate_component_z_coefficients(base_L_coeffs, S, C1_crit_ratio_constant):
    """
    Calculates the coefficients for Attack (A(z)), Crit Rate (CR(z)), and
    Crit Damage (CD(z)) expressed as linear functions of 'z'. This step
    substitutes the expressions for 'x' and 'y' (which depend on 'z') into
    the base L-coefficient formulas to represent all stats in terms of 'z'.

    Args:
        base_L_coeffs (dict): Dictionary of base L-coefficients.
        S (float): Total available points.
        C1_crit_ratio_constant (float): The C1 constant.

    Returns:
        dict: A dictionary containing the constant and linear coefficients
              for A(z), CR(z), and CD(z). Keys include:
              - 'A_z_Constant': Constant term for A(z).
              - 'A_z_Coeff': Coefficient of 'z' for A(z).
              - 'CR_z_Constant': Constant term for CR(z).
              - 'CR_z_Coeff': Coefficient of 'z' for CR(z).
              - 'CD_z_Constant': Constant term for CD(z).
              - 'CD_z_Coeff': Coefficient of 'z' for CD(z).
    """
    comp_z_coeffs = {}

    # A(z) = A_z_Constant + A_z_Coeff * z
    # A(z) = (K + K*I/100 + F) + (K*3/100) * x
    # Substitute x = S - C1 - 2z
    comp_z_coeffs['A_z_Constant'] = base_L_coeffs['ATK_Base_Flat_Const'] + \
                                     base_L_coeffs['ATK_Points_x_Coeff'] * S - \
                                     base_L_coeffs['ATK_Points_x_Coeff'] * C1_crit_ratio_constant
    comp_z_coeffs['A_z_Coeff'] = -2 * base_L_coeffs['ATK_Points_x_Coeff']

    
    # CR(z) = CR_z_Constant + CR_z_Coeff * z
    # CR(z) = (CR0 + 5)/100 + (2.4/100) * y
    # Substitute y = z + C1
    comp_z_coeffs['CR_z_Constant'] = base_L_coeffs['CR_Base_Flat_Const'] + \
                                      base_L_coeffs['CR_Points_y_Coeff'] * C1_crit_ratio_constant
    comp_z_coeffs['CR_z_Coeff'] = base_L_coeffs['CR_Points_y_Coeff']

    # CD(z) = CD_z_Constant + CD_z_Coeff * z
    # CD(z) = (CD0 + 50)/100 + (4.8/100) * z
    # no substitution since we solve in terms of z
    comp_z_coeffs['CD_z_Constant'] = base_L_coeffs['CD_Base_Flat_Const']
    comp_z_coeffs['CD_z_Coeff'] = base_L_coeffs['CD_Points_z_Coeff']

    return comp_z_coeffs

# Crit Product Term coefficients
def calculate_crit_product_coefficients(comp_z_coeffs):
    """
    Calculates the coefficients for the Critical Product term (CR(z) * CD(z)).
    Since CR(z) and CD(z) are linear functions of 'z', their product will
    result in a quadratic function of 'z' (i.e., CR_Prod_z2 * z^2 + CR_Prod_z1 * z + CR_Prod_z0).
    This term is a crucial part of the overall damage formula.

    Args:
        comp_z_coeffs (dict): Dictionary of component Z-coefficients.

    Returns:
        dict: A dictionary containing the quadratic coefficients for the
              Crit Product term. Keys include:
              - 'CR_Prod_z2_Coeff': Coefficient of z^2.
              - 'CR_Prod_z1_Coeff': Coefficient of z.
              - 'CR_Prod_z0_Coeff': Constant term.
    """
    cr_prod_coeffs = {}
    cr_prod_coeffs['CR_Prod_z2_Coeff'] = comp_z_coeffs['CR_z_Coeff'] * comp_z_coeffs['CD_z_Coeff']
    cr_prod_coeffs['CR_Prod_z1_Coeff'] = comp_z_coeffs['CR_z_Constant'] * comp_z_coeffs['CD_z_Coeff'] + \
                                           comp_z_coeffs['CR_z_Coeff'] * comp_z_coeffs['CD_z_Constant']
    cr_prod_coeffs['CR_Prod_z0_Coeff'] = comp_z_coeffs['CR_z_Constant'] * comp_z_coeffs['CD_z_Constant']
    return cr_prod_coeffs

# Main function to get quadratic coefficients
def get_quadratic_coefficients(K, I, F, S, CR0, CD0):
    """
    Calculates the coefficients (A_final, B_final, C_final) for the quadratic
    equation P'(z) = A_final * z^2 + B_final * z + C_final = 0.
    P(z) represents the total damage, which is defined as Attack * (1 + CritRate * CritDamage).
    To find the optimal 'z' that maximizes P(z), we take its first derivative P'(z) and
    set it to zero. This function systematically derives the coefficients for P'(z).

    The overall process can be broken down into these main stages:

    Stage 1: Expressing all stat allocations (x, y) in terms of z.
    Stage 2: Calculating base stat coefficients (L-coefficients).
    Stage 3: Expressing total Attack, Crit Rate, and Crit Damage as functions of z.
    Stage 4: Calculating the Crit Product term (Crit Rate * Crit Damage) as a function of z.
    Stage 5: Forming the full P(z) polynomial and its derivative P'(z).
    Stage 6: Extracting the quadratic coefficients from P'(z).

    Args:
        K (float): Base Attack multiplier.
        I (float): Attack scaling from an investment stat.
        F (float): Flat Attack bonus.
        S (float): Total available points to distribute.
        CR0 (float): Initial Critical Rate percentage.
        CD0 (float): Initial Critical Damage percentage.

    Returns:
        tuple: A tuple containing the coefficients (A_final, B_final, C_final) for
               the quadratic equation P'(z) = 0.
               P'(z) = A_final * z^2 + B_final * z + C_final.
    """
    # Step 1: Calculate C1
    C1_crit_ratio_constant = calculate_C1_crit_ratio_constant(CR0, CD0)

    # Step 2: Calculate Base L-coefficients
    base_L_coeffs = calculate_base_L_coefficients(K, I, F, CR0, CD0)

    # Step 3: Calculate Component Z-coefficients (A(z), CR(z), CD(z))
    comp_z_coeffs = calculate_component_z_coefficients(base_L_coeffs, S, C1_crit_ratio_constant)

    # Step 4: Calculate Crit Product Coefficients
    cr_prod_coeffs = calculate_crit_product_coefficients(comp_z_coeffs)

    # Step 5: Calculate P(z) coefficients (P_z3, P_z2, P_z1, P_z0)

    # Form the full P(z) polynomial and its derivative P'(z)
    # P(z) = A(z) * (1 + CR(z) * CD(z))
    # P(z) = (A_z_Constant + A_z_Coeff * z) * (1 + CR_Prod_z2_Coeff * z^2 + CR_Prod_z1_Coeff * z + CR_Prod_z0_Coeff)
    # Expanding this product will give a cubic polynomial in z:
    P_z3_Coeff = comp_z_coeffs['A_z_Coeff'] * cr_prod_coeffs['CR_Prod_z2_Coeff']
    P_z2_Coeff = comp_z_coeffs['A_z_Constant'] * cr_prod_coeffs['CR_Prod_z2_Coeff'] + \
                 comp_z_coeffs['A_z_Coeff'] * cr_prod_coeffs['CR_Prod_z1_Coeff']
    P_z1_Coeff = comp_z_coeffs['A_z_Constant'] * cr_prod_coeffs['CR_Prod_z1_Coeff'] + \
                 comp_z_coeffs['A_z_Coeff'] * (1 + cr_prod_coeffs['CR_Prod_z0_Coeff'])
    # P_z0_Coeff is not needed for the derivative, but for completeness:
    # P_z0_Coeff = comp_z_coeffs['A_z_Constant'] * (1 + cr_prod_coeffs['CR_Prod_z0_Coeff'])


    # Step 6: Identify A_final, B_final, C_final for P'(z) = 0
    A_final = 3 * P_z3_Coeff
    B_final = 2 * P_z2_Coeff
    C_final = P_z1_Coeff

    return A_final, B_final, C_final

def solve_quadratic(a, b, c):
    """Solves a quadratic equation ax^2 + bx + c = 0 and returns real roots."""
    if a == 0: # Linear equation
        if b == 0:
            return [] if c != 0 else [0] # No solution or infinite solutions (treating as zero)
        return [-c / b]

    discriminant = b**2 - 4*a*c
    if discriminant < 0:
        return [] # No real roots
    elif discriminant == 0:
        return [-b / (2*a)]
    else:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        return [root1, root2]
    
def best_integer_allocation(x, y, z, S, damage_fn, source_label):
    """
    Finds the best integer allocation (xi, yi, zi) that sums to S by
    performing a small local search around the floating-point solution (x, y, z).
    
    Args:
        x (float): The number of points allocated to Scaling Unit.
        y (float): The number of points allocated to Crit Rate.
        z (float): The number of points allocated to Crit Damage.
        S (int): The total available points to allocate.
        damage_fn (function): A function that calculates the damage based on x, y, and z.
        source_label (str): A label indicating the source of the allocation.

    Returns:
        dict: A dictionary containing the best allocation (x, y, z) and the corresponding damage,
              or None if no valid integer allocation is found.
    """
    best = None
    
    # We define a small search radius around the continuous solution.
    # A radius of 2 is typically sufficient for this type of problem.
    search_radius = 2

    # Iterate through a small integer range around the continuous x and y values.
    # The 'max(0, ...)' ensures we never check for negative points.
    x_range = range(int(max(0, x - search_radius)), int(x + search_radius + 1))
    y_range = range(int(max(0, y - search_radius)), int(y + search_radius + 1))
    
    for xi in x_range:
        for yi in y_range:
            zi = S - xi - yi
            
            # Check if zi is a valid, non-negative integer.
            if zi >= 0:
                damage = damage_fn(xi, yi, zi)
                
                if best is None or damage > best['damage']:
                    best = {'x': xi, 'y': yi, 'z': zi, 'damage': damage, 'source': source_label}
    
    return best

def calculate_damage_p(K, I, F, CR0, CD0, x, y, z):
    """Calculates the total damage P for given x, y, z allocations."""
    # Ensure points are non-negative for this calculation
    if x < 0 or y < 0 or z < 0:
        return 0 # Or raise an error, depending on desired handling

    # Attack (A)
    A_val = K * (1 + (I + 3 * x) / 100) + F

    # Crit Rate (CR)
    CR_val = (CR0 + 5 + 2.4 * y) / 100
    # Cap CR at 100% (1.0)
    CR_val = min(CR_val, 1.0)

    # Crit Damage (CD)
    CD_val = (CD0 + 50 + 4.8 * z) / 100

    # Total Damage (P)
    P_val = A_val * (1 + CR_val * CD_val)
    return P_val

def solve_cr_capped_case(K, I, F, CR0, CD0, S_prime, y_cap):
    """
    Optimizes for the best allocation of points to Attack (x) and Crit Damage (z) 
    while keeping Crit Rate (y) capped at 100%.

    Args:
        K (float): Base Attack multiplier.
        I (float): Attack scaling from an investment stat.
        F (float): Flat Attack bonus.
        CD0 (float): Initial Crit Damage.
        S_prime (float): The remaining points to distribute after capping Crit Rate.
        y_cap (float): The number of points allocated to Crit Rate when capped at 100%.

    Returns:
        dict: A dictionary containing the optimal allocation (x, y, z) and the corresponding damage.
    """
    # Constants
    A1 = -K * 3 / 100  # Coefficient of z in A(x) due to x = S' - z
    A0 = K * (1 + (I + 3 * S_prime) / 100) + F  # A(x) when z = 0

    CD_base = (CD0 + 50) / 100
    CD_slope = 4.8 / 100

    # P(z) = (A0 + A1 * z) * (1 + CD_base + CD_slope * z)
    # => P(z) = quadratic: P(z) = a*z^2 + b*z + c

    a = A1 * CD_slope
    b = A0 * CD_slope + A1 * (1 + CD_base)
    c = A0 * (1 + CD_base)

    # Find optimal z = -b / 2a
    if a == 0:
        z_opt = 0 if b <= 0 else S_prime  # Linear case
    else:
        z_opt = -b / (2 * a)

    # Clamp to valid z range
    z_candidates = [
        int(max(0, min(S_prime, math.floor(z_opt)))),
        int(max(0, min(S_prime, math.ceil(z_opt))))
    ]

    best = {'damage': 0}
    for z in z_candidates:
        x = S_prime - z
        damage = calculate_damage_p(K, I, F, CR0, CD0, x, y_cap, z)
        if damage > best.get('damage', 0):
            best = {
                'x': x,
                'y': y_cap,
                'z': z,
                'damage': damage,
                'source': 'CR Capped (y=y_cap)'
            }

    return best

def get_scenario_solutions(K, I, F, S, CR0, CD0):
    """
    Finds potential optimal solutions from various scenarios (main, x=0, y=0, z=0, corners).
    Returns a list of dictionaries, each with {'x', 'y', 'z', 'damage'}.
    """
    solutions = []

    # --- 1. Main Quadratic Solution (potentially 2 solutions) ---
    try:
        c1_val = calculate_C1_crit_ratio_constant(CR0, CD0) 

        a_final, b_final, c_final = get_quadratic_coefficients(K, I, F, S, CR0, CD0)
        
        z_candidates = solve_quadratic(a_final, b_final, c_final)
        
        for z_opt in z_candidates:
            if z_opt >= 0:
                # Assuming x and y are derived from z based on the primary optimization path

                # x = S - C1_val - 2z
                # y = C1_val + z

                y_opt = get_y_from_z(c1_val, z_opt)
                x_opt = get_x_from_z(S, c1_val, z_opt)

                # Check validity
                if x_opt >= 0 and y_opt >= 0:
                    best = best_integer_allocation(x_opt, y_opt, z_opt, S,
                        lambda xi, yi, zi: calculate_damage_p(K, I, F, CR0, CD0, xi, yi, zi),
                        source_label='Main Quadratic')
                    if best:
                        solutions.append(best)
    except ValueError as e:
        # e.g., no real roots, so optimal is on boundary
        print(f"Main quadratic solution failed: {e}. Checking boundaries.")
        pass # Will proceed to boundary checks

    # --- 2. Boundary Cases ---
    # a. All Attack (x=S, y=0, z=0)
    damage_all_atk = calculate_damage_p(K, I, F, CR0, CD0, S, 0, 0)
    solutions.append({'x': S, 'y': 0, 'z': 0, 'damage': damage_all_atk, 'source': 'All Attack (x=S)'})

    # b. All Crit Rate (x=0, y=S, z=0)
    damage_all_cr = calculate_damage_p(K, I, F, CR0, CD0, 0, S, 0)
    solutions.append({'x': 0, 'y': S, 'z': 0, 'damage': damage_all_cr, 'source': 'All Crit Rate (y=S)'})

    # c. All Crit Damage (x=0, y=0, z=S)
    damage_all_cd = calculate_damage_p(K, I, F, CR0, CD0, 0, 0, S)
    solutions.append({'x': 0, 'y': 0, 'z': S, 'damage': damage_all_cd, 'source': 'All Crit Damage (z=S)'})

    # d. Fixed x=0 (optimize y and z given y+z=S)
    # In this case, we've solved for y = C1 + z already, so simply use that.
    if S > c1_val:
        z = (S - c1_val) / 2
        y = (S + c1_val) / 2
        if y > 0 and z > 0:
            ceil_y = calculate_damage_p(K, I, F, CR0, CD0, 0, math.ceil(y), math.floor(z))
            floor_y = calculate_damage_p(K, I, F, CR0, CD0, 0, math.floor(y), math.ceil(z))
            if ceil_y > floor_y:
                solutions.append({'x': 0, 'y': math.ceil(y), 'z': math.floor(z), 'damage': ceil_y, 'source': 'No Attack (x=0)'})
            else:
                solutions.append({'x': 0, 'y': math.floor(y), 'z': math.ceil(z), 'damage': floor_y, 'source': 'No Attack (x=0)'})



    # e. Capped crit rate (optimize x and z given y gives 100 percent crit rate)
    # Calculate S' and then optimize for x and z
    y_cap = max(0, math.ceil((100 - (CR0 + 5)) / 2.4))
    S_prime = S - y_cap

    if S_prime >= 0:
        capped_solution = solve_cr_capped_case(K, I, F, CR0, CD0, S_prime, y_cap)
        solutions.append(capped_solution)

    return solutions

def find_global_optimal_build(K, I, F, S, CR0, CD0, return_all=False):
    """
    Orchestrates the entire optimization process to find the global optimal build.
    """
    all_potential_solutions = get_scenario_solutions(K, I, F, S, CR0, CD0)

    if not all_potential_solutions:
        return {'x': 0, 'y': 0, 'z': 0, 'damage': 0, 'error': "No valid solutions found for given inputs."}

    # Find the solution with the maximum damage
    best_solution = max(all_potential_solutions, key=lambda sol: sol['damage'])

    if return_all:
        return {"best": best_solution, "all": all_potential_solutions}
    return best_solution
