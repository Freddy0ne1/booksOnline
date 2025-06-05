import re  # Module d'expressions régulières, utilisé ici pour nettoyer les noms de fichiers

def clean_filename(name):
    """
    Nettoie une chaîne de caractères pour qu'elle soit utilisable comme nom de fichier.
    
    Remplace tous les caractères interdits par un underscore (_) :
    \ / * ? : " < > |
    """
    return re.sub(r'[\\/*?:"<>|]', "_", name)
