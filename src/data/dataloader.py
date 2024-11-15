import pandas as pd
import os
import sys
import ast
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import wikipediaapi
from bs4 import BeautifulSoup
import requests
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON, CSV



user_agent = "Mus/1.0"
wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='en')
sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent=user_agent)
import sys
sys.path.append('/Users/williamjallot/Desktop/ADA/ada-2024-project-5ds/src/utils')
sys.path.append('/Users/williamjallot/Desktop/ADA/ada-2024-project-5ds/src/data')
from data_utils import save_dataframe_to_csv, load_dataframe_from_csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from extend_dataset import get_actor_information


def load_initial_dataset(PATH_IN) :
    """
    Load the CMU dataset
    Params :
        PATH_IN : The file where are located the CMU data
    Return :
        movie : A panda dataframe containing movies with the following columns : 'Wikipedia movie ID', 'Freebase movie ID',
                'Movie name', 'Movie release date', 'Movie box office revenue', 'Movie runtime', 'Movie languages',
                'Movie countries', 'Movie genres'
        character : A panda dataframe containing movie characters with the following columns : 'Wikipedia movie ID', 'Freebase movie ID', 'Movie release date', 'Character name', 'Actor date of birth', ' Actor gender', 'Actor height)', 'Actor ethnicity', 'Actor name',
                        'Actor age at movie release', 'Freebase character', 'Freebase character ID', 'Freebase actor ID'
        plot summaries : A panda dataframe containing movie plot summaries containing the following columns : 'Wikipedia movie ID', 'Summary'

        tv tropes : A panda dataframe containing tv tropes with the following columns : 'Trope', 'Character Name', 'Movie name', 'Freebase movie ID', 'Actor name'

        name clusters : A panda dataframe containing characters names from film with the freebase ID with the following columns : 'Character Name', 'ID'
    """
    #Load the movie dataframe
    fname = os.path.join(PATH_IN, 'movie.metadata.tsv')
    movie = pd.read_csv(fname, delimiter='\t', header=None)
    movie.columns = ['Wikipedia movie ID', 'Freebase movie ID', 'Movie name', 'Movie release date', 'Movie box office revenue', 'Movie runtime', 'Movie languages', 'Movie countries', 'Movie genres']

    #load the character dataframe
    fname = os.path.join(PATH_IN, 'character.metadata.tsv')
    character = pd.read_csv(fname, delimiter='\t', header=None)
    character.columns = ['Wikipedia movie ID', 'Freebase movie ID', 'Movie release date', 'Character name', 'Actor date of birth', ' Actor gender', 'Actor height)', 'Actor ethnicity', 'Actor name',
                        'Actor age at movie release', 'Freebase character', 'Freebase character ID', 'Freebase actor ID']
    
    ethnicities = character['Actor ethnicity'].values.tolist()

    ethnicities = set(ethnicities)
    freebase_ids_to_labels = {}

    for ethnicity in ethnicities:
        results = get_ethnicity_info(ethnicity)
        for result in results:
            freebase_id = ethnicity
            label = result['itemLabel']['value']
            freebase_ids_to_labels[freebase_id] = label
            
    character['Actor ethnicity'] = character['Actor ethnicity'].map(freebase_ids_to_labels)


    #Load the plot summary data frame
    fname = os.path.join(PATH_IN, 'plot_summaries.txt')
    plot_summaries = pd.read_csv(fname, delimiter='\t', header=None)
    plot_summaries.columns = ['Wikipedia movie ID', 'Summary']

    #Load the tv tropes dataframe
    fname = os.path.join(PATH_IN, 'tvtropes.clusters.txt')
    tvtropes = pd.read_csv(fname, delimiter='\t', header=None, names = ['Trope','StringDict'])

    tvtropes['Dictionnary'] = tvtropes['StringDict'].apply(ast.literal_eval)
    df = pd.json_normalize(tvtropes['Dictionnary'])
    tvtropes['Character Name'] = df['char']
    tvtropes['Movie name'] = df['movie']
    tvtropes['Freebase movie ID'] = df['id']
    tvtropes['Actor name'] = df['actor']
    #Drop the duplicated columns 
    tvtropes = tvtropes.drop(tvtropes.columns[1], axis=1)
    tvtropes = tvtropes.drop(tvtropes.columns[1], axis=1)

    #Load the name_cluster datframe
    fname = os.path.join(PATH_IN, 'name.clusters.txt')
    name_clusters = pd.read_csv(fname, delimiter='\t', header=None, names = ['Character Name','ID'])

    save_dataframe_to_csv(movie, 'movie_cmu.csv')
    save_dataframe_to_csv(character, 'character.csv')
    save_dataframe_to_csv(plot_summaries, 'plot_summaries.csv')
    save_dataframe_to_csv(tvtropes, 'tvtropes.csv')
    save_dataframe_to_csv(name_clusters, 'name_clusters.csv')



def load_oscar_winning_films_ids(OS = 'WINDOWS') :
    """
    Search all the films that won an oscar and save it with the wikidata id in the cleaned_data directory
    Params :
        OS : The opearting system you are own, default Windows
    """
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture"
    page_ids = search_winning_films_ids(url,OS)
    df= pd.DataFrame(page_ids, columns=['Page ID'])
    save_dataframe_to_csv(df, "oscar_winning_films_ids.csv")

