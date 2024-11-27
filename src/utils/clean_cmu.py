import ast


def clean_movies_cmu(movie) : 
    # Apply ast.literal_eval to convert strings to dictionaries
    movie['Movie countries'] = movie['Movie countries'].apply(ast.literal_eval)

    # Extract and clean the values, removing parentheses
    movie['Movie countries'] = movie['Movie countries'].apply(lambda x: ', '.join(x.values()))
        
    movie['Movie languages'] = movie['Movie languages'].apply(ast.literal_eval)

    # Extract and clean the values, removing parentheses
    movie['Movie languages'] = movie['Movie languages'].apply(lambda x: ', '.join(x.values()))

    # Apply ast.literal_eval to convert strings to dictionaries
    movie['Movie genres'] = movie['Movie genres'].apply(ast.literal_eval)

    # Extract and clean the values, removing parentheses
    movie['Movie genres'] = movie['Movie genres'].apply(lambda x: ', '.join(x.values()))

    return movie