# Spell Finder

This is a tool for finding spells that are similar to a word provided.

It currently scans all spells from the PHB, XGE, and TCE books. This all happens in the `spell_unloaded.py` file; gathering the following information:
- Name
- Level
- School
- Description
- Source (i.e. which book it is from)

Next we extract important information from the file before cleaning it in `spell_info_extraction.py`. This currently extracts:
- Damage dice used (incl. modifiers)
- Misc dice used (incl. modifiers)
- Conditions mentioned
- Any saving throws required by the spell

After extracting this information and storing it in a dictionary associated with the spell it then cleans the text with regex functions to prepare it for preprocessing.

Preprocessing occurs in `spell_cleaning.py`. This does the following transformations to the spell descriptions in the order given:
- Tokenises all the words
- Filters out stop words (e.g. "the", "is", "and" etc...)
- Assigns pos_tags (e.g. "adjective", "noun" etc..)
- Stems the word using a lemmetizer (e.g. the words "walking", "walks", and "walked" would all be broken down into "walk")

Finally comes the `spell_finder.py` file. This takes an input of a single word and ranks all the spells from the previous steps to give a list of the top 10 spells that are most synonymous to the given word. It does this by:
- Asking for the word
- Preprocessing the word (similar to how the `spell_cleaning` file does it)
- Searching that word via the [datamuse API](https://www.datamuse.com/api/) to retrieve a list of synonyms
This can be manually overwritten by changing the values in the first few lines of code (as can the adj or noun):
```python
word_to_check = input("Please enter the word you wish to find spells similar to: ")
overwrite_tag = None     # Set to None for default
overwrite_limit = None   # Set to None for default
```
- It then compares the spell descriptions to the synonyms with a Vectorizer
- It then assesses the cosine simularity of the words
- Then it ranks them
- Then it normalises those ranks
- Finally outputs the top ten spells (with a score over 0.5) to the terminal
This can also be manually overwritten by changing the values in the first few lines of code:
```python
score_limit = 0.5        # Set to 0.5 for default
no_of_spells = 10        # Set to 10 for default
```

### Example:
Example with typing the word Fire into console (case insensitive)
```terminal
Please enter the word you wish to find spells similar to: Fire
```
Output:
```terminal
--------------------Getting Synonyms------------------
--------------------Loading Corpus--------------------
--------------------Finding Similarities--------------
--------------------Ranking Scores--------------------
Normalized Similarity Score: 1.00, Name: Produce Flame 
Normalized Similarity Score: 0.76, Name: Fire Bolt
Normalized Similarity Score: 0.74, Name: Continual Flame
Normalized Similarity Score: 0.68, Name: Control Flames
Normalized Similarity Score: 0.57, Name: Investiture of Flame
Normalized Similarity Score: 0.57, Name: Gentle Repose
Normalized Similarity Score: 0.57, Name: Searing Smite
Normalized Similarity Score: 0.52, Name: Tasha's Otherworldly Guise
Normalized Similarity Score: 0.51, Name: Immolation
```

### Plans for the future

I would like to make an interface, where you can select levels of spell, classes of spell, schools of spell.