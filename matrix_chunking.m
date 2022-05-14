function [i,j] = matrix_chunking(a,b)
i = zeros(1,a*b);
j = i;
for m = 1:1:(a*b)
    j(m) = mod(m,a);
    i(m) = floor((m-1)/a) + 1;
end

%task_id - 1 < m*(n/a*b) leq task_id