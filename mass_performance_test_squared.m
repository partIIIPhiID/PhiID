function mass_performance_test_squared(task_id, electrodes, filename, filepath, performance_path, performance_name)
    zzz_array = ['rtr', 'rtx', 'rty', 'rts', 'xtr', 'xty', 'xts', 'ytr', 'ytx', 'yty', 'yts', 'str', 'stx', 'sty', 'sts'];
    chunk_array = ['pre1', 'pre2', 'post1', 'post2'];
    for q = 1:1:16
        for w = 1:1:4
            mass_performance_test(task_id, electrodes, filename, filepath, performance_path, performance_name, zzz_array(q), chunk_array(w))
        end
    end
end