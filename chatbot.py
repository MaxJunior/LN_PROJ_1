import sys, re
from utils  import  ID, DOCUMENT, QUESTION, ANSWER,FAQ, TITLE
from xml.dom import minidom
from nltk.stem import RSLPStemmer
import nltk.corpus as corpus
from nltk import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer


# stemmer for portuguese words
stemmer = RSLPStemmer()

# list of portuguese stopwords
stopwords = corpus.stopwords.words('portuguese')

def get_documents_xml_file (xml_file_name):
    ''' given a xml file , return all the element
        with tag name "<documento>" 
     '''
    # parse an xml file by name
    xml_content = minidom.parse(xml_file_name)

    return xml_content.getElementsByTagName(DOCUMENT)

def get_faq_content(faq_obj):
    ''' given a faq_obj : object of type <faq> ... </taq>
        returns a string, in a list, obtained by concatenating all questions 
        contained in the faq_obj
    '''
    #return ' '.join([get_question(question) for question in faq_obj.getElementsByTagName(QUESTION)]).lower()
    return [get_question(question) for question in faq_obj.getElementsByTagName(QUESTION)]

def  get_faqs(doc_obj):
    ''' given a doc_obj : <document> type 
        return the list all faq object, <faq> , in the document
    '''
    return doc_obj.getElementsByTagName(FAQ)

def get_answer_id(faq_obj) :
    '''  given a faq : <faq> type
         return the faq answer id
    '''
    return faq_obj.getElementsByTagName(ANSWER)[0].attributes[ID].value

def get_question(question_object):
    ''' question_object : object of type "<pergunta>"  
        return the associated text content 
    '''
    return question_object.firstChild.data

def get_document_content(doc_obj): 
    '''doc_obj : object of type "<documento>" 
       given a document  object of type "documento",return a list where each sub-element is a list1
       list1 : first element answer id and the second element is a list containing
               all the questions associated with the id(first element)            
    '''
    faqs = get_faqs(doc_obj)
    faqs = [ [get_answer_id(faq),get_faq_content(faq)] for  faq  in faqs ]
    
    return faqs

def document_title( doc_obj):
    return doc_obj.getElementsByTagName(TITLE)[0].firstChild.data.lower()


def get_all_documents_content(list_docs_object):
    ''' given a list of <document> xml objects
        return a list  where each element is a 
        list with a document having:
            first element :  document title
            second element : list of all the faq associated with that document        
    '''
    return [ [document_title(doc_obj) , get_document_content(doc_obj)] for  doc_obj  in list_docs_object]

def get_questions(xml_file_name):
    '''
    Importar perguntas para formato a ser processado
    '''

    ''' get the content of all the document in the xml structure '''
    xml_docs = get_documents_xml_file(xml_file_name)
    ''' get the list of all docs, where each doc have content associated [title, [answer_id,questions] ] '''
    docs_parsed = get_all_documents_content(xml_docs)
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



def preproc_aux(l):
    '''
    Funcao retirada do Lab3, do ficheiro DIST.py
     - elimina acentos
     - tudo em minusculas
     - elimina pontuacao
     - fica so com as perguntas
    '''
    # ELIMINA ACENTOS
    l = re.sub(u"ã", 'a', l)
    l = re.sub(u"á", "a", l)
    l = re.sub(u"à", "a", l)
    l = re.sub(u"õ", "o", l)
    l = re.sub(u"ô", "o", l)
    l = re.sub(u"ó", "o", l)
    l = re.sub(u"é", "e", l)
    l = re.sub(u"ê", "e", l)
    l = re.sub(u"í", "i", l)
    l = re.sub(u"ú", "u", l)
    l = re.sub(u"ç", "c", l)
    l = re.sub(u"Ã", 'A', l)
    l = re.sub(u"Á", "A", l)
    l = re.sub(u"À", "A", l)
    l = re.sub(u"Õ", "O", l)
    l = re.sub(u"Ô", "O", l)
    l = re.sub(u"Ô", "O", l)
    l = re.sub(u"Ó", 'O', l)
    l = re.sub(u"Í", "I", l)
    l = re.sub(u"Ú", "U", l)
    l = re.sub(u"Ç", "C", l)
    l = re.sub(u"É", "E", l)
    # TUDO EM MINÚSCULAS
    l = l.lower()
    # ELIMINA PONTUAÇÃO
    l = re.sub("[?|\.|!|:|,|;]", '', l)
    # fica so com as perguntas
    l = re.sub("^\w+\t+[^\w]", '', l)
    return l



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


def main():

   ''' get the xml file name and test file name from command line '''
   xml_file_name, test_file_name  = sys.argv[1: ]

   # lista com os queries preprocessados
   queries = get_queries(test_file_name)

   # formato de elemento de questions: [pergunta, id, titulo]
   questions = get_questions(xml_file_name)

   # find best match and print in results.txt
   write_results(queries, questions)



if __name__ == "__main__":
    main()
