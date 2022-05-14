%take 2 electrodes from the eeg array and compute phiID metrics
function main(electrode_a, electrode_b, filename, filepath)
    addpath ~/tools/eeglab; eeglab nogui;
    addpath ~/tools/fieldtrip; ft_defaults;
    data = loadfilename(sprintf('%s%s',filepath,filename));
    [prestim1, prestim2, poststim1, poststim2] = trim_data(electrode_a, electrode_b, data);
    for i = 1: +1: size(data, 3)
        atoms.pre1(i) = PhiIDFull(prestim1(:, :, i));
        atoms.pre2(i) = PhiIDFull(prestim2(:, :, i));
        atoms.post1(i) = PhiIDFull(poststim1(:, :, i));
        atoms.post2(i) = PhiIDFull(poststim2(:, :, i));
    end
    results_folder = '/rds/user/ae431/hpc-work/PhiID_results/';
    save(sprintf('%sdata_%d%d_%s.mat', results_folder, electrode_a, electrode_b, filename), 'atoms')
end