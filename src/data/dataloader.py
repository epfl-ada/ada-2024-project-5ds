import pandas as pd
import os
import ast
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from utils.csv import save_dataframe_to_csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ECmport 
import requests



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
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture"
    df = search_golden_names(url,OS)
    save_dataframe_to_csv(df, "oscar_winning_films")

def load_oscar_winning_films_ids(OS = 'WINDOWS') :
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture"
    df = search_golden_names_ids(url,OS)
    save_dataframe_to_csv(df, "oscar_winning_films_ids")

def load_oscar_winning_actors(OS = 'WINDOWS') :
    """
    Search all the actors that won an oscar 
    Params :
        OS : The opearting system you are own, default Windows
    """
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actor"
    names_list = search_special_symbols(url, OS)
    df = pd.DataFrame(names_list, columns=['actors'])
    save_dataframe_to_csv(df, 'oscar_winning_actors')

def load_oscar_winning_actresses(OS = 'WINDOWS') :
    """
    Search all the actresses that won an oscar 
    Params :
        OS : The opearting system you are own, default Windows
    """
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Actress"
    names_list = search_special_symbols(url, OS)
    df = pd.DataFrame(names_list, columns=['actresses'])
    save_dataframe_to_csv(df, 'oscar_winning_actresses')

def load_oscar_winning_supporting_actors(OS = 'WINDOWS') :
    """
    Search all the supporting actors that won an oscar 
    Params :
        OS : The opearting system you are own, default Windows
    """
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actor"
    names_list = search_special_symbols(url, OS)
    df = pd.DataFrame(names_list, columns=['supporting_actors'])
    save_dataframe_to_csv(df, 'oscar_winning_supporting_actors')

def load_oscar_winning_supporting_actresses(OS = 'WINDOWS') :
    """
    Search all the supporting actresses that won an oscar 
    Params :
        OS : The opearting system you are own, default Windows
    """
    url = "https://en.wikipedia.org/wiki/Academy_Award_for_Best_Supporting_Actress"
    names_list = search_special_symbols(url, OS)
    df = pd.DataFrame(names_list, columns=['supporting_actresses'])
    save_dataframe_to_csv(df, 'oscar_winning_supporting_actresses')
   
def load_reviews(movies_list, max_number_of_reviews,OS) :

    if OS == 'MAC' :
        driver = webdriver.Chrome()
    else :
        service = Service('C:\webdrivers\chromedriver.exe')
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service = service, options = options)

    real_movie_titles = []
    movie_reviews = pd.DataFrame(columns=['Movie name', 'Review'])

    for movie_title in movies_list:
        print(movie_title[0])
        url = f"https://www.rottentomatoes.com/search?search={movie_title[0].replace(' ', '_').lower()}"
        driver.get(url)
        time.sleep(5)
        link = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a[@data-qa='info-name']"))  # Replace with your actual locator
        )
        link.click()
        time.sleep(5)
        # Wait until the rt-text element with the slot attribute is present
        rt_text_element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//rt-text[@slot='title']"))
        )


        title_name = rt_text_element.text
        real_movie_titles.append(title_name)
        base_url = driver.current_url
        
        reviews_url = f"{base_url}/reviews?type=user"
        

        driver.get(reviews_url)
    
        time.sleep(1)  
       
        number_reviews = 0
        output_txt_path = 'movie_reviews.txt'

        with open(output_txt_path, mode='a', encoding='utf-8') as file:
            while number_reviews < max_number_of_reviews:
                try:
                    reviews = WebDriverWait(driver, 15).until(
                        EC.presence_of_all_elements_located((By.XPATH, "//p[@class='audience-reviews__review js-review-text']"))
                    )
                    for review in reviews:
                        review_text = review.text.strip()
                        movie_review_entry = f"Movie name: {title_name}\nReview: {review_text}\n\n"
                        file.write(movie_review_entry)
                        number_reviews += 1

                    load_more_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.XPATH, "//rt-button[@data-qa='load-more-btn']"))
                    )
                    driver.execute_script("arguments[0].scrollIntoView(true);", load_more_button)
                    load_more_button.click()
                except:
                    break
    driver.quit()
    return real_movie_titles, 


def search_special_symbols(url, OS) : 
    if OS == 'MAC' :
        driver = webdriver.Chrome()
    else :
        service = Service('C:\webdrivers\chromedriver.exe')
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service = service, options = options)
    driver.get(url)
    names_list = []
    time.sleep(5)

    tr_tags = driver.find_elements(By.TAG_NAME, 'tr')

    for tr_tag in tr_tags:
        # Extract 'td' elements from the row
        td_tags = tr_tag.find_elements(By.TAG_NAME, 'td')

        if len(td_tags) > 0:
            for td_tag in td_tags:
                text = td_tag.text.strip()

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
    return names_list

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

def search_golden_names_ids(url, OS):
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
        style = tr_tag.get_attribute('style')

        if 'rgb(250, 235, 134)' in style:
            td_tags = tr_tag.find_elements(By.TAG_NAME, 'td')
            if len(td_tags) > 1:
                link_tag = td_tags[0].find_element(By.TAG_NAME, 'a')
                film_url = link_tag.get_attribute('href')
                
                # Extract page ID using Wikipedia API
                page_id = get_page_id_from_url(film_url)
                if page_id:
                    page_ids.append(page_id)

    driver.quit()
    movies_oscar_winning = pd.DataFrame(page_ids, columns=['Page ID'])
    return movies_oscar_winning

def get_page_id_from_url(film_url):
    # Extract the title from the film URL
    title = film_url.split('/wiki/')[-1]
    api_url = f"https://en.wikipedia.org/w/api.php?action=query&titles={title}&format=json"
    
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        for page_id, page_data in pages.items():
            if 'missing' not in page_data:  # Ensures page exists
                return page_id
    return None
