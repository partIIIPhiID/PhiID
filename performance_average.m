function performance_average(filepath)
    files = dir(sprintf('%s*.txt', filepath));
    for i=1:length(files)
        if startsWith(files(i), 'Original') == 1
            files(i).performance = load(files(i).name, '-ascii');
            files(i).mean = mean(files(i).performance);
        end
    end
   results_folder = '/rds/user/ae431/hpc-work/PhiID_results/';
   save(sprintf('%smeans_%s.mat', results_folder, filepath), 'files')
    
end