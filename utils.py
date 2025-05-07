import re

def clean_filename(name):
    return re.sub(r'[\\/*?:"<>|]', "_", name)
