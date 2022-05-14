function performance_average(experiment)
    filepath = sprintf('/rds/project/tb419/rds-tb419-bekinschtein/Yanzhi/%s/', experiment);
    files = dir(sprintf('%s*', filepath));
    for i=1:length(files)
        if startsWith(files(i).name, 'Original') == 1
            files(i).performance = load(sprintf('%s%s', filepath, files(i).name), '-ascii');
            files(i).mean = mean(mod(files(i).performance(:,3),2));
        end
    end
   results_folder = '/rds/user/ae431/hpc-work/PhiID_results/';
   save(sprintf('%smeans_%s.mat', results_folder, experiment), 'files')
    
end