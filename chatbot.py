import sys
import xml_parser
from utils  import preproc_aux
from nltk.stem import RSLPStemmer
import nltk.corpus as corpus
from nltk import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


""" For preprocessing """
# stemmer for portuguese words
stemmer = RSLPStemmer()
# list of portuguese stopwords
stopwords = corpus.stopwords.words('portuguese')


def get_data(doc_contents,noStop,bool_val):   
    ''' given a list with all the faq question list and the respective answer id ,
        and the a boolean value, bool_val, corresponding to the stemming of data.
        Return a list,preprocessed, with :
          - train question 
          - train answer
          - test question
          - test answer 
     ''' 
    q_train = []
    a_train = []
    q_test = []
    a_test = []
  
    for doc_cont in doc_contents:        
        all_faqs = doc_cont[1]
        for faq in all_faqs :
            answer_id = faq[0]
            questions_list = faq[1]
 
            for q in questions_list:
     
                q_train.append(' '.join(preprocess_sentence(q,noStop,bool_val)).lower())
                a_train.append(int(answer_id))   
                
    return q_train , a_train

def get_queries(test_file_name, noStop, Stem):
   '''
   Importar perguntas para formato a ser processado
   '''
   test_file = open(test_file_name, mode="r", encoding="utf-8")
   queries = []
   for query in test_file:
       prep = preprocess_sentence(query, noStop, Stem)
       queries.append( ' '.join(prep).lower() )

   return queries


def preprocess_sentence(sent, noStop, toStem=False):
    '''
    Pre-processamento das perguntas:
    - remove acentos
    - tokenize
    - remove Stop Words
    - Stemming
    '''
    # remove accentuation
    sent = preproc_aux(sent)
    # tokenize
    tokens = word_tokenize(sent)
    # remover stopwords
    tokens = [t for t in tokens if not t in stopwords] if noStop else tokens
    # stemming
    if toStem == True:
        return [stemmer.stem(t) for t in tokens]
    else :
        return tokens



def tfidf_cosine(q_train,a_train,q_test):
    """
    TF-IDF and Cosine Similarity
    """

    ids_list = []

    sentences = q_train[:]

    # file where we will write the IDs
    results_file = open("results.txt", mode="w", encoding="utf-8")
    
    # get best id for each query
    for test_q in q_test :

        best = 0.25
        a_id = '0'
        el_index = 0
        sentences.append(test_q)
        
        # Tf-idf-weighted document-term matrix.
        # one sentences per line, one term per column
        tfidf = TfidfVectorizer().fit_transform(sentences)

        # compute cosine similarity between the query and all other sentences
        vals = cosine_similarity(tfidf[-1], tfidf[:-1])[0]

        # get index of highest similarity
        a_id = vals.argmax()

        # compute if similarity is significant
        # otherwise, query is not recognized
        if(vals[a_id] < best):
            ids_list.append("0")
        else:
            ids_list.append(a_train[a_id])

        sentences = sentences[:-1]

    for best_id in ids_list[:-1]:
        results_file.write(str(best_id)+"\n")

    results_file.write(str(ids_list[-1]))


    

def main():

    # get command line arguments
    xml_file_name, test_file_name  = sys.argv[1: ]

    # parse the xml file
    docs = xml_parser.get_documents_xml_file(xml_file_name)
    faqs = xml_parser.get_all_documents_content(docs)

    # data with stremming and removing stopwords
    q_train , a_train = get_data(faqs,True,True)

    # preprocess queries
    q_test = get_queries(test_file_name,True, True)

    # find best match and print in results.txt
    tfidf_cosine(q_train, a_train, q_test)


if __name__ == "__main__":
    main()
