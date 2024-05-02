import regex

# defines what we want to remove from string for langID
nonword_replace_str = r'[^\p{Word}\p{Zs}]|\d'  # either (not a word nor a space) or (is digit)
nonword_replace_pattern = regex.compile(nonword_replace_str)