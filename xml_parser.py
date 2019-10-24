from utils  import  ID, DOCUMENT, QUESTION, ANSWER,FAQ, TITLE, preproc_aux
from xml.dom import minidom


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

def get_train_test(doc_contents,bool_val):   
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
            questions_len = len(questions_list)
            elems_train = int(.75*(questions_len))
            for index in range(questions_len):
                if index <  elems_train:
                    q_test.append(' '.join(preprocess_sentence(questions_list[index],bool_val)).lower())
                    a_test.append(int(answer_id))
                else :
                    q_train.append(' '.join(preprocess_sentence(questions_list[index],bool_val)).lower())
                    a_train.append(int(answer_id))                  
    return q_train , a_train , q_test , a_test

def get_questions_and_answers(doc_contents):    
    ''' given a list of all the faq in the all the documents
       return a 2 list one with all the questions and other with all the answer id associated 
    '''
    answers = []
    questions = []
    for doc_cont in doc_contents :
        all_faqs = doc_cont[1]
        for faq in all_faqs :
            answer_id = faq[0]
            questions_list = faq[1]
            
            for question in questions_list :
                answers.append(int(answer_id))
                questions.append(question)
    return questions, answers