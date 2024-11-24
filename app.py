from flask import Flask, render_template, request, jsonify
from pulp import LpProblem, LpMinimize, LpVariable, lpSum

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/calculate', methods=['POST'])
def calculate_nutrients():
    data = request.json
    age = int(data['age'])  # Convert age to an integer
    weight = float(data['weight'])  # Convert weight to a float
    state = data['state']
    
    daily_nutrients = calculate_daily_nutrients(age, weight, state)
    cost = calculate_minimum_cost(daily_nutrients)
    
    return jsonify({'daily_nutrients': daily_nutrients, 'minimum_cost': cost})

def calculate_daily_nutrients(age, weight, state):
    # Example nutrient calculation logic
    # This should be replaced with actual logic based on age, weight, and state
    protein = 0
    fiber = 0
    
    if state == "young":
        protein = weight * 1.5
        fiber = weight * 0.015
    elif state == "adult":
        protein = weight * 0.08
        fiber = weight * 0.04
    elif state == "pregnant":
        protein = weight * 0.12
        fiber = weight * 0.06
    
    return {'protein': protein, 'fiber': fiber}

def calculate_minimum_cost(nutrients):
    # Example cost calculation logic using PuLP
    # This should be replaced with actual feed data and cost
    protein_cost = 2.0  # Cost per unit of protein
    fiber_cost = 1.5    # Cost per unit of fiber
    
    # Create a linear programming problem
    prob = LpProblem("Minimize_Cost", LpMinimize)
    
    # Variables
    protein_amount = LpVariable('protein_amount', lowBound=0)
    fiber_amount = LpVariable('fiber_amount', lowBound=0)
    
    # Objective function
    prob += protein_cost * protein_amount + fiber_cost * fiber_amount
    
    # Constraints
    prob += protein_amount >= nutrients['protein']
    prob += fiber_amount >= nutrients['fiber']
    
    # Solve the problem
    prob.solve()
    
    return prob.objective.value()

if __name__ == '__main__':
    app.run(debug=True)