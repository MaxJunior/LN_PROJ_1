import sys
import random # Dev
import re # Dev
import xml_parser
from utils  import preproc_aux
from nltk.stem import RSLPStemmer
import nltk.corpus as corpus
from nltk import word_tokenize
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


""" FOR DEVELOPMENT """
# to always get the same results
random.seed(123)
# percentage of test set
test_percentage = 0.02
# get the list of correct id
correct_ids = []


""" For preprocessing """
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
    
    # DEV: to write some of the questions in the test file
    write_test_file = open("test.txt", mode="w", encoding="utf-8")

    questions = []
    for doc in docs_parsed:
        titulo = preprocess_sentence(doc[0])
        for faq in doc[1]:
            # iterate over variations of same faq
            for q in faq[1]:
                ###################################
                #
                #   for developlment :)
                #
                #

                # decide if goes into development set
                if (random.random() < test_percentage):
                    #add question to test file
                    write_test_file.write( re.sub('\n', ' ', q) + "\n")
                    correct_ids.append(faq[0])
                    continue
                
                #
                #
                #  end of for developlment ;)
                #
                ###################################

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
    Compara o query com cada pergunta.
    Retorna o ID da pergunta mais semelhante, usando o TD-IDF.
    Experimentar várias semelhancas antes de escolher a final.
    """
    best_id = 'none'

    sentences = [' '.join(question[0]) for question in questions]
    sentences.append(' '.join(query))
    ids = [question[1] for question in questions]

    # Tf-idf-weighted document-term matrix.
    # one sentences per line, one term per column
    tfidf = TfidfVectorizer().fit_transform(sentences)

    # compute cosine similarity between the query and all other sentences
    vals = cosine_similarity(tfidf[-1], tfidf[:-1])[0]

    # get index of highest similarity
    index = vals.argmax()

    # compute if similarity is significant
    # otherwise, query is not recognized
    if(vals[index] < 0.4):
        best_id = '0'
    else:
        best_id = ids[index]

    # dev ###################################
    print("Best_id \t= "+best_id+"\n")
    # end of dev ############################

    return best_id

def write_results(queries, questions):
    '''
    Get best ID for each query and write in results.txt
    '''
    count_correct = 0

    results_file = open("results.txt", mode="w", encoding="utf-8")
    # dev
    i = 0
    # end of dev
    for query in queries[:-1]:
        id = get_ID(query, questions)
        results_file.write(id+"\n")
        # dev ###################################
        print("Correct_id \t= "+correct_ids[i]+"\n")
        if (id == correct_ids[i]):
            count_correct += 1
        i += 1
        # end of dev #############################
            
    id = get_ID(queries[-1], questions)
    results_file.write(id+"\n")
    
    # dev ###################################
    print("Correct_id \t= "+correct_ids[i]+"\n")
    if (id == correct_ids[i]):
        count_correct += 1
    i += 1
    print("\ntotal queries = ",i)
    print("\n\ncorrect queries = ",count_correct)
    print("\n\nfinal accuracy = {:.2f}\n\n".format(float(count_correct)/float(i)) )
    # end of dev #############################

def main():
#def init_main(xml_file_name, test_file_name):

   ''' get the xml file name and test file name from command line '''
   xml_file_name, test_file_name  = sys.argv[1: ]
   # formato de elemento de questions: [pergunta, id, titulo]
   questions = get_questions(xml_file_name)
   # lista com os queries preprocessados
   queries = get_queries(test_file_name)
   # find best match and print in results.txt
   write_results(queries, questions)


if __name__ == "__main__":
    main()