def load_oscar_winning_actors(OS='WINDOWS'):
    """
    Search all the actors that won an Oscar and save the actor along with the Wikipedia film ID and the actor ID in the cleane_data directory.
    
    Params:
        OS: The operating system you are on, default is Windows.
    """
    # Get actor and film data
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor"
    page_ids = search_actors_and_films(url, OS)
    # Construct the DataFrame
    rows = []
    for actor_id, film_ids in page_ids.items():
        for film_id in film_ids:
            rows.append((actor_id, film_id))
    
    df = pd.DataFrame(rows, columns=['Actors id', 'film_id'])
    save_dataframe_to_csv(df, 'oscar_winning_actors.csv')
    


def load_oscar_winning_actresses(OS = 'WINDOWS') :
    """
    Search all the actresses that won an Oscar and save the actress along with the Wikipedia film ID and the actor ID in the cleane_data directory.
    
    Params:
        OS: The operating system you are on, default is Windows.
    """
    # Get actress and film data
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress"
    page_ids = search_actors_and_films(url, OS)
    # Construct the DataFrame
    rows = []
    for actor_id, film_ids in page_ids.items():
        for film_id in film_ids:
            rows.append((actor_id, film_id))
    
    df = pd.DataFrame(rows, columns=['Actress id', 'film_id'])
    save_dataframe_to_csv(df, 'oscar_winning_actresses.csv')

def load_oscar_winning_supporting_actors(OS = 'WINDOWS') :
    """
    Search all the supporting actors that won an oscar and save the actor along with the wikipedia film id and the actor ID in the cleane_data directory
    
    Params:
        OS: The operating system you are on, default is Windows.
    """
    # Get supporting actor and film data
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actor"
    # Construct the DataFrame
    page_ids = search_actors_and_films(url, OS)
    # Construct the DataFrame
    rows = []
    for actor_id, film_ids in page_ids.items():
        for film_id in film_ids:
            rows.append((actor_id, film_id))
    df = pd.DataFrame(rows, columns=['Supporting Actor id', 'film_id'])
    save_dataframe_to_csv(df, 'oscar_winning_supporting_actors.csv')

def load_oscar_winning_supporting_actresses(OS) :
    """
    Search all the supporting actresses that won an oscar and save the actor along with the wikipedia film id and the actress ID in the cleane_data directory
    Params :
        OS : The opearting system you are own, default Windows
    """
    # Get actress and film data
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actress"
     # Construct the DataFrame
    page_ids = search_actors_and_films(url, OS)
    # Construct the DataFrame
    rows = []
    for actor_id, film_ids in page_ids.items():
        for film_id in film_ids:
            rows.append((actor_id, film_id))
    
    df = pd.DataFrame(rows, columns=['Supporting Actress id', 'film_id'])
    save_dataframe_to_csv(df, 'oscar_winning_supporting_actresses.csv')


def search_actors_and_films(url, OS) : 
    if OS == 'MAC' :
        driver = webdriver.Chrome()
    else :
        service = Service('C:\webdrivers\chromedriver.exe')
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service = service, options = options)
    driver.get(url)
    time.sleep(2)
    #Search all the tr tags containings the informations on the actors, the role and the film
    tr_tags = driver.find_elements(By.TAG_NAME, 'tr')
    #define a variable actor name to match correctly the film id to the actor in case of several films
    page_ids = {}
    actor_name = ""
    actor_page_id = ''


    for tr_tag in tr_tags:
        # Extract td tag
        td_tags = tr_tag.find_elements(By.TAG_NAME, 'td')
    
        for td_tag in td_tags:
            #The winners have a golden background on wikipedia so we only consider the one with a golden background
            style = td_tag.get_attribute('style')    
            if 'rgb(250, 235, 134)' in style: 

                #Find the i_tag correspond to the film url
                i_tag = td_tag.find_element(By.TAG_NAME, 'i') if len(td_tag.find_elements(By.TAG_NAME, 'i')) > 0 else None
                if i_tag:
                    # Extract the <a> inside <i> in order to get the film url
                    a_tag = i_tag.find_element(By.TAG_NAME, 'a') if len(i_tag.find_elements(By.TAG_NAME, 'a')) > 0 else None
                    if a_tag:
                        film_url = a_tag.get_attribute('href')
                        #Get the film wikidata id
                        page_id = get_page_id_from_url(film_url)
                        if page_id:
                            page_ids.setdefault((actor_page_id), []).append(page_id)
                else:
                    #If not a film, we want to check if it's an actor
                    text = td_tag.text.strip()
                
                #Separated the cases in case we want to module the code depending on the winning circumstances
                #Set the variable 'actor_name' to the name of the actor to correctly save the film id with the corresponding actors
                #All actors won an oscar by playing in a film so each actor is associated with one or several films
                if '‡' in text or '§' in text or  '†' in text :
                    a_tag = td_tag.find_element(By.TAG_NAME, 'a') if len(td_tag.find_elements(By.TAG_NAME, 'a')) > 0 else None
                    if a_tag:
                        actor_url = a_tag.get_attribute('href')
                        #Get the film wikidata id
                        page_id = get_page_id_from_url(actor_url)
                        if page_id:
                            actor_page_id = page_id

    driver.quit()
    return page_ids


