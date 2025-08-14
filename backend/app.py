from flask import Flask, request, jsonify
from flask_cors import CORS
from calculations import find_global_optimal_build
from graphing import generate_alloc_points
import logging
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', force=True)

app = Flask(__name__)
CORS(app) # for development purposes allow all

logger = logging.getLogger(__name__)

@app.route('/api/calculate', methods=['POST'])

def calculate():
    if not request.json:
        return jsonify({"error": "Invalid request, must be JSON"}), 400
    
    try:
        K = float(request.json.get('K'))
        I = float(request.json.get('I'))
        F = float(request.json.get('F'))
        S = int(request.json.get('S'))
        CR0 = float(request.json.get('CR0'))
        CD0 = float(request.json.get('CD0'))
    except (TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid input data: {e}"}), 400
    # Placeholder values
    optimal_x = 12.34
    optimal_y = 56.78
    optimal_z = 90.12
    max_damage = 7500.50

    # Call optimization function
    optimal_build = find_global_optimal_build(K, I, F, S, CR0, CD0)

    # Generate data for graph
    visualization_data = generate_alloc_points(S, K, I, F, CR0, CD0)

    # Check if a valid solution was found
    if optimal_build.get('error'):
        return jsonify(optimal_build), 404

    return jsonify({
        "optimal_x": optimal_build['x'],
        "optimal_y": optimal_build['y'],
        "optimal_z": optimal_build['z'],
        "max_damage": optimal_build['damage'],
        "source": optimal_build['source'],
        "visualization_data": visualization_data
    })

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="calculus based stat allocation optimizer")
    parser.add_argument('--log_level', type=str, default='INFO', help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).')

    args = parser.parse_args()

    level = getattr(logging, args.log_level.upper(), logging.INFO)
    
    logging.basicConfig(level=level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', force=True)

    app.run(debug=True, port=5000) # Run Flask on port 5000