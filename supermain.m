function supermain(electrodes, filename, filepath)
    for i = 2:1:size(electrodes, 2)
        for j = 1:1:(i - 1)
                main(electrodes(i), electrodes(j), filename, filepath)
        end
    end
end