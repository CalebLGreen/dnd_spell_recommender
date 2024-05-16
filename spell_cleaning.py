# Imports
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag
import re
import ast

# Load the Corpus
corp = []

with open("./data/extracted_spell_desc.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        name, source, level, school, desc, add_info = line.split("~")
        add_info = ast.literal_eval(add_info)
        corp.append((name, source, level, school, desc, add_info))

print("-" * 50)

# Make a corpus with just the description
corpus = [x[4].lower() for x in corp]
no_punc_corpus = [re.sub(r"[^\w\s]", "", x) for x in corpus]

# Generate preprocessors
stop_words = set(stopwords.words("english"))
lem = WordNetLemmatizer()


# Define a function to attach usable pos_tags
def get_wordnet_pos(nltk_tag):
    if nltk_tag.startswith("J"):
        return wordnet.ADJ
    elif nltk_tag.startswith("V"):
        return wordnet.VERB
    elif nltk_tag.startswith("N"):
        return wordnet.NOUN
    elif nltk_tag.startswith("R"):
        return wordnet.ADV
    else:
        return None


# Process the entire corpus
processed_corpus = []
for no_punc_text in no_punc_corpus:
    # Tokenize
    tokens = word_tokenize(no_punc_text)
    # Remove stopwords
    filtered_list = [word for word in tokens if word.casefold() not in stop_words]
    # Attach pos_tags
    pos_tags = pos_tag(filtered_list)
    lemmed_words = []
    # Lemmatize words
    for word, tag in pos_tags:
        wordnet_pos = get_wordnet_pos(tag) or wordnet.NOUN
        lemmed_word = lem.lemmatize(word, pos=wordnet_pos)
        lemmed_words.append(lemmed_word)
    processed_corpus.append(lemmed_words)
    # Rejoin each description into its own string
    processed_texts = [" ".join(words) for words in processed_corpus]

# Reformat the data for saving in file
new_corpus = []
for idx, proc_desc in enumerate(processed_texts):
    new_corp = (
        corp[idx][0],   # Spell Name
        corp[idx][1],   # Spell Source Book
        corp[idx][2],   # Spell Level
        corp[idx][3],   # Spell School
        proc_desc,      # New preprocessed description
        corp[idx][5],   # Additional spell info, like dice values, conditions, and saving throws incurred
    )
    new_corpus.append(new_corp)

# Save to file
with open("./data/cleaned_spell_desc.txt", "w") as f:
    f.write("\n".join("%s~%s~%s~%s~%s~%s" % x for x in new_corpus))
