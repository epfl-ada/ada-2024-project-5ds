import wikipediaapi
from bs4 import BeautifulSoup
import requests
import pandas as pd
import sys
from SPARQLWrapper import SPARQLWrapper, JSON, CSV
sys.path.append('/Users/williamjallot/Desktop/ADA/ada-2024-project-5ds/src/utils')
from data_utils import save_dataframe_to_csv
from collections import defaultdict

user_agent = "Mus/1.0"
wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='en')
sparql = SPARQLWrapper("https://query.wikidata.org/sparql", agent=user_agent)


def extend_dataset() :
    films_since_2013 = {}

    for year in range(2013, 2025):  # Adjust end year as needed
        films = get_films_by_year(year)
        films_since_2013[year] = films
        print(f"{year}: Retrieved {len(films)} films.")
        film_dict = {}

    for year, films in films_since_2013.items():
        print(f"\n{year} films:")
        for film in films:
            film_info = get_film_info(film)
            if film_info is not None:
                film_dict[film] = film_info
                print(f'processed film {film}.')
            else:
                print(f"Failed to retrieve information for '{film}'.")
                
        df = pd.DataFrame.from_dict(film_dict, orient='index').T
        save_dataframe_to_csv(df, f'films_{year}.csv')
        
        film_dict = {}
            
            
        print(f'Processed films for {year}.')
        
        


def get_films_by_year(year):
    category_name = f"Category:{year} films"
    category = wiki_wiki.page(category_name)

    # Check if the category exists
    if not category.exists():
        print(f"Category '{category_name}' does not exist.")
        return []

    # Collect film titles from the category
    films = [page.title for page_title, page in category.categorymembers.items()
             if page.ns == wikipediaapi.Namespace.MAIN]
    return films


def get_id(page_title):
    # Get the page
    
    wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='en')
    page = wiki_wiki.page(page_title)
    
    if not page.exists():
        print(f"Page '{page_title}' does not exist.")
        return None
    
    # Get the page url
    url = page.canonicalurl
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page '{page_title}'.")
        return None
    
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find("table", {"class": "infobox"})  # Find the infobox table
    
    informations = soup.find("a", title="More information about this page")
    
    page_info_url = "https://en.wikipedia.org"+informations.get("href")
    
    page_info_response = requests.get(page_info_url)
    
    page_info_soup = BeautifulSoup(page_info_response.content, 'html.parser')
    
    # Find all <tr> tags
    rows = page_info_soup.find_all('tr')

    # Loop through each row to find the one with the desired structure
    for row in rows:
        # Find all <td> elements within the row
        tds = row.find_all('td')
        # Check if there are exactly two <td> elements and if one contains the desired text
        if len(tds) == 2 and "Wikidata item ID" in tds[0].text:
            # Found the desired row, process it as needed
            wikidata_id = tds[1].text.strip()
        elif len(tds) == 2 and "Page ID" in tds[0].text:
            page_id = tds[1].text.strip()
    
    return wikidata_id, page_id

