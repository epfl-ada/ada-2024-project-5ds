
# ADA 2024 - Team 5DS -- "Predicting Success Through the Winning Formula: What Makes a Movie Gain an Oscar?"

## Abstract:
In this project, we aim to identify the factors that make a movie Oscar-worthy. By analyzing an extensive dataset of movies and actors, we aim to uncover patterns and correlations that may reveal a "winning formula" for cinematic recognition. This exploration is motivated by the influence awards have on careers, industry standards, and public interest. Through this analysis, we hope to provide actionable insights for filmmakers and audiences about the elements contributing to Oscar success.

Our approach also examines how both actors and films benefit from awards, particularly Oscars, and delves into trends surrounding genres, themes, and cast features. This can help uncover how these elements influence recognition by award panels.

## Research Questions:
### Core Questions:
1. What factors (e.g., genre, themes, or plot elements) correlate with a movie’s likelihood of winning an Oscar?
2. How do actor characteristics (e.g., age, gender, ethnicity) influence their chances of receiving an Oscar?
3. What role does diversity play in Oscar nominations and wins for actors and films?
4. Is there a relationship between box office performance and Oscar success?
5. How does sentiment in movie plots impact their chances of winning?

### Sub-questions:
1. Is there a correlation between an actor's physical characteristics (age, height, ethnicity) and their likelihood of winning an Oscar?
2. Do the Best Actor and Best Supporting Actor awards reflect different patterns in diversity, particularly regarding underrepresented groups?
3. Do specific TV tropes associated with characters increase their chances of receiving an Oscar?
4. How do public reviews translate a movie's prestige?

## Dataset:
We utilize the CMU Summary Corpus (updated to 2024), supplemented with IMDb and Rotten Tomatoes scores, to analyze data spanning decades. This dataset provides information on award-winning films, actors, genres, and audience/critic reviews. To ensure relevance, we:

- Standardized dates (birth and release years).
- Extracted key features like genres, languages, and ethnicities.
- Addressed missing values, retaining NaNs to leverage other variables.

This enriched dataset will allow us to explore factors affecting both individual and film-specific Oscar success.

## Methods:
### Data Cleaning:
- Standardized dates for consistency.
- Extracted key attributes such as movie genres and actor characteristics.
- Retained NaN values where relevant.

### Exploratory Data Analysis (EDA):
- Visualized relationships between factors such as actor characteristics, movie genres, and award success.
- Explored distributions, correlations, and trends.

### Advanced Analysis:
1. **Character Representation and Success:**
   - Clustering characters by traits (e.g., gender, archetypes) to identify patterns in Oscar-winning roles.
   - Statistical tests confirming correlations between character traits and awards.

2. **Actor Diversity:**
   - Created a diversity index and analyzed its impact on lead vs. supporting roles.
   - Explored historical trends and recent shifts in representation.

3. **Film Genre and Box Office:**
   - Modeled relationships between genres, box office revenues, and award outcomes.
   - Built a predictive model evaluating genre and performance correlations.

4. **Network Analysis:**
   - Developed a Neo4j graph model connecting films, actors, genres, and awards to uncover complex relationships.

5. **Sentiment Analysis:**
   - Assessed how plot sentiments (e.g., positive, negative) align with Oscar outcomes.
   - Evaluated sentiment’s interaction with genre and theme.

6. **Website Development:**
   - Created a user-friendly website hosted on GitHub Pages, showcasing the project, visualizations, and interactive elements.
   - Website contributions were led by Yassine Wahidy, ensuring an engaging platform for presenting findings.

7. **Data Story Development:**
   - Developed the data story to narrate the insights and findings of the project.
   - The data story integrates analysis, visualizations, and a clear narrative to effectively communicate the "Oscar-winning formula."
   - Contributions to the data story were a collaborative effort across the team, ensuring accessibility and engagement for a broad audience.

### Graph Plotting:
- Generated visualizations such as world maps, runtime distributions, genre dominance, and sentiment word clouds to identify trends and patterns.

## Tasks:
### Task 1: Character Representation and Oscar Success
- Analyze attributes such as gender, age, role significance, and personality archetypes using clustering techniques.
- Perform statistical tests to assess the significance of these traits in Oscar outcomes.

### Task 2: Actor Diversity Analysis
- Quantify diversity in Oscar-winning films by creating an index encompassing ethnicity, gender, and nationality.
- Compare diversity trends in lead versus supporting roles.
- Use historical and recent data to identify shifts in representation.

### Task 3: Film Genre and Box Office Performance
- Analyze the relationship between genres and Oscar success using descriptive statistics and predictive modeling.
- Evaluate the impact of box office performance on Oscar nominations and wins.
- Incorporate external data (e.g., Rotten Tomatoes scores) for enhanced analysis.

### Task 4: Network Modeling
- Use Neo4j to model relationships between films, actors, genres, and awards as a graph.
- Identify key nodes and relationships to reveal patterns in Oscar success.
- Implement queries to extract actionable insights from the network.

### Task 5: Sentiment Analysis
- Assess sentiment polarity and emotional tones in plot summaries to determine correlations with Oscar success.
- Investigate sentiment distribution across genres and themes.
- Develop a predictive model combining sentiment, genre, and box office features.

### Task 6: Website and Data Story Development
- Design and implement an interactive and visually appealing website using Jekyll and GitHub Pages.
- Develop the data story to narrate the insights and findings of the project.
- The data story integrates analysis, visualizations, and a clear narrative to effectively communicate the "Oscar-winning formula."
- Contributions to the data story were a collaborative effort across the team, ensuring accessibility and engagement for a broad audience.

## Timeline:
- **15 Nov 2024:** Data handling, preprocessing, and initial exploratory analysis.
- **30 Nov 2024:** Complete all tasks and perform preliminary analysis.
- **6 Dec 2024:** Compile final analysis and draft Jekyll site.
- **13 Dec 2024:** Write final report.
- **20 Dec 2024:** Submit final deliverables.

## Team Contributions:
- Thierry Sokhn: Task 1 & 2 (Character Representation, Diversity Analysis).
- Yassine Wahidy: Task 3 & 6 (Genre and Box Office Analysis, Website and Data Story Development).
- Khalil Ouazzani Chahdi: Task 2 & 4 (Diversity and Network Analysis).
- William Jallot: Task 4 (Network Modeling).
- Amine Bengelloun: Task 3 & 5 (Genre, Box Office, Sentiment Analysis).

## Deliverables:
- Final GitHub repository containing cleaned datasets, scripts, notebooks, and visualizations.
- Data story hosted on GitHub Pages.
- README reflecting the comprehensive project scope.

This README reflects updates aligning with Milestone 3 objectives while retaining key elements from previous milestones. Let me know if additional adjustments are required.
