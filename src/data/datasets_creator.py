import os
import sys


import pandas as pd
import time
import sys

from dataloader import load_oscar_winning_films_ids, load_oscar_winning_actors, load_oscar_winning_actresses, load_oscar_winning_supporting_actors, load_oscar_winning_supporting_actresses, load_academy_award_winning_films, merge_actors_dataframe
from extend_dataset import extend_dataset


def create_datasets() :
    OS = 'MAC'
    print('Creating the external datasets :')
    
    print('Merge actor : ')
    merge_actors_dataframe() 

    print('Searching information on awards for films')
    load_academy_award_winning_films(OS)
    print('Completed')

    print('Searching information about winning films :')
    load_oscar_winning_films_ids(OS)
    print('Completed')

    print('Searching information about winning actresses:')
    load_oscar_winning_actresses(OS)
    print('Completed')

    print('Searching information about winning actors :')
    load_oscar_winning_actors(OS)
    print('Completed')

    print('Searching information about winning supporting actors :')
    load_oscar_winning_supporting_actors(OS)
    print('Completed')


    print('Searching information about winning supporting actresses :')
    load_oscar_winning_supporting_actresses(OS)
    print('Completed')


    print('Extending the CMU dataset with newer films :')
    extend_dataset()
    print('Completed')


create_datasets()
    