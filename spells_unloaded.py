import json
import pandas as pd
from IPython.display import display


def startup(path) -> dict:
    """Opens the json file

    Returns:
        dict: json file of all the spells
    """
    with open(path) as file:
        data = json.load(file)
    spells = data["spell"]
    spell_df = pd.DataFrame.from_dict(spells)
    columns_to_keep = ["name", "source", "level", "school", "entries"]
    for column_name in spell_df.columns:
        if column_name in columns_to_keep:
            pass
        else:
            spell_df.drop(columns=column_name, inplace=True)
    return spell_df


def column_headings(path) -> list:
    """Generates a list of all the headings used in the spells json

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


if __name__ == "__main__":
    global spell_df, col_heads
    spell_df_phb = startup("./spells/spells-phb.json")
    spell_df_xge = startup("./spells/spells-xge.json")
    spell_df_tce = startup("./spells/spells-tce.json")
    spell_df = pd.concat([spell_df_phb, spell_df_xge, spell_df_tce])
    spell_df.reset_index(inplace=True)
    col_heads = column_headings("./spells/spells-phb.json")

# print(col_heads)
# display(spell_df)


def entry_gatherer(df):
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
corpus = entry_gatherer(spell_df)

with open("./data/spell_desc.txt", "w", encoding="utf-8") as f:
    f.write("\n".join("%s~%s~%s~%s~%s" % x for x in corpus))