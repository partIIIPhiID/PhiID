function mat_to_csv_analysis(filename, filepath, savename, savepath,dataset_number)
    FileData = load(sprintf('%s%s.mat', filepath, filename));
    analysis_table = newdataset(FileData.dataset, dataset_number)
    writetable(struct2table(analysis_table), sprintf('%s%s.csv', savepath, savename));
end