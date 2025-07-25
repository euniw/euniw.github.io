from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # for development purposes allow all

@app.route('/api/calculate', methods=['POST'])

def calculate():
    if not request.json:
        return jsonify({"error": "Invalid request, must be JSON"}), 400
    
    try:
        K = float(request.json.get('K'))
        I = float(request.json.get('I'))
        F = float(request.json.get('F'))
        S = float(request.json.get('S'))
        CR0 = float(request.json.get('CR0'))
        CD0 = float(request.json.get('CD0'))
    except (TypeError, ValueError) as e:
        return jsonify({"error": f"Invalid input data: {e}"}), 400
    # Placeholder values
    optimal_x = 12.34
    optimal_y = 56.78
    optimal_z = 90.12
    max_damage = 7500.50

    return jsonify({
        "optimal_x": optimal_x,
        "optimal_y": optimal_y,
        "optimal_z": optimal_z,
        "max_damage": max_damage
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000) # Run Flask on port 5000