def get_wikidata_info(wikidata_id, sparqlAgent):
    
    query = f"""
      SELECT ?film ?filmLabel (MIN(?releaseDate) AS ?earliestReleaseDate) (MAX(?boxOffice) AS ?highestBoxOffice) ?runtime 
            (GROUP_CONCAT(DISTINCT ?languageLabel; separator=", ") AS ?languages) 
            (GROUP_CONCAT(DISTINCT ?countryLabel; separator=", ") AS ?countries) 
            (GROUP_CONCAT(DISTINCT ?genreLabel; separator=", ") AS ?genres)
            (GROUP_CONCAT(DISTINCT ?reviewScoreLabel; separator=", ") AS ?reviewScores)
            (GROUP_CONCAT(DISTINCT ?awardLabel; separator=", ") AS ?awardsReceived)
            (GROUP_CONCAT(DISTINCT ?nominatedAwardLabel; separator=", ") AS ?awardsNominated)
            ?capitalCost WHERE {{
        BIND(wd:{wikidata_id} AS ?film)  # Using the specific Wikidata movie ID
        
        ?film wdt:P31 wd:Q11424;  # Instance of film
              wdt:P577 ?releaseDate.
        
        OPTIONAL {{ ?film wdt:P2142 ?boxOffice. }}
        OPTIONAL {{ ?film wdt:P2047 ?runtime. }}
        OPTIONAL {{ ?film wdt:P364 ?language. ?language rdfs:label ?languageLabel. FILTER(LANG(?languageLabel) = "en") }}
        OPTIONAL {{ ?film wdt:P495 ?country. ?country rdfs:label ?countryLabel. FILTER(LANG(?countryLabel) = "en") }}
        OPTIONAL {{ ?film wdt:P136 ?genre. ?genre rdfs:label ?genreLabel. FILTER(LANG(?genreLabel) = "en") }}
        OPTIONAL {{ ?film wdt:P444 ?reviewScoreLabel. }}
        OPTIONAL {{ ?film wdt:P166 ?award. ?award rdfs:label ?awardLabel. FILTER(LANG(?awardLabel) = "en") }}
        OPTIONAL {{ ?film wdt:P1411 ?nominatedAward. ?nominatedAward rdfs:label ?nominatedAwardLabel. FILTER(LANG(?nominatedAwardLabel) = "en") }}
        OPTIONAL {{ ?film wdt:P2130 ?capitalCost. }}

        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
      }}
      GROUP BY ?film ?filmLabel ?runtime ?capitalCost
      """
    
    sparqlAgent.setQuery(query)
    sparqlAgent.setReturnFormat(JSON)
    results = sparqlAgent.query().convert()
    
    return results['results']['bindings']

def get_film_info(film_title):
    wikidata_id, page_id = get_id(film_title)
    
    if wikidata_id is None:
        print(f"Failed to retrieve Wikidata ID for '{film_title}'.")
        return None
    
    film_info = get_wikidata_info(wikidata_id, sparql)
    
    
    info = {}
    info['page_id'] = page_id
    info['wikidata_id'] = wikidata_id
    
    if len(film_info) == 0:
        info['film'] = film_title
        info['release_date'] = None
        info['box_office'] = None
        info['runtime'] = None
        info['languages'] = None
        info['countries'] = None
        info['genres'] = None
        info['reviewScores'] = None
        info['awardsReceived'] = None
        info['awardsNominated'] = None
        info['capitalCost'] = None
    
    
    
    for film in film_info:
        
        info['film'] = film['filmLabel']['value']
        info['release_date'] = film['earliestReleaseDate']['value']
        info['box_office'] = film['highestBoxOffice']['value'] if 'highestBoxOffice' in film else None
        info['runtime'] = film['runtime']['value'] if 'runtime' in film else None
        info['languages'] = film['languages']['value'] if 'languages' in film else None
        info['countries'] = film['countries']['value'] if 'countries' in film else None
        
        
        genres = film['genres']['value'] if 'genres' in film else None
        genres = genres.split(", ") if genres is not None else None
        info['genres'] = [genre.replace("film", "").strip() for genre in genres if len(genre.split()) <= 2 ]
        
        reviewScores = film['reviewScores']['value'] if 'reviewScores' in film else None
        reviewScores = reviewScores.split(", ") if reviewScores is not None else None
        info['reviewScores'] = reviewScores
        
        awardsReceived = film['awardsReceived']['value'] if 'awardsReceived' in film else None
        awardsReceived = awardsReceived.split(", ") if awardsReceived is not None else None
        info['awardsReceived'] = awardsReceived
        
        awardsNominated = film['awardsNominated']['value'] if 'awardsNominated' in film else None
        awardsNominated = awardsNominated.split(", ") if awardsNominated is not None else None
        info['awardsNominated'] = awardsNominated
        
        info['capitalCost'] = film['capitalCost']['value'] if 'capitalCost' in film else None

        
    return info


def get_wikidata_id(page_title):
    # Get the page
    
    wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='en')
    page = wiki_wiki.page(page_title)
    
    if not page.exists():
        print(f"Page '{page_title}' does not exist.")
        return None
    
    # Get the page url
    url = page.canonicalurl
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page '{page_title}'.")
        return None
    
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find("table", {"class": "infobox"})  # Find the infobox table
    
    informations = soup.find("a", title="More information about this page")
    
    page_info_url = "https://en.wikipedia.org"+informations.get("href")
    
    page_info_response = requests.get(page_info_url)
    
    page_info_soup = BeautifulSoup(page_info_response.content, 'html.parser')
    
    # Find all <tr> tags
    rows = page_info_soup.find_all('tr')

    # Loop through each row to find the one with the desired structure
    for row in rows:
        # Find all <td> elements within the row
        tds = row.find_all('td')
        # Check if there are exactly two <td> elements and if one contains the desired text
        if len(tds) == 2 and "Wikidata item ID" in tds[0].text:
            # Found the desired row, process it as needed
            wikidata_id = tds[1].text.strip()
        elif len(tds) == 2 and "Page ID" in tds[0].text:
            page_id = tds[1].text.strip()
    
    return wikidata_id, page_id

