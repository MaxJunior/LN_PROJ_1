from xml.dom import minidom

ID =    'id'
FAQ  = 'faq'
QUESTION = 'pergunta'
ANSWER = 'resposta'


# parse an xml file by name
mydoc = minidom.parse('KB.xml')
items = mydoc.getElementsByTagName('documento')

def get_faq_content(faq_obj):
    ''' given a faq_obj : object of type <faq> ... </taq>
        returns a string, in a list, obtained by concatenating all questions 
        contained in the faq_obj
    '''
    return ' '.join([get_question(question) for question in faq_obj.getElementsByTagName(QUESTION)])

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

'''
def get_faq_content(faqs_obj):
    return [get_question(question) for question in faqs_obj.getElementsByTagName(QUESTION)]
'''
