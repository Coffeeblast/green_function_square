# green_function_square

This script visualizes approximation to the Green function of Laplacian on square, 

(partial^2_x + partial^2_y) G (x, y) = delta(x - x0)delta(y - y0)
where G(0, y) = G(1, y) = G(x, 0) = G(x, 1) = 0
for 0 < x0 < 1, 0 < y0 < 0

By the Fourier method the solution can be approximated as 
G(x, y) = lim_{n --> infty} sum_{i = 1} ^ n sum_{j = 1} ^ n (4 / lambda_ij) * sin(alpha_i x0) * sin(alpha_i x) * sin(beta_j y0) * sin(beta_j y)
where alpha_i = i * pi, beta_j = j * pi and lambda_ij = -(alpha_i^2 + beta_j^2)

Visualisation allows one to see how the function changes for various n, and for various values of the singularity position (x0, y0). 
