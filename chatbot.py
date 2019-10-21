import sys
import xml_parser
from utils  import preproc_aux
from nltk.stem import RSLPStemmer
import nltk.corpus as corpus
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


# stemmer for portuguese words
stemmer = RSLPStemmer()

# list of portuguese stopwords
stopwords = corpus.stopwords.words('portuguese')


def get_questions(xml_file_name):
    '''
    Importar perguntas para formato a ser processado
    '''

    ''' get the content of all the document in the xml structure '''
    xml_docs = xml_parser.get_documents_xml_file(xml_file_name)
    ''' get the list of all docs, where each doc have content associated [title, [answer_id,questions] ] '''
    docs_parsed = xml_parser.get_all_documents_content(xml_docs)
    ''' print the first 2 documents '''
    #print(docs_parsed[:2])   

    questions = []
    for doc in docs_parsed:
        titulo = preprocess_sentence(doc[0])
        for faq in doc[1]:
            # iterate over variations of same faq
            for i, q in enumerate(faq[1]):
                # preprocessing
                prep = preprocess_sentence(q)
                if prep != []:
                    questions.append([prep,faq[0],titulo])

    return questions


def get_queries(test_file_name):
   '''
   Importar perguntas para formato a ser processado
   '''
   test_file = open(test_file_name, mode="r", encoding="utf-8")
   queries = []
   for query in test_file:
       prep = preprocess_sentence(query)
       queries.append(prep)

   return queries


def preprocess_sentence(sent):
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
    tokens = [t for t in tokens if not t in stopwords]
    # stemming
    stem_tokens = [stemmer.stem(t) for t in tokens]

    return stem_tokens


def get_ID(query, questions):
    """
    Percorre cada pergunta e compara com o query.
    Retorna o ID da pergunta mais semelhante, usando o TD-IDF.
    Experimentar várias semelhancas antes de escolher a final.
    """
    best_id = 'none'
    best_similarity = -1
    best_match = ''
    for question in questions:
        tfidf = TfidfVectorizer().fit_transform([' '.join(query), ' '.join(question[0])])
        pairwise_similarity = tfidf * tfidf.T
        sim = pairwise_similarity[(0,1)]
        if sim > best_similarity:
            best_similarity = sim
            best_id = question[1]
            best_match = ' '.join(question[0])

    # Debug
    print("Query \t\t= "+' '.join(query))
    print("Best match \t= "+best_match)
    print("Best_id \t= "+best_id+"\n")

    return best_id

def write_results(queries, questions):
    '''
    Get best ID for each query and write in results.txt
    '''
    results_file = open("results.txt", mode="w", encoding="utf-8")
    for query in queries[:-1]:
        results_file.write(get_ID(query, questions)+"\n")

    results_file.write(get_ID(queries[-1], questions))

#def main():
def init_main(xml_file_name, test_file_name):

   ''' get the xml file name and test file name from command line '''
   #xml_file_name, test_file_name  = sys.argv[1: ]
   # lista com os queries preprocessados
   queries = get_queries(test_file_name)
   # formato de elemento de questions: [pergunta, id, titulo]
   questions = get_questions(xml_file_name)
   # find best match and print in results.txt
   write_results(queries, questions)

'''
if __name__ == "__main__":
    main()
'''