from matplotlib.pylab import f
from nbconvert import export


genre_categories_cmu = {
    "Documentary": [
        "Biography", "Documentary", "Concert film", "Docudrama",
        "Historical Documentaries", "Political Documentary", "Sponsored film",
        "Mondo film", "Essay Film", "Educational", "News", "Media Studies",
        "Anthropology", "Archaeology", "World History", "Environmental Science",
        "Film & Television History", "Political Documetary", "Journalism", "Education"
    ],
    "Action & Adventure": [
        "Action", "Adventure", "Action/Adventure", "Wuxia", "Martial Arts Film", "Spy", "Combat Films", "Fantasy Adventure",
        "Sword and sorcery", "Sword and sorcery films", "Chase Movie", "Heist",
        "Road movie", "Prison escape", "Alien invasion", "Road-Horror",
        "Swashbuckler films", "Sword and Sandal", "Revenge", "Cavalry Film",
        "Superhero", "Superhero movie", "Indian Western", "Revisionist Western",
        "Epic Western", "B-Western", "Hybrid Western", "Spaghetti Western",
        "Action Comedy", "Caper story", "Singing cowboy", "Northern", "Western",
        "Glamorized Spy Film", "Samurai cinema", "Private military company", "Race movie"
    ],
    "Comedy": [
        "Comedy", "Black comedy", "Parody", "Satire", "Comedy film",
        "Romantic comedy", "Adventure Comedy", "Comedy-drama", "Comedy of manners",
        "Gross-out film", "Gross out", "Slapstick", "Mockumentary", "Buddy film",
        "Stoner film", "Comedy Thriller", "Domestic Comedy", "Screwball comedy",
        "Workplace Comedy", "Heavenly Comedy", "Sex comedy", "Bloopers & Candid Camera",
        "Chick flick", "Buddy Picture", "Courtroom Comedy", "Comedy Western",
        "Comedy of Errors", "Comedy horror", "Fantasy Comedy", "Female buddy film",
        "Stand-up comedy","Ealing Comedies", "Media Satire"
    ],
    "Drama": [
        "Drama", "Crime Drama", "Crime Fiction", "Biographical film", "Family Drama",
        "Melodrama", "Political drama", "Marriage Drama", "Coming of age",
        "Coming-of-age film", "Childhood Drama", "Ensemble Film",
        "Juvenile Delinquency Film", "Social problem film", "Addiction Drama",
        "Inspirational Drama", "Teen", "Escape Film", "Courtroom Drama",
        "Legal drama", "Social issues", "Biopic [feature]", "Crime",
        "Kitchen sink realism", "Erotic Drama", "Tragedy", "Tragicomedy",
        "Slice of life story", "Family & Personal Relationships",
        "Interpersonal Relationships", "School story", "Prison", "Prison film"
    ],
    "Fantasy & Sci-Fi": [
        "Science Fiction", "Space western", "Supernatural", "Fantasy",
        "Sci-Fi Adventure", "Sci-Fi Horror", "Sci-Fi Thriller",
        "Apocalyptic and post-apocalyptic fiction", "Space opera", "Cyberpunk",
        "Steampunk", "Alien Film", "Future noir", "Romantic fantasy", "Dystopia",
        "Science fiction Western", "Fantasy Drama", "Mythological Fantasy", "Fairy tale",
        "Time travel", "Sci Fi Pictures original films", "Tokusatsu", "Doomsday film"
    ],
    "Thriller & Mystery": [
        "Thriller", "Mystery", "Crime Thriller", "Psychological thriller",
        "Erotic thriller", "Suspense", "Political thriller", "Romantic thriller",
        "Spy Thriller", "Whodunit", "Conspiracy fiction", "Crime Comedy",
        "Detective fiction", "Master Criminal Films", "Giallo", "Film noir",
        "Detective", "Gangster Film", "Action Thrillers", "Law & Crime"
    ],
    "Horror": [
        "Horror", "Zombie Film", "Slasher", "Creature Film", "Monster movie",
        "Psychological horror", "Natural horror films", "Haunted House Film",
        "Gothic Film", "Demonic child", "Period Horror", "Werewolf fiction",
        "Horror Comedy", "Splatter film", "Costume Horror", "Monster"
    ],
    "Romance": [
        "Romance Film", "Romantic drama", "Romantic comedy", "Chick flick",
        "Homoeroticism", "Romantic thriller"
    ],
    "Historical & Period": [
        "Historical drama", "Costume drama", "Costume Adventure", "Historical Epic",
        "Period piece", "Historical fiction",

          "British Empire Film", "Epic", "Americana",
        "History"
    ],
    "Music & Dance": [
        "Musical", "Musical Drama", "Musical comedy", "Rockumentary",
        "Jukebox musical", "Animated Musical", "Backstage Musical", "Dance",
        "Instrumental Music", "Music", "Punk rock", "Film-Opera", "Hip hop movies","Operetta"
    ],
    "Sports": [
        "Sports", "Boxing", "Baseball", "Extreme Sports", "Auto racing",
        "Horse racing"
    ],
    "Animated & Family": [
        "Animation", "Animated cartoon", "Children's/Family", "Family Film",
        "Children's Fantasy", "Family-Oriented Adventure", "Children's Entertainment",
        "Computer Animation", "Stop motion", "Silhouette animation",
        "Supermarionation", "Clay animation", "Children's", "Holiday Film",
        "Christmas movie", "Anime"
    ],
    "War & Political": [
        "Anti-war", "Anti-war film", "War effort", "Political cinema",
        "Propaganda film", "Political satire", "Cold War", "Nuclear warfare", "Gulf War", "War film", "The Netherlands in World War II", "Media Satire", "Foreign legion"
    ],
    "Experimental & Art": [
        "Art film", "Avant-garde", "Surrealism", "Experimental film",
        "New Hollywood", "Neo-noir", "Existentialism", "Kafkaesque", "Absurdism",
        "Indie", "Dogme 95", "Czechoslovak New Wave", "Expressionism", "Mumblecore",
        "Graphic & Applied Arts"
    ],
    "Religious & Spiritual": [
        "Religious Film", "Christian film", "Hagiography", "Heaven-Can-Wait Fantasies",
        "Feminist Film"
    ],
    "Other": [
        "Live action", "Adult", "Feature film", "Film adaptation", "Language & Literature",
        "Finance & Investing", "Psycho-biddy", "Fan film", "Blaxploitation", "Computers",
        "Film", "Libraries and librarians", "Travel", "Illnesses & Disabilities",
        "Linguistics", "Animals", "Health & Fitness", "Reboot", "Softcore Porn", "Silent film",
        "Short Film", "Gay pornography", "Latino", "Goat gland", "Natural disaster",
        "Travel", "Revisionist Fairy Tale", "Pre-Code", "B-movie", "Z movie",
        "Pornography", "Hardcore pornography", "Sexploitation", 
        "Fictional film", "Inventions & Innovations", "Filmed Play",
        "Women in prison films", "Tollywood", "Airplanes and airports", "Nature",
        "Roadshow theatrical release", "Television movie", "Statutory rape",
        "Pinku eiga", "Cult", "Outlaw biker film", "LGBT", "Roadshow/Carny",
        "Biker Film", "Erotica", "Japanese Movies", "Bengali Cinema", "Albino bias",
        "World cinema", "Glamorized Spy Film", "Pornographic movie", "Animal Picture",
        "Black-and-white", "Filipino Movies", "Disaster", "Early Black Cinema",
        "Jungle Film", "Gay Interest", "Anthology", "Gender Issues", "Business",
        "Culture & Society", "Film \\u00e0 clef","Tamil cinema", "Remake", "Malayalam Cinema", "Bollywood", "Exploitation", "Chinese Movies"
    ]
}
genre_categories = {
    "Documentary": [
        "documentary", "nature documentary", "docudrama", "animated documentary", 
        "rockumentary", "pseudo-documentary", "docufiction", "true crime", "muckraker", 
        "biography", "popular science", "environmental", "reality", "sports documentary", 
        "Archives and records", 'autobiography'
    ],
    "Action & Adventure": [
        "action", "action thriller", "action-adventure", "superhero", "adventure", 
        "spy", "heist", "thriller", "suspense", "swashbuckler", "survival", "vigilante", 
        "heroic bloodshed", "disaster", "space opera", "alien invasion", "road movie",
        "ninja", "prison", "bushranging", "kaiju", "pirate", "buddy", "trial",
        "tokusatsu", "western", "action fiction", "apocalyptic", "Spaghetti Western", 
        "neo-Western", "Action Movies", "Buddy cop", "Acid western", "Bruceploitation", 'robbery', 'hood', 'Ninja movie'
    ],
    "Comedy": [
        "comedy", "romantic comedy", "black comedy", "slapstick", "musical comedy",

        "comedy drama", "comedy horror", "comedy thriller", "satire", "parody", "dark comedy", 
        "stand-up comedy", "stoner", "mockumentary", "tragicomedy", "surreal humour", 
        "sex comedy", "comical satyre", "Masala", "Humour", "satyr play", 'comic book'
    ],
    "Drama": [
        "drama", "historical drama", "romantic drama", "social drama", "legal drama", 
        "political drama", "drama fiction", "melodrama", "coming-of-age", 
        "coming-of-age fiction", "rural drama",
        "anthology", "social", "teen", "spoken drama", "poverty porn", "magic realism", 'Medical fiction', "Children's Issues", 'Plague', 'tragedy'
    ],
    "Fantasy & Sci-Fi": [
        "fantasy", "dark fantasy", "urban fantasy", "space fantasy", "contemporary fantasy", 
        "fantasy anime", "science fiction", "cyberpunk", "steampunk", "dieselpunk", "space opera", 
        "post-apocalyptic fiction", "dystopian fiction", "alien invasion", "time-travel", 
        "technofantasy", "supernatural", "post-apocalyptic", "speculative fiction", 
        "Supernatural fiction", "fantasy drama", "metafiction", "biopunk", "dystopian", 
        "crossover fiction", "supernatural", "Chinese animation", "uchronia", 
        "Three Kingdoms"
    ],
    "Thriller & Mystery": [
        "thriller", "psychological thriller", "erotic thriller", "financial thriller", 
        "techno-thriller", "mystery", "detective", "whodunit", "noir", "neo-noir", "crime", 
        "gangster", "mystery fiction", "police procedural", "polar", "psychological", 
        "thriller play", "crime fiction", "mafia", "police", "noir fiction", 
        "detective fiction"
    ],
    "Horror": [
        "horror", "psychological horror", "cosmic horror", "folk horror", "vampire", 
        "zombie", "ghost", "slasher", "werewolf", "monster", "giallo", 
        "splatter", "cannibal", "Satanic", "found footage", "paranormal", "horror fiction", 
        "zombie comedy", "Vampire movies"
    ],
    "Romance": [
        "romance", "Romance" "gay romance", "lesbian-related", "romantic thriller", "romantic drama", 
        "romantic fantasy", "romantic novel", "chick flick", "LGBT-related", "erotic", 
        "erotic thriller", "romantic comedy", "Gay", "Gay Themed"
    ],
    "Historical & Period": [
        "historical", "historical drama", "historical fiction", "period", "alternate history", 
        "legend", "medieval", "sword-and-sandal", "epic", "biographical", "autobiographical", 
        "pseudo-documentary", "Robin Hood", "Jidaigeki", "adaptation", "Mormon cinema", 
        "Beach Party film", "Movies About Gladiators", "Beach Film"
    ],
    "Music & Dance": [
        "musical", "jukebox musical", "rockumentary", "pop music", "concert", "dance", 
        "aqua-musical", "music-themed", "cantopop", "J-pop", "rock music", "pop rock", 
        "progressive rock", "Therimin music", "i music", "opera", 'alternative rock'
    ],
    "Sports": [
        "sport", "sports drama", "boxing", "triathlon", "athletics", "gambling", "wrestling", 
        "triathlon s", "Parkour in popular culture"
    ],
    "Animated & Family": [
        "animated", "anime", "family", "childrens", "puppet", "adult animation", 
        "Christmas", "holiday-themed", "fantasy anime", "children's"
    ],
    "War & Political": [
        "war", "anti-war", "political drama", "political satire", "propaganda", "military", 
        "disaster", "heroic bloodshed", "political", "revolution", "military fiction",  'Patriotic film', 'political thriller'
    ],
    "Experimental & Art": [
        "art", "experimental", "absurdist fiction", "metacinema", "collage", "mashup", 
        "contemporary art", "protest art", "non-narrative", "surrealist cinema", "essay", 
        "fan edit", "alternate history", "screenlife", "short", "silent", 'independent', 
        "mumblecore", "interactive", "behind-the-scenes", "nonlinear narrative", 
        "ethnofiction", "New Queer Cinema", 'Point of view shot'
    ],
    "Religious & Spiritual": [
        "religious", "Christian", "Christian fiction", "spiritual", "religious satire", 
        "Satanic", "Christian art", "soul", "mythology", "biblical genre"
    ],
    "Other": [
        "BDSM-themed", "pornographic", "mockbuster", "student", "fan", "fiction", "pritcha", 
        "Masala", "transgender", "intersex", "live action", "blockbuster", "one-shot", 
        "educational", "CMC Pictures", "Outlaw", 'sexploitation', 'prequel','Sámi', 'Movie serial', 'Film à clef', 'Camp', 'score', 'Bildungsroman'
    ]
}

full_genre_dict = {}
for key, value in genre_categories.items():
    full_genre_dict[key] = value
for key, value in genre_categories_cmu.items():
    full_genre_dict[key].extend(value)
    
    

def categorize_genres(genres):
    uncategorized = []
    categories = []
    try:
        for genre in genres:
            if genre == '':
                continue
            for category, genre_list in full_genre_dict.items():
                if genre in genre_list:
                    categories.append(category)
            if categories == []:
                uncategorized.append(genre)
        return list(set(categories))
    except:
        return []