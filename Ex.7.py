def Ex_7():
    print("Ex_7 - ")
    print("In the given file, there is a function named main_processing_function, which, after being run multiple times, seems to cause slowdowns and memory issues.")
    print("Add @profile to the function main_processing_function and identify where the problem is.\n")
    print(f"By using @profile with the function, we can see the line:\n\
     - 797.5 MiB    765.7 MiB           1       heavy_result = calc_log_function() - \n\
     Which shows that 'calc_log_function()' required a high memory usage of 797.5 MiB...")
