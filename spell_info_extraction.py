import re

corpus = []

with open("./data/spell_desc.txt", "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        name, source, level, school, text = line.split("~")
        corpus.append((name, source, level, school, text))


def extract_dice_type(desc):
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


def extract_save_throw(desc):
    matches = re.findall(r"(\w+) saving throw", desc)
    if matches:
        return matches[-1]
    else:
        return "None"

def extract_conditions(desc):
    matches = re.findall(r"\{@condition (\w+)\}", desc)
    if matches:
        return matches[0]
    else:
        return "None"

def extract_creatures(desc):
    matches = re.findall(r"\{@creature ([\w\s\|]+)\}", desc)
    if matches:
        return matches[0]
    else:
        return "None"

new_corpus = []
for name, source, level, school, desc in corpus:
    desc = desc.replace("Ã—", "*")
    damage, dice = extract_dice_type(desc)
    save_throws = extract_save_throw(desc)
    conditions = extract_conditions(desc)
    creatures = extract_creatures(desc)
    new_desc = re.sub(r"(?i)This spell\'s damage increases.*", "", desc)
    new_desc = re.sub(r"\{@damage (\d+d\d+(?:\s*[+*/-]\s*\d+)*)\}", "damage", new_desc)
    new_desc = re.sub(r"\{@dice (\d+d\d+(?:\s*[+*/-]\s*\d+)*)\}", "dice", new_desc)
    new_desc = re.sub(r"\{@creature [\w\s\|]+\}", f"creature {creatures}", new_desc)
    new_desc = re.sub(r"\{@condition \w+\}",
                       f"condition {conditions}",
                       new_desc)
    new_corp = (name, source, level, school, new_desc, {"dice": dice, "damage": damage, "saving_throw_types": save_throws, "conditions": conditions})
    new_corpus.append(new_corp)

with open('./data/extracted_spell_desc.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join('%s~%s~%s~%s~%s~%s' % x for x in new_corpus))
