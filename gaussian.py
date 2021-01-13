# Filename: gaussian.py
# Authors: Julieth Jaramillo
# Description: Gaussian Mixture implementation for movie recommendations
# Tested on: py-3.8.6 && kivy-2.0.0rc4

import pandas as pd
from collections import Counter
from sklearn.mixture import GaussianMixture

# Gaussian Mixture method of getting movie recommendations
def Gaussian_Mixture(data):
    gm = GaussianMixture(n_components=16)
    
    #add the new user ratings to the end of the dataframe containing user ratings per movie
    gm.fit(data)
    #Get the predicted user group/cluster
    labels = gm.predict(data)
    new_data = pd.DataFrame(data)
    #add the groups to the dataframe
    new_data['cluster'] = labels
    #get group classification obtained by using gaussian mixture
    group =int(new_data.iloc[-1]['cluster'])
    
    #print(group)
    
    return get_recommendations(new_data,group)

# Utility function to return a list of movieIDs liked by a group of users
def get_recommendations(data,group):
    
    recommendations=[]
    #get_likes returns list of movies liked per user
    user_likes=get_likes(data)
    
    #Get ratings of all users in a specific group
    group_ratings=data.loc[data['cluster'] == group]
    count_u =0
    for key in group_ratings:
        
        if key !='cluster' :
            #get ratings of group members
            rate=group_ratings[key]
            
            likes= []
            for user,rating in rate.iteritems():
                u_likes=user_likes[user]
                likes.extend(u_likes)
                #stop at 20 users
                if count_u ==20:
                    #Get the 10 most common movies amoung the group
                    recommendations=[movie for movie, count in Counter(likes).most_common(15)]
                    return recommendations
                
                count_u+=1
        break
    
    return recommendations

def get_likes(data):
    u_likes={}
    #initialize an empty movies_liked list for all users
    for i in range(0,610):
        u_likes[i]=[]
    #Go through each user ratings and get list of all movies rated higher than 4 for each user
    for key in data:
        rate=data[key]
        
        for user,rating in rate.iteritems():
            #add movies liked by user to the user's movies liked list
            if float(rating)>=4:
                c= u_likes[int(user)]
                c.append(key)
                u_likes[int(user)]=c
    return u_likes
