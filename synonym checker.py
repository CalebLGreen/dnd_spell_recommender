import requests

def get_synonyms(word):
    """Generate a list of synonyms using Datamuse API

    Args:
        word (string): The word that the system will search for a list of synonyms from

    Returns:
        list: a list of tuples containing synonyms and their corresponding rank
    """
    # Base URL for Datamuse API
    base_url = "https://api.datamuse.com/words"

    # Query parameters for finding synonyms
    params = {"ml": word}

    # Query Datamuse API for related terms
    response = requests.get(base_url, params=params)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract synonyms and assign ranks
        synonyms = [(word_obj["word"], rank + 1) for rank, word_obj in enumerate(response.json())]
        return synonyms
    else:
        print(f"Failed to retrieve synonyms for '{word}'. Status code: {response.status_code}")
        return []

# Example usage
word = "flames"
synonyms_with_rank = get_synonyms(word)
for synonym, rank in synonyms_with_rank:
    print(f"Synonym: {synonym}, Rank: {rank}")
