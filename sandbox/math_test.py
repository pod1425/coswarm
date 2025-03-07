import math

from swarm.graphing import MathExpression, get_graph_points

#expr = MathExpression("(x+1)^2")
#for i in range(-5, 5):
#    expr.set_variable("x", i)
#    result = expr.evaluate()
#    print(f"x={i},y={result}")

points = get_graph_points("abs(2*x)", -5, 5, 7)

for point in points:
    print(f"{point[0]},{point[1]};")