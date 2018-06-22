
def get_no_meaning_word():
    """
    :return: a list of word considered to have no meaning (conjunction, pronouns, etc)
    """
    return {
        'who', 'whom', 'which', 'what', 'whose', 'whoever', 'whatever', 'whichever', 'whomever',
        'I', 'you', 'he', 'she', 'it', 'we', 'they', 'what', 'who',
        'me', 'him', 'her', 'it', 'us', 'you', 'them', 'whom',
        'mine', 'yours', 'his', 'hers', 'ours', 'theirs',
        'these', 'those', 'this', 'that',
        'a', 'an', 'the',
        'for', 'nor', 'but', 'or', 'so', 'yet', 'as', 'and', 'no', 'not',
        'on', "on's", 'in', 'into', 'with', 'by', 'to', 'of', 'at', 'upon',
        'while', 'if', 'during', 'when', 'from', 'such',
        'has', "it's", 'made', '...', 'etc.', 'e.g.',
        'does', "doesn't"
    }
