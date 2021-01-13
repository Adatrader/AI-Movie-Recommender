# Filename: compare.py
# Authors: David Allison, Adam VanRiper
# Description: Performance comparison of SVD and Gaussian Mixture
# Tested on: py-3.8.6 && kivy-2.0.0rc4

import pandas as pd
from svd import SVD
from gaussian import Gaussian_Mixture
import time
import matplotlib.pyplot as plt


def create_datasets(filename, num_intervals):
    origin_df = pd.read_csv(filename)  # Open dataset
    origin_len = origin_df.columns.size  # df size
    interval = origin_len/num_intervals  # new df for each +10 movie
    new_len = int(interval)

    df_dict = {}  # dict of dataframes
    for i in range(num_intervals):
        if new_len > origin_len:
            df_dict['df_origin'] = origin_df
            break

        df_dict['df_' + str(new_len)] = origin_df.iloc[:, 1:new_len]
        new_len += int(interval)
    return df_dict

def duplicate_full_dataset(filename, length):
    origin_df = pd.read_csv(filename)  # Open dataset
    dataFrames = []  # dict of dataframes
    for i in range(length):
        dataFrames.append(origin_df)
    return dataFrames
    
def run_single_comparison(df_dict):
    X = []
    GM_Y = []
    SVD_Y = []

    for df in df_dict:
        X.append(df_dict[df].columns.size)
        
        gm_start = time.time()
        Gaussian_Mixture(df_dict[df])
        gm_time = time.time() - gm_start
        GM_Y.append(gm_time)
        #print("\nTime to run GM: on size ", df_dict[df].columns.size, ": ", gm_time, " seconds")

        svd_start = time.time()
        SVD(0,10,df_dict[df])
        svd_time = time.time() - svd_start
        SVD_Y.append(svd_time)
        #print("Time to run SVD on size ", df_dict[df].columns.size, ": ", svd_time, " seconds\n")

        print(df_dict[df].columns.size, " calculated.")
        
    return X, GM_Y, SVD_Y

def run_multi_comparison(dataFrames):
    interval = int(40/(len(dataFrames) - 1))
    X = []
    GM_Y = []
    SVD_Y = []
    GM_time = 0
    for i in range(len(dataFrames)):
        if i == 0:
            GM_start = time.time()
            Gaussian_Mixture(dataFrames[i])
            GM_time = time.time() - GM_start
        else:
            GM_Y.append(GM_time)
            X.append(i * interval)
            SVD_start = time.time()

            for j in range(i * interval):
                SVD(j,10,dataFrames[i])
                
            SVD_time = time.time() - SVD_start
            SVD_Y.append(SVD_time)
        print(i * interval, " calculated.")

    return X, GM_Y, SVD_Y

# -------------------------------------------------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------------------------------------------------
start = time.time()
full_file = "data/final_datasets_LARGE.csv"

# Uncomment to plot GM vs SVD at varying numbers of  on varying dataset sizes from 0 to 3276
# -------------------------------------------------------------------------------------------
dataframes = duplicate_full_dataset(full_file, 11) # 1 for GM, the rest for SVD
X, GM_Y, SVD_Y = run_multi_comparison(dataframes)
fig, ax = plt.subplots()
ax.plot(X,GM_Y)
ax.plot(X,SVD_Y)
ax.set(xlabel = 'Number of movies rated (n)', ylabel='Execution time (sec)',
       title='SVD vs Gaussian Mixture with Different Numbers of Movie Ratings')
ax.legend(["Gaussian Mixture", "SVD"], loc='upper left')
fig.savefig("full_dataset_performance.png")
fig.show()
# -------------------------------------------------------------------------------------------

# Uncomment to plot SVD vs GM on varying dataset sizes from 0 to 3276
# -------------------------------------------------------------------------------------------
datasets = create_datasets(full_file, 10)
X, GM_Y, SVD_Y = run_single_comparison(datasets)
fig2, ax2 = plt.subplots()
ax2.plot(X,GM_Y)
ax2.plot(X,SVD_Y)
ax2.set(xlabel = 'Length of data set (n)', ylabel='Execution time (sec)',
       title='SVD vs Gaussian Mixture Efficiency')
ax2.legend(["Gaussian Mixture", "SVD"], loc='upper left')
fig2.savefig("multi_dataset_performance.png")
fig2.show()
# -------------------------------------------------------------------------------------------

print("Total runtime: ", (time.time()-start)/60, " minutes.")
