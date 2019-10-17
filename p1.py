import os, re, codecs
import nltk
from nltk.metrics.scores import accuracy
from nltk import sent_tokenize, word_tokenize
#from nltk.metrics.distance import edit_distance
from nltk.metrics.distance import jaccard_distance
#from nltk.metrics.distance import masi_distance


def get_perguntas():
    """
    Importar perguntas para formato a ser processado
    """

def preprocessing():
    """
    Pre-processamento das perguntas:
    - remover Stop Words
    - Stemming
    - Lemmatization ???
    - Bag of words para cada pergunta
    - TF-IDF
    """

def cosine_similarity(query, pergunta):
    """
    Pronduto interno entre o query e uma pergunta da base de dados
    """

def get_ID(query):
    """
    Percorre cada pergunta e compara com o query.
    Retorna o ID da pergunta mais semelhante.
    Experimentar várias semelhancas antes de escolher a final.
    """

def main():
    """
    Funcao principal.
    """

    # get_perguntas

    # preprocessing

    # for query in queries:
    #    id = get_ID(query)
    #    por id no ficheiro de respostas

main()