def search_winning_films_ids(url, OS):
    if OS == 'MAC':
        driver = webdriver.Chrome()
    else:
        service = Service('C:\\webdrivers\\chromedriver.exe')
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    time.sleep(5)
    page_ids = []

    tr_tags = driver.find_elements(By.TAG_NAME, 'tr')
    for tr_tag in tr_tags:

        #The winners have a golden background on wikipedia so we only consider the one with a golden background
        style = tr_tag.get_attribute('style')
        if 'rgb(250, 235, 134)' in style:

            td_tags = tr_tag.find_elements(By.TAG_NAME, 'td')
            if len(td_tags) > 1:
                #Get the winning film ID
                link_tag = td_tags[0].find_element(By.TAG_NAME, 'a')
                film_url = link_tag.get_attribute('href')
                
                # Extract page ID using Wikipedia API
                page_id = get_page_id_from_url(film_url)
                if page_id:
                    page_ids.append(page_id)
    driver.quit()
    return page_ids

def get_page_id_from_url(film_url):
    # Extract the title from the film URL
    title = film_url.split('/wiki/')[-1]
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&format=json"
    
    #Request to the wikipedia api
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        #Collect the page ids for the requested urls
        for page_id, page_data in pages.items():
            if 'missing' not in page_data:  # Ensures page exists
                return page_id
    #If unsucessful return None
    return None


def load_academy_award_winning_films(OS='WINDOWS'):
    # Set up the Chrome WebDriver for Selenium
    if OS == 'MAC':
        driver = webdriver.Chrome()
    else:
        service = Service('C:\\webdrivers\\chromedriver.exe')  # Update with the correct path to your chromedriver
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
    
    # Navigate to the Wikipedia page for Academy Award-winning films
    url = "https://en.wikipedia.org/wiki/List_of_Academy_Award%E2%80%93winning_films"
    driver.get(url)
    time.sleep(5)  # Allow time for the page to load

    # Initialize lists to store the extracted data
    film_names = []
    years = []
    awards_won = []
    nominations_received = []

    # Locate the table with Academy Award-winning films
    table = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//table[contains(@class, 'wikitable')]"))
    )

    # Get all rows of the table except the header row
    rows = table.find_elements(By.XPATH, ".//tr")[1:]  # Skips the header row

    for row in rows:
        columns = row.find_elements(By.XPATH, ".//td")

        # Ensure there are enough columns (Film, Year, Awards Won, Nominations Received)
        if len(columns) >= 4:
            film_name = columns[0].text.strip()  # First column: Film name
            year = columns[1].text.strip()  # Second column: Year
            awards_won_count = columns[2].text.strip()  # Third column: Awards won
            nominations_count = columns[3].text.strip()  # Fourth column: Nominations received

            # Append the extracted data to the lists
            film_names.append(film_name)
            years.append(year)
            awards_won.append(awards_won_count)
            nominations_received.append(nominations_count)

    # Close the browser
    driver.quit()

    # Create a DataFrame from the extracted data
    df_films = pd.DataFrame({
        'Movie name': film_names,
        'Movie release date': years,
        'Awards Won': awards_won,
        'Nominations': nominations_received
    })

    # Optionally, save to a CSV file
    save_dataframe_to_csv(df_films, "academy_award_winning_films.csv")


def merge_actors_dataframe() : 
    oscar_winning_actors = load_dataframe_from_csv('oscar_winning_actors.csv')
    oscar_winning_actresses = load_dataframe_from_csv('oscar_winning_actresses.csv')
    oscar_supporting_actors = load_dataframe_from_csv('oscar_winning_supporting_actors.csv')
    oscar_supporting_actresses = load_dataframe_from_csv('oscar_winning_supporting_actresses.csv')

    oscar_winning_actors.columns =  oscar_winning_actresses.columns =  oscar_supporting_actors.columns = oscar_supporting_actresses.columns = ['page_id', 'film_id']
    combined_df = pd.concat([oscar_winning_actors, oscar_winning_actresses, oscar_supporting_actors, oscar_supporting_actresses], axis=0)


    first_column_name = combined_df.columns[0]  # Get the name of the first column
    combined_df = combined_df.drop_duplicates(subset=first_column_name, keep='first')
    combined_df = combined_df.astype(int)
    
    processed_data = []
    for id in combined_df[first_column_name] : 
        item = get_actor_information(id)
        processed_data.append({key: next(iter(value)) if value else None for key, value in item.items()})   

    df = pd.DataFrame(processed_data)

    save_dataframe_to_csv(df, 'winning_actors_information.csv')





def get_ethnicity_info(ethnicitie):
    query = f"""
        SELECT ?item ?itemLabel WHERE {{
        ?item wdt:P646 "{ethnicitie}".  # Replace with your Freebase ID
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    
    return results['results']['bindings']