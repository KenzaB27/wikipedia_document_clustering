import re
import string
from bs4 import BeautifulSoup, Tag
import contractions
import unicodedata


def remove_html_tags(text):
    """Remove html tags from a string text.
    We want to get rid of all the math formulas (tags:math, semantics, annotation).
    The references and further reading are not relevant for our study. (tags: cite, See_also, ... )
    Titles will be removed too as they are quite similar in all wikipedia pages (i.e Introduction, History,... )
    which may bias the clustering. Moreover titles are usually cotained in the paragraph below them.
    Args:
        text (string): the string text to be cleaned from html tags.

    Returns:
        string: The text cleaned from all html tags.
    """
    soup = BeautifulSoup(text)

    tags_to_be_removed = ['semantics', 'math', 'annotation', 'cite', 'h2', 'h3']
    for tag_ in tags_to_be_removed:
            for tag in soup.find_all(tag_):
                tag.decompose()

    ids = ['See_also', 'References', 'Footnotes',
           'Bibliography', 'Further_reading', 'External_links']
    for id in ids:
        el = soup.find('span', id=id)
        if el:
            el.decompose()

    return soup.get_text()

def remove_accented_chars(text):
    """Removes accented characters from a string.

    Args:
        text (string): the string text containing accented characters. 

    Returns:
        string: The text cleaned without accented characters.
    """
    new_text = unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode('utf-8', 'ignore')
    return new_text

def replace_contractions(text):
    """Removes contractions from a tet string.

    Args:
        text (string): the string text to be decontracted.

    Returns:
        string: The text decontracted.
    """
    return contractions.fix(text)

def remove_punctuation(text):
    """Removes punctuation from a string

    Args:
        text (string): the text with punctuation.

    Returns:
        string: The text without punctuation.
    """
    s = ''.join([i for i in text if i not in frozenset(string.punctuation)])
    return s

def remove_numbers(text):
    """Remove numbers from a string.

    Args:
        text (string): the string text to be cleaned from numbers. 

    Returns:
        string: The text cleaned from numbers.
    """
    text = text.replace('"', '')
    text = text.replace('\d+,', ' ')
    clean = re.compile('\d+')
    return re.sub(clean, '', text)

def remove_special_characters(text):
    """Removes special character.

    Args:
        text (string): a text with special characters.

    Returns:
        string: a text without special characters
    """
    pat = r'[^a-zA-z\s]'
    return re.sub(pat, '', text)

def remove_noise(text):
    """Removes all the noise from a text.

    Args:
        text (string): text with noise (numbers, punctuation, html tags, ...)

    Returns:
        string: a text that contains only words.
    """
    text = remove_html_tags(text)
    # text = remove_accented_chars(text)
    text = remove_punctuation(text)
    text = remove_numbers(text)
    text = remove_special_characters(text)
    return text

def remove_noise_from_df(df):
    """Removes noise from a dataframe.

    Args:
        df (pandas df): a dataframe with noisy content.

    Returns:
        pandas df: a clean dataframe.
    """
    return df.apply(remove_noise).apply(str.strip).apply(str.lower)
