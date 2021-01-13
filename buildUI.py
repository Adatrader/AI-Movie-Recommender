# Filename: buildUI.py
# Authors: David Allison, Minh Huynh, Julieth Jaramillo, Adam VanRiper
# Description: AI Movie Recommender System UI
# Tested on: py-3.8.6 && kivy-2.0.0rc4

# Utility Dependencies:
import requests
import json
import csv
import random
from collections import Counter
import time

# UI Dependencies:
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.image import Image, AsyncImage
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.image import Image, AsyncImage
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.uix.dropdown import DropDown

# Data Analysis Dependencies:
from svd import SVD
from gaussian import Gaussian_Mixture
from gaussian import get_likes
import pandas as pd

# -------------------------------------------------------------------------------------------
# PROGRAM PARAMETERS
# -------------------------------------------------------------------------------------------

USE_FULL_DATASET = False

if USE_FULL_DATASET:
    dataFile = "data/final_datasets_LARGE.csv"
    genreFile = "data/genre_imdbId_LARGE.csv"
else:
    dataFile = "data/final_datasets_SMALL.csv"
    genreFile = "data/genre_imdbId_SMALL.csv"

data = pd.read_csv(dataFile,sep=',')

# -------------------------------------------------------------------------------------------
# KIVY BUILDER
# -------------------------------------------------------------------------------------------

