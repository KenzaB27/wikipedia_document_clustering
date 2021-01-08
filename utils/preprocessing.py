from bs4 import BeautifulSoup, Tag
from tqdm import tqdm, tqdm_pandas
from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import LancasterStemmer, WordNetLemmatizer

import re, string, unicodedata, contractions
import nltk

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
tqdm_pandas(tqdm())
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('punkt')
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# =======================================================================================================================
#                                           TEXT DATA PREPROCESSING
# This file includes all the utility functions used for data preprocessing for the specific task of clustering and
# classifying a dataset of wikipedia articles.
# Text data preprocessing consist of 3 major tasks:
#   - Noise Removal
#   - Normalization
#   - Tokenisation & Segmentation
# =======================================================================================================================

# =======================================================================================================================

# =======================================================================================================================
#                                               NOISE REMOVAL
# =======================================================================================================================
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

    tags_to_be_removed = ['semantics', 'math',
                          'annotation', 'cite', 'h2', 'h3']
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

# =======================================================================================================================
def expand_contractions(text):
    """Expands contractions of a text string with the library contractions.

    Args:
        text (string): the string text to be decontracted.

    Returns:
        string: The text decontracted.
    """
    return contractions.fix(text)

# =======================================================================================================================
def remove_noise(text):
    """ Removes the overall noise from an html text.

    Args:
        text (string): an html markup string with contractions.

    Returns:
        string: plain-text decontracted.
    """
    text = remove_html_tags(text)
    text = expand_contractions(text)
    return text

# =======================================================================================================================
def remove_noise_from_df(df):
    """Removes HTML and contractions noise from a dataframe.

    Args:
        df (pandas df): a dataframe with noisy content.

    Returns:
        pandas df: a clean dataframe.
    """
    return df.progress_apply(remove_noise)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# =======================================================================================================================
#                                               NORMALISATION
# =======================================================================================================================
def remove_accented_chars(text):
    """Removes accented characters from a string as we are dealing with engilsh words.

    Args:
        text (string): the string text containing accented characters. 

    Returns:
        string: The text cleaned without accented characters.
    """
    new_text = unicodedata.normalize('NFKD', text).encode(
        'ascii', 'ignore').decode('utf-8', 'ignore')
    return new_text

# =======================================================================================================================
def remove_punctuation(text):
    """Removes punctuation from a string

    Args:
        text (string): the text with punctuation.

    Returns:
        string: The text without punctuation.
    """
    s = ''.join([i for i in text if i not in frozenset(string.punctuation)])
    return s

# =======================================================================================================================
def remove_numbers(text):
    """Remove numbers from a string.

    Args:
        text (string): the string text to be cleaned from numbers. 

    Returns:
        string: The text cleaned from numbers.
    """
    clean = re.compile('\d+')
    return re.sub(clean, '', text)

# =======================================================================================================================
def remove_special_characters(text):
    """Removes special character, leaves only alphbetic characters.

    Args:
        text (string): a text with special characters.

    Returns:
        string: a text without special characters
    """
    pat = r'[^a-zA-z\s]'
    return re.sub(pat, '', text)

# =======================================================================================================================
def remove_stopwords(text):
    """Removes stop words from text

    Args:
        text (string): text with stop words.

    Returns:
        [type]: text without stop words.
    """
    words = text.split()
    new_words = []
    for word in words:
        if word not in stopwords.words("english"):
            new_words.append(word)
    return " ".join(new_words)

# =======================================================================================================================
def stem_words(text):
    """ Stem words in text.

    Args:
        text (string): The content to be stemmed.

    Returns:
        string: a standardize text.
    """
    stemmer = nltk.porter.PorterStemmer()
    text=' '.join([stemmer.stem(word) for word in text.split()])
    return text

# =======================================================================================================================
def lemmatize_verbs(text):
    """Lemmatize verbs of text.

    Args:
        text (string): The content to be lemmatised.
    Returns:
        string: a standardize text.
    """
    lemmatizer = WordNetLemmatizer()
    text = ' '.join([lemmatizer.lemmatize(word, pos='v')
                     for word in text.split()])
    return text

# =======================================================================================================================
def normalize_text(text):
    """Normalization pipeline of a given text.

    Args:
        text (string)

    Returns:
        string: standardized text.
    """
    text = text.lower()
    text = text.strip()
    text = remove_accented_chars(text)
    text = remove_punctuation(text)
    text = remove_numbers(text)
    text = remove_special_characters(text)
    text = remove_stopwords(text)
    text = stem_words(text)
    text = lemmatize_verbs(text)
    return text

# =======================================================================================================================
def normalize_df(df):
    """Normalize the content of a dataframe.

    Args:
        df (pandas df): the dataframe to be normalized.

    Returns:
        pandas df: the standardized df.
    """
    return df.progress_apply(normalize_text)
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

