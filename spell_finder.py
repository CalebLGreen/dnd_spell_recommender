import ast
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import sys
import requests


# Example word for which synonyms are to be found
word_to_check = input(
    "Please enter the word you wish to find spells similar to: "
).lower()
overwrite_tag = None  # Set to None for default
overwrite_limit = None  # Set to None for default
score_limit = 0.5  # Set to 0.5 for default
no_of_spells = 10  # Set to 10 for default

print("-" * 20 + "Getting Synonyms" + "-" * 18)


# Function for retrieving synonyms from the wordnet package
def get_synonyms(word: str, limit: int):
    """Generate a list of synonyms using Datamuse API

    Args:
        word (string): The word that the system will search for a list of synonyms from

    Returns:
        list: a list of synonyms of the word given, or an empty list if no synonyms are found
    """
    # URL for Datamuse API
    base_url = "https://api.datamuse.com/words"

    # parameters for finding synonyms
    params = {"ml": word, "max": limit}

    # Make the request
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract synonyms from the response
        synonyms = [word_obj["word"] for word_obj in response.json()]
        return synonyms
    else:
        print(
            f"Failed to retrieve synonyms for '{word}'. Status code: {response.status_code}"
        )
        return []


def get_wordnet_pos(tag: str) -> str:
    """Converts the tag given by pos_tag from nltk to the pos_tag for wornet to work with.

    Args:
        tag (str): pos_tag to be converted

    Returns:
        str: wordnet.X string
    """
    if tag.startswith("J"):
        return wordnet.ADJ
    elif tag.startswith("V"):
        return wordnet.VERB
    elif tag.startswith("N"):
        return wordnet.NOUN
    elif tag.startswith("R"):
        return wordnet.ADV
    else:
        return wordnet.NOUN  # default to noun if tag not found


# Initialise lemmatizer
lem = WordNetLemmatizer()


def clean_word(word: str) -> str:
    """tokenizes the word given, then searches for the word tag and converts it to the wordnet version
    to be used to find the lemma of that word

    Args:
        word (str): the word to clean

    Returns:
        str: the word tag associated with the given word
    """
    token = word_tokenize(word)
    pos_tags = pos_tag(token)
    wordnet_pos = pos_tags[0][1]
    return wordnet_pos


# Clean the word and attach wordnet tag
tag = clean_word(word_to_check)

# Find the lemma of that word
lemmed_word = lem.lemmatize(
    word_to_check, pos=get_wordnet_pos(overwrite_tag if overwrite_tag else tag)
)
# Get synonyms of the word
synonyms = get_synonyms(lemmed_word, limit=overwrite_limit if overwrite_limit else 15)
synonyms.append(word_to_check)

# Check that at least 1 synonym has been found
try:
    100 / (len(synonyms) - 1)
except ZeroDivisionError:
    print("No synonyms found")
    sys.exit()

print("-" * 20 + "Loading Corpus" + "-" * 20)

# Load the Corpus
corp = []

with open("./data/cleaned_spell_desc.txt", "r") as f:
    for line in f:
        line = line.strip()
        name, source, level, school, desc, add_info = line.split("~")
        # Make sure that the additional information is understood to be a dictionary
        add_info = ast.literal_eval(add_info)
        corp.append((name, source, level, school, desc, add_info))

descriptions = [f"{x[0]}~{x[1]}~{x[2]}~{x[3]}~{x[4]}" for x in corp]

print("-" * 20 + "Finding Similarities" + "-" * 14)

# Calculate TF-IDF vectors for descriptions
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(descriptions)

# Calculate similarity scores between descriptions and synonyms
similarity_scores = cosine_similarity(tfidf_matrix, vectorizer.transform(synonyms))

# Calculate adjusted similarity scores
adjusted_scores = similarity_scores.max(axis=1) + similarity_scores.mean(axis=1)

# Normalize the scores
normalized_scores = (adjusted_scores - min(adjusted_scores)) / (
    max(adjusted_scores) - min(adjusted_scores)
)

print("-" * 20 + "Ranking Scores" + "-" * 20)

# Rank descriptions based on normalized scores
ranked_descriptions = [
    (desc, score, score2)
    for desc, score, score2 in zip(descriptions, normalized_scores, adjusted_scores)
]
# Sort the scores based on their normalised score
ranked_descriptions.sort(key=lambda x: x[1], reverse=True)

# Print scores and the spell name
for desc, score, score2 in ranked_descriptions[:10]:
    if score > 0.5:
        spell_name = desc.split("~")[0]
        formatted_score = "{:.2f}".format(score)
        print(
            f"Normalized Similarity Score: {formatted_score}, Raw Score: {score2}, Name: {spell_name} "
        )
