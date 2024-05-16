import re
from typing import Tuple, List

# Load data from file
corpus = []

with open("./data/spell_desc.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        name, source, level, school, text = line.split("~")
        corpus.append((name, source, level, school, text))


# Extract dice values from the description
def extract_dice_type(desc: str) -> Tuple[List[str], List[str]]:
    """Searches through a string to find @damage and @dice values (including any modifiers),
     Examples:
    - {@dice 1d4 + 20} -> 1d4 + 20
    - {@damage 6d8} -> 6d8
    - {@dice 4d8 + 2d6} -> 4d8 + 2d6
    Supports the format of up to (xdx [+-*/] xdx)

    Args:
        desc (str): A spell description with damage and dice values

    Returns:
        Tuple[list, list]: The first value is a list of damage dice matches,
        the second value is a list of other dice values (usually not associated with damage).
        Returns "None" as a string in place if none is found
    """
    # Uses re.findall() to find the damage and dice values
    dmg_matches = re.findall(r"\{@damage (\d+d\d+(?:\s*[+*/-]\s*\d+)*)\}", desc)
    dice_matches = re.findall(r"\{@dice (\d+d\d+(?:\s*[+*/-]\s*\d+)*)\}", desc)
    if dmg_matches and dice_matches:
        return dmg_matches, dice_matches
    elif dmg_matches:
        return dmg_matches, "None"
    elif dice_matches:
        return "None", dice_matches
    else:
        return "None", "None"


def extract_save_throw(desc: str) -> List[str]:
    """Extracts a list of saving throws mentioned in the text

    Args:
        desc (str): A spell desription as one string

    Returns:
        List[str]: A list of strings with the saving throws in, returns a string "None" if none is found
    """
    matches = re.findall(r"(\w+) saving throw", desc)
    if matches:
        return matches[-1]  # Returns the word before the phrase "saving throw"
    else:
        return "None"


def extract_conditions(desc: str) -> List[str]:
    """Extracts a list of conditions inflicted by the spell

    Args:
        desc (str): A spell description as one string

    Returns:
        _type_: A list of conditions afflicted by the spell, returns a string "None" if none is found
    """
    matches = re.findall(r"\{@condition (\w+)\}", desc)
    if matches:
        return matches[0]
    else:
        return "None"


def extract_creatures(desc) -> List[str]:
    """Extracts a list of creatures summoned or mentioned by the spell

    Args:
        desc (str): A spell description as one string

    Returns:
        _type_: A list of creatures summoned or mentioned by the spell, returns a string "None" if none is found
    """
    matches = re.findall(r"\{@creature ([\w\s\|]+)\}", desc)
    if matches:
        return matches[0]
    else:
        return "None"


new_corpus = []
# Time for the main information instraction
for name, source, level, school, desc in corpus:
    # First replaces a unicode encoding error of a weird x to a *
    desc = desc.replace("Ã—", "*")
    # Extract all the details previously mentioned with earlier functions
    damage, dice = extract_dice_type(desc)
    save_throws = extract_save_throw(desc)
    conditions = extract_conditions(desc)
    creatures = extract_creatures(desc)
    # Removes spell damage increasing at future levels description in cantrips 
    #- stop bias with the word damage being mentioned 4-5 additional times
    new_desc = re.sub(r"(?i)This spell\'s damage increases.*", "", desc)
    # Replace the {@something text} text foumd in most spell descriptions with simplified text
    new_desc = re.sub(r"\{@damage (\d+d\d+(?:\s*[+*/-]\s*\d+)*)\}", "damage", new_desc)
    new_desc = re.sub(r"\{@dice (\d+d\d+(?:\s*[+*/-]\s*\d+)*)\}", "dice", new_desc)
    new_desc = re.sub(r"\{@creature [\w\s\|]+\}", f"creature {creatures}", new_desc)
    new_desc = re.sub(r"\{@condition \w+\}", f"condition {conditions}", new_desc)
    # Rewrite the information back into a savable format
    new_corp = (
        name,
        source,
        level,
        school,
        new_desc,
        {
            "dice": dice,
            "damage": damage,
            "saving_throw_types": save_throws,
            "conditions": conditions,
        },
    )
    new_corpus.append(new_corp)

# Save data to file
with open("./data/extracted_spell_desc.txt", "w", encoding="utf-8") as f:
    f.write("\n".join("%s~%s~%s~%s~%s~%s" % x for x in new_corpus))