# kv multipage layout
Builder.load_string("""
<HomeWindow>:
    name: "home"
    
    BoxLayout:
        orientation: 'vertical'
        padding: 60
        Label:
            text: 'Find A Movie To Watch'
            color: '72add4'
            font_size: 40
            size_hint_y: .6
            font_name: 'Roboto-Bold'
        Label:
            text: 'Pick 1-3 Genres You Like'
            color: '72add4'
            font_size: 20
            size_hint_y: .2
            font_name: 'Roboto-Bold'
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: '        Action'
            CheckBox:
                name: 'Action'
                on_active: root.checkbox_click(self, self.active)
            Label:
                text: '        Comedy'
            CheckBox:
                name: 'Comedy'
                on_active: root.checkbox_click(self, self.active)
            Label:
                text: '        Romance'
            CheckBox:
                name: 'Romance'
                on_active: root.checkbox_click(self, self.active)
            Label:
                text: '        Adventure'
            CheckBox:
                name: 'Adventure'
                on_active: root.checkbox_click(self, self.active)
            Label:
                text: '        Documentary'
            CheckBox:
                name: 'Documentary'
                on_active: root.checkbox_click(self, self.active)
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: '        Thriller'
            CheckBox:
                name: 'Thriller'
                on_active: root.checkbox_click(self, self.active)
            Label:
                text: '        Mystery'
            CheckBox:
                name: 'Mystery'
                on_active: root.checkbox_click(self, self.active)
            Label:
                text: '        Animation'
            CheckBox:
                name: 'Animation'
                on_active: root.checkbox_click(self, self.active)
            Label:
                text: '        Children'
            CheckBox:
                name: 'Children'
                on_active: root.checkbox_click(self, self.active)
            Label:
                text: '        Drama'
            CheckBox:
                name: 'Drama'
                on_active: root.checkbox_click(self, self.active)
        BoxLayout:
            orientation: 'horizontal'
            Label:
                text: '        Horror'
            CheckBox:
                name: 'Horror'
                on_active: root.checkbox_click(self, self.active)
            Label:
                text: '        Western'
            CheckBox:
                name: 'Western'
                on_active: root.checkbox_click(self, self.active)
            Label:
                text: '        War'
            CheckBox:
                name: 'War'
                on_active: root.checkbox_click(self, self.active)
            Label:
                text: '        Crime'
            CheckBox:
                name: 'Crime'
                on_active: root.checkbox_click(self, self.active)
            Label:
                text: '        Sci-Fi'
            CheckBox:
                name: 'Sci-Fi'
                on_active: root.checkbox_click(self, self.active)
        Button:
            text: "Next"
            pos_hint: {'center_x': 0.5}
            size_hint: 0.2, 0.3
            on_release: app.root.current = "second" if root.confirmRange() == True else "home"
        
<TopMoviesWindow>:
    name: "second"
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Have you seen these titles?'
            font_size: 20
            size_hint_y: .1
            color: '72add4'
            font_name: 'Roboto-Bold'
        Label:
            text: 'Select movies to rate'
            font_size: 15
            size_hint_y: .1
            color: '72add4'
            font_name: 'Roboto-Bold'
        Label:
            text: " "
            font_size: 3
    ScrollView:
  
        pos_hint: {'top':.90}      
        do_scroll_y: True
        height: 647500
        FloatLayout:
            size_hint_y: None
            height: 1310
            GridLayout:
                size_hint_y: None
                height: 1310
                id: movies         
                cols: 5
                
    Label:
        text: "       "
        font_size: 250        
    BoxLayout:
        orientation: 'horizontal'
        pos_hint: {'bottom':.98}
        
        Button:
            text: "Back"
            spacing: 10
            pos_hint: {0.1: 0.5}
            size_hint: 0.1, 0.1
            on_release: 
                app.root.current = "home"
                root.manager.transition.direction = "right"
        Button:
            text: "Next"
            spacing: 10
            pos_hint: {0.1: 0.5}
            size_hint: 0.1, 0.1
            on_release: app.root.current = "third"
<RateTitlesWindow>:
    name: "third"
    BoxLayout:
        pos_hint: {'top':.98} 
        orientation: 'vertical'
        padding: 10,10
        Label:
            text: 'Rate these Titles'
            font_size: 40
            size_hint_y: .6
            color: '72add4'
            font_name: 'Roboto-Bold'
        Label:
            text: 'From 1 to 5 (5 being the best)'
            font_size: 20
            size_hint_y: .2
            color: '72add4'
            font_name: 'Roboto-Bold'
        Label:
            text: " "
            font_size: 3
    ScrollView:
  
        pos_hint: {'top':.55}      
        do_scroll_y: True
        height: 647500
        FloatLayout:
            size_hint_y: None
            height: 1310
            GridLayout:
                
                id: moviesP
                cols: 5
                row_force_default:True
                row_default_height:350
    Label:
        text: "       "
        font_size: 450  
    BoxLayout:
    
        pos_hint: {'bottom':.98} 
        orientation: 'vertical'
          
        Label:
            text: "Get Your Recommendations (Choose which method):"
            font_size: 20
        BoxLayout:
            orientation: 'horizontal'
            Button:
                text: "Back"
                
                pos_hint: {0.1: 0.5}
                size_hint: 0.1, 0.1
                on_release: 
                    app.root.current = "second"
                    root.manager.transition.direction = "right"
            Button:
                text: "Gaussian Mixture"
                spacing: 10
                pos_hint: {0.1: 0.5}
                size_hint: 0.1, 0.1
                on_release: app.root.current = "finalGaus"
            Button:
                text: "SVD"
                spacing: 10
                pos_hint: {0.1: 0.5}
                size_hint: 0.1, 0.1
                on_release: app.root.current = "finalSVD"
<RecommendedWindowGaus>:
    name: "finalGaus"
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: 50,50
            
    BoxLayout:
        orientation: 'horizontal'
        pos_hint: {'bottom':.98}
        Label:
            text: "       "
            font_size: 250    
        Button:
            text: "Back"
            spacing: 10
            pos_hint: {0.1: 0.5}
            size_hint: 0.1, 0.1
            on_release: app.root.current = "third"
        
<RecommendedWindowSVD>:
    name: "finalSVD"
    ScrollView:
        BoxLayout:
            orientation: 'vertical'
            padding: 50,50
    BoxLayout:

        
        orientation: 'horizontal'
        pos_hint: {'bottom':.98}
        Label:
            text: "       "
            font_size: 250   
        Button:
            text: "Back"
            spacing: 10
            pos_hint: {0.1: 0.5}
            size_hint: 0.1, 0.1
            on_release: app.root.current = "third"     
""")

# -------------------------------------------------------------------------------------------
# KIVY UI CLASSES
# -------------------------------------------------------------------------------------------

class MainApp(App):  # Kivy Window
    def build(self):
        
        Window.size = (1300, 800)
        # Window.AliasProperty(center=True)
        # Create screen manager
        sm = ScreenManager()
        sm.add_widget(HomeWindow(name='home'))
        sm.add_widget(TopMoviesWindow(name='second'))
        sm.add_widget(RateTitlesWindow(name='third'))
        sm.add_widget(RecommendedWindowGaus(name='finalGaus'))
        sm.add_widget(RecommendedWindowSVD(name='finalSVD'))
        
        return sm