def get_title_from_page_id(page_id):
 
    url = f'https://en.wikipedia.org/w/api.php?action=query&format=json&pageids={page_id}&prop=wikidata'

    # Make the API request
    response = requests.get(url)
    data = response.json()
    # Extract the Wikidata ID
    title = data['query']['pages'][str(page_id)]['title']
    return title

def get_wikidata_id(page_title):
    # Get the page
    
    wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language='en')
    page = wiki_wiki.page(page_title)
    
    if not page.exists():
        print(f"Page '{page_title}' does not exist.")
        return None
    
    # Get the page url
    url = page.canonicalurl
    
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to retrieve page '{page_title}'.")
        return None
    
    # Parse the page content
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find("table", {"class": "infobox"})  # Find the infobox table
    
    informations = soup.find("a", title="More information about this page")
    
    page_info_url = "https://en.wikipedia.org"+informations.get("href")
    
    page_info_response = requests.get(page_info_url)
    
    page_info_soup = BeautifulSoup(page_info_response.content, 'html.parser')
    
    # Find all <tr> tags
    rows = page_info_soup.find_all('tr')

    # Loop through each row to find the one with the desired structure
    for row in rows:
        # Find all <td> elements within the row
        tds = row.find_all('td')
        # Check if there are exactly two <td> elements and if one contains the desired text
        if len(tds) == 2 and "Wikidata item ID" in tds[0].text:
            # Found the desired row, process it as needed
            wikidata_id = tds[1].text.strip()
            break
    
    return wikidata_id

def get_wikdata_information(wikidata_id, sparqlAgent):
    query =f"""
        SELECT ?actor ?sexLabel ?nativeLanguageLabel ?countryOfCitizenshipLabel ?ethnicGroupLabel WHERE {{
        wd:{wikidata_id} wdt:P31 wd:Q5;  # Ensures it's a human (actor)
                                OPTIONAL {{ wd:{wikidata_id} wdt:P21 ?sex. 
                                        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }} }}  # Sex or gender label
                                OPTIONAL {{ wd:{wikidata_id} wdt:P103 ?nativeLanguage. 
                                        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }} }}  # Native language label
                                OPTIONAL {{ wd:{wikidata_id} wdt:P27 ?countryOfCitizenship. 
                                        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }} }}  # Country of citizenship label
                                OPTIONAL {{ wd:{wikidata_id} wdt:P172 ?ethnicGroup. 
                                        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }} }}  # Ethnic group label
        }}
        """



    sparqlAgent.setQuery(query)
    sparqlAgent.setReturnFormat(JSON)
    results = sparqlAgent.query().convert()
    
    return results['results']['bindings']

def get_actor_information(page_id):
    title = get_title_from_page_id(page_id)
    wikidata_id = get_wikidata_id(title)
    
    if wikidata_id is None:
        return None
    
    results = get_wikdata_information(wikidata_id, sparql)
    
    actor_info = defaultdict(set)
    
    if len(results) == 0:
        return None
    
    for result in results:
        actor_info['page_id'].add(page_id)	
        actor_info['wikidata_id'].add(wikidata_id)
        actor_info['actor'].add(title)
        actor_info['sexLabel'].add(result['sexLabel']['value'] if 'sexLabel' in result else None)
        actor_info['nativeLanguageLabel'].add(result['nativeLanguageLabel']['value'] if 'nativeLanguageLabel' in result else None)
        actor_info['countryOfCitizenshipLabel'].add(result['countryOfCitizenshipLabel']['value'] if 'countryOfCitizenshipLabel' in result else None)
        actor_info['ethnicGroupLabel'].add(result['ethnicGroupLabel']['value'] if 'ethnicGroupLabel' in result else None)
        
    
    return actor_info
    