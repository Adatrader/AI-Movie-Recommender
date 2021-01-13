# AI Movie Recommender System
## CS 4200
We developed a movie recommender system. The data used in this project was ratings gathered on MovieLens.org and distributed by GroupLens.org. We performed two different AI algorithms on this dataset to match a new user to movie recommendations. The two primary algorithms we used were Singular Value Decomposition and Gaussian Mixture. Here we will discuss our implementation and findings.  

### Group members:
* Adam VanRiper (S1)
* David Allison (S1)
* Minh Huynh (S2)
* Julieth Jaramillo (S2)

### Files:
* *Report*: CS4200 Final Report.pdf
* *Code*:
  * buildUI.py : Launches GUI, run this file and traverse the UI to select and rate some movies you've seen. This program will then run SVD and Gaussian Mixture on your prefeneces against the data set to yield a list of recommended movies.
  * gaussian.py : Contains implementation for Gaussian Mixture Method of recommending movies
  * svd.py : Contains implementation for SVD Method of recommending movies
  * compare.py : Warning: takes ~1 hour to run, generates graphs for final report
* *Dependencies*:
  * ```pip install wheel setuptools virtualenv kivy numpy requests pandas scikit-learn sklearn matplotlib```
* *Repo*: https://github.com/juliethjar/CS4200
* *Data*: final_dataset_3276.csv - This is the MovieLens (ml-latest-small.zip, found here: http://files.grouplens.org/datasets/movielens/ml-latest-small.zip) data with the MovieLensIDs replaced with the IMDB ids. This is the only dataset currently being used by buildUI.py and compare.py.