class HomeWindow(Screen):  # Homepage with genre selection
    # Callback for the checkbox
    sm = ScreenManager()
    def checkbox_click(self, instance, value):
        if value:
            getMoviesPageHelper(instance.name, True)
            #print("Checkbox Checked")
        else:
            getMoviesPageHelper(instance.name, False)
            #print("Checkbox Unchecked")

    def confirmRange(self):
        # Pop up if entry not 1-3 genres selected
        if (len(genreArr) > 3 or len(genreArr) < 1):
            popup = Popup(title='Invalid Entry',
                          content=Label(
                              text='Please select 1-3 genres', font_size=25),
                          size_hint=(None, None), size=(400, 400))
            popup.open()
        else:
            # Filter list of movies to serve on 2nd page
            filterGenres()
            return True
    

class TopMoviesWindow(Screen):  # 2nd window "Have you seen these titles?"
    visited_2=0
    def on_enter(self):
        if self.visited_2 ==0:
            self.visited_2=1
            layoutPT = GridLayout(cols=5, row_force_default=True, row_default_height=350)
            
            for mov in moviesPageTwo:
                result = getJson(mov)
                if 'Poster' in result:
                    # add poster image link to the page layout to display
                    poster = result['Poster']
                    title = result['Title']
                    exportPageTwo.update({title: mov})
                    moviecard =BoxLayout(orientation='vertical')
                    moviecard.add_widget(AsyncImage(source=str(poster)))
                    
                    moviecard.add_widget(Button(text=title,size_hint=(1, None), height=20,on_press=self.buttonPressed))
                    layoutPT.add_widget(moviecard)    
            self.ids.movies.add_widget(layoutPT)
    def buttonPressed(self, instance):
        watchedMovies.update({exportPageTwo.get(instance.text): 0})
    

class RateTitlesWindow(Screen):  # 3rd window "Rate these titles"
    visited_3=0
    def on_enter(self):
        if self.visited_3 ==0:
            self.visited_3=1
            
            for mov in watchedMovies:
                result = getJson(mov)
                if 'Poster' in result:
                    # add poster image link to the page layout to display
                    poster = result['Poster']
                    title = result['Title']
                    star_row= BoxLayout(orientation='horizontal',size_hint=(1, None),height=10 )
                    layoutrm = GridLayout(cols=1)
                    layoutrm.add_widget(AsyncImage(source=str(poster)))
                    #self.ids.moviesPageThree.add_widget(AsyncImage(source=str(poster)))
                    starButton = [mov + '_1', mov + '_2',
                                mov + '_3', mov + '_4', mov + '_5']
                    layoutrm.add_widget(
                        Label(text=title, font_size=18, size_hint=(1, None)))            
                    #self.ids.moviesLabelPageThree.add_widget(
                     #   Label(text=title, font_size=30))
                    # Star Buttons
                    star_row.add_widget(Label(text=" ", font_size=30))
                    #self.ids.moviesTwoPageThree.add_widget(Label(text=" ", font_size=30))
                    for imdbId in starButton:
                        btn = Button(background_normal='img/star_empty.png',
                                    background_down='img/star_full.png', size=(50, 50), size_hint=(None, None),
                                    on_press=self.ratedValue)
                        # unable to assign id attribute to button so used custom attribute
                        btn.id_created = imdbId
                        star_row.add_widget(btn)
                        #self.ids.moviesTwoPageThree.add_widget(btn)
                    star_row.add_widget(Label(text=" ", font_size=30))
                    #self.ids.moviesTwoPageThree.add_widget(
                     #   Label(text=" ", font_size=30))
                    layoutrm.add_widget(star_row)
                    self.ids.moviesP.add_widget(layoutrm)
            
    def ratedValue(self, instance):
        list = self.ids.moviesP.children
        c_list = []
        for e in list:
            list2 = e.children
            for c in list2:
                list3=c.children
                for cc in list3:
                    c_list.append(cc)
        #print(c_list)
        
        tempDict = {}
        for x in c_list:
            try:
                tempDict.update({x.id_created: x})
            except:
                continue
        if int(instance.id_created[-1:]) > 1:
            count = int(instance.id_created[-1:])
            while count > 0:
                curId = str(instance.id_created[:-1]) + str(count)
                temp = tempDict.get(curId)
                temp.background_normal = 'img/star_full.png'
                count -= 1
        instance.background_normal = 'img/star_full.png'
        newId = instance.id_created[:-2]
        # Export movie ratings to watchMovies for recommended pages
        initializeRatings.update({newId: instance.id_created[-1:]})


