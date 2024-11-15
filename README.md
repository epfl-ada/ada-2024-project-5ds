# ADA 2024 - Team 5DS -- "Predicting success through the winning formula: What makes a movie gain an Oscar ?"

### Abstract:

In this project, we’re diving into what makes a movie stand out enough to win an oscar. By analyzing a dataset of movies, we aim to uncover trends across factors such as genre, theme, and actor characteristics, questioning if there exists a “winning formula” for cinematic recognition. This choice is mostly mostivated because award recognition not only boosts a film’s prestige but can also propel careers and influence industry standards, from actors to screenwriters with a deep mark on our society nowadays.

Our approach looks at how both actors and films benefit from awards, espcially from an oscar. By exploring these patterns, we aim to understand the main elements that make a movie award-worthy. This could give helpful insights to both filmmakers and audiences about how genre, themes, and cast play a role in making a movie stand out to award panels.

### Subquestions we want to answer:

In this analysis there are several reasearch subquestions we want to answer : 
- Is there a correlation between an actor's physical characteristics (age, height, ethnicity) and their likelihood of winning an Oscar?
- Do the Best Actor and Best Supporting Actor awards reflect different patterns in the diversity of actors, particularly in terms of underrepresented groups?
- Do specific TV tropes associated with characters played by actors increase their chances of receiving an Oscar?
- Is there a correlation between the movie's phenotype and/or box-office sales and/or plots and the award it won?
- How does public reviews translate a movie's prestige?
- How do a movie’s genre, themes, and plot elements correlate with its likelihood of winning an Oscar?

### Used Dataset

We will use the CMU Summary Corpus, updated to 2024, which includes movies from 2015 to 2024 sourced from Wikipedia. Our focus will be on identifying award-winning films from this period and before, specifically those recognized by the Oscar. In addition,  we also gathered comprehensive data on Oscar-winning actors, actresses, supporting actors, and supporting actresses, as well as winning films. This includes a detailed list of films with the number of awards won and nominations received from 1927 to 2023. It will allow us to analyze both individual and film-specific factors that contribute to winning an Oscar. To enrich our dataset, we will also include Rotten Tomatoes scores out of 100 for both critics and audience reviews.

We believe that this comprehensive dataset will provide enough information to address the questions we aim to explore in our analysis.

### Methods

When extracting data from the CMU dataset, we found that additional processing and filtering were necessary to ensure the data was clean and relevant for our analysis.

#### Data cleaning 
The birth dates were standardized by retaining only the year of birth, and the same process was applied to the movie release dates. Additionally, we extracted important features such as movie genres, languages, and other relevant columns required for our analysis. For ethnicities, we also managed to extract the different values.

We are aware that our dataframe contains certain NaN values for some columns. However, we have decided to retain them in order to utilize the other available variables.

#### Initial analyses
Before diving into complex modeling, we performed exploratory data analysis to understand the distribution and trends in our dataset. This included inspecting correlations, missing values, and data ranges to ensure accuracy and completeness.

#### Graph Plotting
Various graphs were plotted to visualize relationships between factors such as actor characteristics, movie genres, and award success. These visualizations helped in identifying patterns and potential correlations that will be explored further in our analysis.

### Tasks

##### Task 1:

##### Task 2: Actor Diversity Analysis

This task will focus on quantifying the diversity of actors in Oscar-winning films. An index will be created to assess the diversity of actors based on ethnicity, gender, and nationality. Statistical comparisons will be made between lead and supporting actors to determine if there is a significant difference in diversity between the two roles. The analysis will also explore whether diversity plays a significant role in Oscar nominations and wins, with potential implications for the broader industry.

##### Task 3: Film Genre and Box Office Performance Analysis

This task will investigate how genre and box office performance correlate with Oscar nominations and wins. Using the tvtropes dataset, we will classify films by genre and explore how genre affects the likelihood of winning an Oscar. We will also examine the relationship between a film’s box office performance and its chances of winning an Oscar. A predictive model will be developed to assess how well box office and genre performance can predict Oscar nominations and wins.

##### Task 4: Network Modeling of Relationships Between Films, Actors, and Awards

In this task, we will create a network model in Neo4j to explore the relationships between films, actors, and awards. The network will include nodes representing films, actors, genres, and awards, with relationships linking films to their genres, actors, and the awards they have received. This model will be used to generate insights into the connections between different attributes, such as how film genre and actor diversity are linked to Oscar outcomes.


### Proposed timeline

- `15.11.2024`: Data Handling and Preprocessing & Initial Exploratory Data Analysis.
- `30.11.2024`: Finishing the 5 tasks (each member of the team doing one), and preliminary analysis
- `06.12.2024`: Commpile the final analysis, and writing on Jekyll.
- `13.12.2024`: Writing of the final report. 
- `20.12.2024`: Deadline for submitting.  

### Team Organization

Each member will take care of one task (specified before):
- Thierry Sokhn: Task 1 & 2
- Yassine Wahidy: Task 3
- Khalil Ouazzani Chahdi: Task 2 & 4
- William Jallot: Task 4
- Amine Bengelloun: Task 3 & 5

Each team member is responsible of their own task, while of course being responsible for writing their part of the data story and creating the final visualizations. 
