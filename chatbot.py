import sys
from utils  import  ID, DOCUMENT, QUESTION, ANSWER,FAQ, TITLE
from xml.dom import minidom
from nltk.stem import RSLPStemmer
import nltk.corpus as corpus
from nltk import word_tokenize
import math


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


#
# PREPROCESSING
#


def preprocess_sentence(sent):
    '''
    Pre-processamento das perguntas:
    - tokenize
    - remover Stop Words
    - Stemming
    '''

    # tokenize
    tokens = word_tokenize(sent)

    # remover stopwords
    tokens = [t for t in tokens if not t in stopwords]

    # stemming
    stem_tokens = [stemmer.stem(t) for t in tokens]

    return stem_tokens


def get_tf(wordDict, bow):
    '''
    get TF score for each word in the document
    '''
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict


def get_idf(docList):
    '''
    get IDF score of every word in the corpus
    '''
    idfDict = {}
    N = len(docList)
    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log10(N/float(val))

    return idfDict

def get_tfidf(tfBow, idfs):
    '''
    get the TF-IDF score for each word, by multiplying the TF and IDF scores
    '''
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return tfidf


def main():

   ''' get the xml file name and test file name from command line '''
   xml_file_name,test_file_name  = sys.argv[1: ]

   ''' get the content of all the document in the xml structure '''
   xml_docs = get_documents_xml_file(xml_file_name)
   ''' get the list of all docs, where each doc have content associated [title, [answer_id,questions] ] '''
   docs_parsed = get_all_documents_content(xml_docs)
   ''' print the first 2 documents '''
   #print(docs_parsed[:2])

   #cont = get_document_content(xml_docs[0])
   
   wordSet = set()

   # formato de elemento de questions: [pergunta, id, titulo]
   questions = []
     
   tfs = []
   tfidfs = []

   for doc in docs_parsed:
       #print("\nTitulo: ",doc[0])
       titulo = preprocess_sentence(doc[0])
       for faq in doc[1]:
           #print("\nTitulo: ",faq[0], "\n\nQuestions:\n")
           # iterate over variations of same faq
           for i, q in enumerate(faq[1]):
               #print(str(i+1)+".",q)
               # preprocessing
               prep = preprocess_sentence(q)
               if prep != []:
                    questions.append([prep,faq[0],titulo])
                    #print(str(i+1)+".",prep,"\n")
                    wordSet = wordSet | set(prep)

   for q in questions:
       wordDict = dict.fromkeys(wordSet, 0) 
       for word in q[0]:
           wordDict[word]+=1

       #print(q[0])
       tfs.append( get_tf(wordDict, q[0]) )

   idfs = get_idf(tfs)

   for i, q in enumerate(questions):
       tfidfs.append(get_tfidf(tfs[i], idfs))
    
   print("DONE")



if __name__ == "__main__":
    main()