# Final window showing recommendations Gaussian
class RecommendedWindowGaus(Screen):
    def on_enter(self):
        
        global visited_p1,visited_p2
        visited_p1=1
        if visited_p2==0:
            for x in initializeRatings:
                userRatings.append(float(initializeRatings.get(x)))
            data.iloc[-1] = userRatings
        start = time.time()
        group_gm = Gaussian_Mixture(data)
        print("Time to calculate Gaussian Mixture: ", time.time() - start, " seconds.")
        
        #Setup page to display movie recommendations
        layout = GridLayout(cols=4)
        new_layout= getlayout(layout,group_gm,'Gaussian Mixture')
   
        self.add_widget(new_layout)


class RecommendedWindowSVD(Screen):  # Final window showing recommendations SVD
    def on_enter(self):
        # Update user ratings
        global visited_p1,visited_p2
        visited_p2=1
        if visited_p1==0:
            for x in initializeRatings:
                userRatings.append(float(initializeRatings.get(x)))
            data.iloc[-1] = userRatings
        user_likes =get_likes(data)
        last_user = list(user_likes.keys())[-1]
        u_likes=user_likes[last_user]
        m_likes = []
        recommendations_l = []
        
        count = 0
        for m in u_likes:
            # stop at 10 movies
            if count ==10:
                break
            # find the  movie index number
            m_index = data.columns.get_loc(m) 
            print(m_index)
            start = time.time()
            similar_movies = SVD(m_index, 10, data)
            print("Time to calculate SVD: ", time.time() - start, " seconds.")
            
            m_likes.extend(similar_movies)
            #print(m_likes)
            count+=1
        recommendations_l=[movie for movie, count in Counter(m_likes).most_common(15)]

        #return page layout to display
        layout = GridLayout(cols=4)    
        new_layout= getlayout(layout,recommendations_l,'SVD')
        self.add_widget(new_layout)
     
# -------------------------------------------------------------------------------------------
# LAYOUT CREATOR AND HELPER DATA 
# -------------------------------------------------------------------------------------------

# User Data Passed Between Windows
genreArr = []  # Store genres
moviesPageTwo = []  # Generated top rated movies from each genre selected
exportPageTwo = {}  # temp dict, issue with passing state from page two
watchedMovies = {}  # for page 3, imdb id : rating
initializeRatings = {}
userRatings = []  # Here is the generated user ratings for recommended pages
visited_p1=0
visited_p2=0

def getlayout(layout,recommendations, method):
    layout.add_widget(Label(text ="Movie Recommendations "+method) )
    
    ombdURL ="http://www.omdbapi.com/?apikey=98016917&"
    dbSession = requests.Session()
    dbSession.verify = False
    #Go trough the user's recommendation and display poster for the movie
    for imdbID in recommendations:
        movieRequest = dbSession.get(ombdURL + 'i='+imdbID)
        #save api query result into result
        result = movieRequest.json()
        #check if api returns a poster for the movie
        if 'Poster' in result:
            #add poster image link to the page layout to display
            poster =movieRequest.json()['Poster']
            layout.add_widget(AsyncImage(source=str(poster)))
    return layout

# -------------------------------------------------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------------------------------------------------

def getMoviesPageHelper(name, action):  # Helper for checkbox selections on page one
    if(action):
        genreArr.append(name)
        #print(genreArr)
    else:
        genreArr.remove(name)
        #print(genreArr)

def filterGenres():  # Generate top nine movies from selected genres
    genre_movies = []
    filtered_list = []
    average_score = {}
    with open(genreFile, 'r') as data:
        for line in csv.DictReader(data):
            # for recommended page
            initializeRatings.update({line.get('movieId'): -1})
            genre_movies.append(line)
    # Check if user selected genres are contained in dataset
    for next in genre_movies:
        for x in genreArr:
            if x in next.get('genres'):
                filtered_list.append(next)

    # Create dictionary of imdbId : average score
    for filt in filtered_list:
        average_score.update({filt.get('movieId'): filt.get('average')})

    # Get top 9 rated movies (can update to 18-36 for additional rounds
    # if user hasn't watch any)
    topNine = Counter(average_score)
    topNine.most_common()
    for k, v in topNine.most_common(15):
        moviesPageTwo.append(k)
    #print(moviesPageTwo)

def getJson(movId):  # Imdb Json API request
    ombdURL = "http://www.omdbapi.com/?apikey=98016917&"
    dbSession = requests.Session()
    dbSession.verify = False
    movieRequest = dbSession.get(ombdURL + 'i='+movId)
    result = movieRequest.json()
    return result

# -------------------------------------------------------------------------------------------
# RUN PROGRAM
# -------------------------------------------------------------------------------------------
if __name__ == "__main__":
    MainApp().run()  # Run Kivy
