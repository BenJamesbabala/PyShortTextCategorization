import re

from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.stem import PorterStemmer

def preprocess_text(text, pipeline):
    """ Preprocess the text according to the given pipeline.

    Given the pipeline, which is a list of functions that process an
    input text to another text (e.g., stemming, lemmatizing, removing punctuations etc.),
    preprocess the text.

    :param text: text to be preprocessed
    :param pipeline: a list of functions that convert a text to another text
    :return: preprocessed text
    :type text: str
    :type pipeline: list
    :rtype: str
    """
    if len(pipeline)==0:
        return text
    else:
        return preprocess_text(pipeline[0](text), pipeline[1:])

def text_preprocessor(pipeline):
    """ Return the function that preprocesses text according to the pipeline.

    Given the pipeline, which is a list of functions that process an
    input text to another text (e.g., stemming, lemmatizing, removing punctuations etc.),
    return a function that preprocesses an input text outlined by the pipeline, essentially
    a function that runs :func:`~preprocess_text` with the specified pipeline.

    :param pipeline: a list of functions that convert a text to another text
    :return: a function that preprocesses text according to the pipeline
    :type pipeline: list
    :rtype: function
    """
    return lambda text: preprocess_text(text, pipeline)

def standard_text_preprocessor_1():
    """ Return a commonly used text preprocessor.

    Return a text preprocessor that is commonly used, with the following steps:

    - removing special characters,
    - removing numerals,
    - converting all alphabets to lower cases,
    - removing stop words, and
    - stemming the words (using Porter stemmer).

    This function calls :func:`~text_preprocessor`.

    :return: a function that preprocesses text according to the pipeline
    :rtype: function
    """
    stemmer = PorterStemmer()
    pipeline = [lambda s: re.sub('[^\w\s]', '', s),
                lambda s: re.sub('[\d]', '', s),
                lambda s: s.lower(),
                lambda s: ' '.join(filter(lambda s: not (s in stopwords.words()), word_tokenize(s))),
                lambda s: ' '.join(map(lambda t: stemmer.stem(t), word_tokenize(s)))
               ]
    return text_preprocessor(pipeline)