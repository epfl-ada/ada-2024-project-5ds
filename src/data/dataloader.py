import pandas as pd
import os
import ast
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from utils.csv import save_dataframe_to_csv

def load_initial_dataset(PATH_IN) :

    fname = os.path.join(PATH_IN, 'movie.metadata.tsv')
    movie = pd.read_csv(fname, delimiter='\t', header=None)
    movie.columns = ['Wikipedia movie ID', 'Freebase movie ID', 'Movie name', 'Movie release date', 'Movie box office revenue', 'Movie runtime', 'Movie languages (Freebase ID:name tuples)', 'Movie countries (Freebase ID:name tuples)', 'Movie genres (Freebase ID:name tuples)']

    fname = os.path.join(PATH_IN, 'character.metadata.tsv')
    character = pd.read_csv(fname, delimiter='\t', header=None)
    character.columns = ['Wikipedia movie ID', 'Freebase movie ID', 'Movie release date', 'Character name', 'Actor date of birth', ' Actor gender', 'Actor height (in meters)', 'Actor ethnicity (Freebase ID)', 'Actor name',
                        'Actor age at movie release', 'Freebase character/actor map ID', 'Freebase character ID', 'Freebase actor ID']

    fname = os.path.join(PATH_IN, 'plot_summaries.txt')
    plot_summaries = pd.read_csv(fname, delimiter='\t', header=None)
    plot_summaries.columns = ['Wikipedia movie ID', 'Summary']


    fname = os.path.join(PATH_IN, 'tvtropes.clusters.txt')
    tvtropes = pd.read_csv(fname, delimiter='\t', header=None, names = ['Trope','StringDict'])


    tvtropes['Dictionnary'] = tvtropes['StringDict'].apply(ast.literal_eval)
    df = pd.json_normalize(tvtropes['Dictionnary'])
    tvtropes['Character Name'] = df['char']
    tvtropes['Movie name'] = df['movie']
    tvtropes['Freebase movie ID'] = df['id']
    tvtropes['Actor name'] = df['actor']
    tvtropes = tvtropes.drop(tvtropes.columns[1], axis=1)
    tvtropes = tvtropes.drop(tvtropes.columns[1], axis=1)



    fname = os.path.join(PATH_IN, 'name.clusters.txt')
    name_clusters = pd.read_csv(fname, delimiter='\t', header=None, names = ['Character Name','ID'])

    return  movie, character, plot_summaries,  tvtropes, name_clusters

def load_oscar_winning_films(OS = 'WINDOWS') :
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Cinematography"
    df = search_golden_names(url,OS)
    save_dataframe_to_csv(df, "oscar_winning_films")

def load_oscar_winning_actors(OS = 'WINDOWS') :
    
    if OS == 'MAC' :
        driver = webdriver.Chrome()
    else :
        service = Service('C:\webdrivers\chromedriver.exe')
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service = service, options = options)

    names_list = []
   
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor"
    driver.get(url)

    # Adding a wait to ensure all content is loaded
    time.sleep(5)

    # Find all 'tr' tags in the table to extract year, movie, and symbol information
    tr_tags = driver.find_elements(By.TAG_NAME, 'tr')

    # Iterate over each 'tr' tag to find the required information
    for tr_tag in tr_tags:
        # Extract 'td' elements from the row
        td_tags = tr_tag.find_elements(By.TAG_NAME, 'td')

        if len(td_tags) > 0:
            # Extract the text content and background color from each 'td' tag
            for td_tag in td_tags:
                text = td_tag.text.strip()
                style = td_tag.get_attribute('style')

                # Check for specific symbols in the text and categorize them
                if '‡' in text:
                    cleaned_text = text.replace('‡', '').strip()
                    first_two_words = ' '.join(cleaned_text.split()[:2])
                    names_list.append(first_two_words)
                #Refused oscar
                elif '§' in text:
                    cleaned_text = text.replace('§', '').strip()
                
                #Posthume oscar
                elif '†' in text:
                    cleaned_text = text.replace('†', '').strip()
                
    driver.quit()
    df = pd.DataFrame(names_list, columns=['actors'])
    save_dataframe_to_csv(df, 'oscar_winning_actors')
   

def search_golden_names(url, OS) :
    if OS == 'MAC' :
        driver = webdriver.Chrome()
    else :
        service = Service('C:\webdrivers\chromedriver.exe')
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service = service, options = options)

    driver.get(url)
    movie_names = []
    time.sleep(5)

    tr_tags = driver.find_elements(By.TAG_NAME, 'tr')

    for tr_tag in tr_tags:
        style = tr_tag.get_attribute('style')
        
        
        if 'rgb(250, 235, 134)' in style:  
        
            td_tags = tr_tag.find_elements(By.TAG_NAME, 'td')
            
            if len(td_tags) > 1:
                name = td_tags[0].text.strip()
                movie_names.append(name)
                movie_info = td_tags[1].text.strip()


    driver.quit()
    movies_oscar_winning = pd.DataFrame(movie_names, columns=['Movie name'])

    return movies_oscar_winning