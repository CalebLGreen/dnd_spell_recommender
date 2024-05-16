import json
import pandas as pd
from IPython.display import display
from typing import Tuple, List


def startup(
    path: str, columns_to_keep: list = ["name", "source", "level", "school", "entries"]
) -> pd.DataFrame:
    """Loads the json file and converts to a dataframe

    Args:
        path (str): The relative or absolute path to the data files
        columns_to_keep (list, optional): A list of column headers to keep. Defaults to ["name", "source", "level", "school", "entries"].

    Returns:
        pd.DataFrame: A data frame with all the data from the spell json, keeps the columns from the
        columns to keep list
    """
    with open(path) as file:
        data = json.load(file)
    spells = data["spell"]
    spell_df = pd.DataFrame.from_dict(spells)
    for column_name in spell_df.columns:
        if column_name in columns_to_keep:
            pass
        else:
            spell_df.drop(columns=column_name, inplace=True)
    return spell_df

# A method for gathering a list of the column headings for use if needed
def column_headings(path) -> list:
    """Generates a list of all the headings used in the spells json

    Args:
        path (str): The relative or absolute path to the data files

    Returns:
        list: list of spell headings
    """
    with open(path) as file:
        data = json.load(file)
    spells = data["spell"]
    cols = []
    for entry in spells:
        for e in entry:
            if e in cols:
                pass
            else:
                cols.append(e)

    return cols

# Works on startup
if __name__ == "__main__":
    global spell_df, col_heads
    spell_df_phb = startup("./spells/spells-phb.json")
    spell_df_xge = startup("./spells/spells-xge.json")
    spell_df_tce = startup("./spells/spells-tce.json")
    # Unions the dataframes together
    # TODO: Make modular so you can suuply a list of dataframes to be made and unioned
    spell_df = pd.concat([spell_df_phb, spell_df_xge, spell_df_tce])
    spell_df.reset_index(inplace=True)
    col_heads = column_headings("./spells/spells-phb.json")

# print(col_heads)
# display(spell_df)


def entry_gatherer(df: pd.DataFrame) -> List[Tuple[str, str, str, str, List[str]]]:
    """Gathers all entries portions of text description from the spell entry section (including nested information)

    Args:
        df (pd.DataFrame): The spell dataframe from the startup() function

    Returns:
        List[Tuple[str, str, str, str, List[str]]]: A list of tuples, where each tuple is a spell with the following values:
        - Spell name
        - Spell source book
        - Spell level
        - Spell school
        - Full spell description 
    """
    corpus = []
    for idx, item in enumerate(df.loc[:, "entries"]):
        full_sentence = ""
        for i in item:
            if type(i) == str:
                full_sentence += i
                full_sentence += " "
            elif type(i) == dict:
                for parts in i.values():
                    if isinstance(parts, list):
                        for sentences in parts:
                            if type(sentences) == str:
                                full_sentence += sentences
                                full_sentence += " "
                            elif type(sentences) == list:
                                for s in sentences:
                                    if type(s) == str:
                                        full_sentence += s
                                        full_sentence += " "

        corpus.append(
            (
                df.loc[idx, "name"],
                df.loc[idx, "source"],
                df.loc[idx, "level"],
                df.loc[idx, "school"],
                full_sentence,
            )
        )
    return corpus


print("-" * 50)
# Gain the full list of tuples of every spell from the concatted dataframe
corpus = entry_gatherer(spell_df)

# Save data to file
with open("./data/spell_desc.txt", "w", encoding="utf-8") as f:
    f.write("\n".join("%s~%s~%s~%s~%s" % x for x in corpus))
