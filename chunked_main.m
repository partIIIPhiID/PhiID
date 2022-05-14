function chunked_main(task_id, electrodes, filename, filepath)
    for i = 2:1:size(electrodes, 2)
           if task_id < i
                main(electrodes(i), electrodes(task_id), filename, filepath)
           end
    end
end