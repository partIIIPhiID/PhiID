%takes in a 92x5000xn matrix
%outputs four*n 2x1000 matrices, 2 pre and 2 post stimulus
function [prestim1, prestim2, poststim1, poststim2] = trim_data(electrode_a, electrode_b, data) 
    prestim1 = data([electrode_a, electrode_b], linspace(1,1000,1000), :);
    prestim2 = data([electrode_a, electrode_b], linspace(1001,2000,1000), :);
    poststim1 = data([electrode_a, electrode_b], linspace(3001,4000,1000), :);
    poststim2 = data([electrode_a, electrode_b], linspace(4001,5000,1000), :);
end