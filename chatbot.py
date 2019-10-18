import sys
from utils  import  ID, DOCUMENT, QUESTION, ANSWER,FAQ, TITLE
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
    return ' '.join([get_question(question) for question in faq_obj.getElementsByTagName(QUESTION)]).lower()

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




def main():
   ''' get the xml file name and test file name from command line '''
   xml_file_name,test_file_name  = sys.argv[1: ]

   ''' get the content of all the document in the xml structure '''
   xml_docs = get_documents_xml_file(xml_file_name)
   ''' get the list of all docs, where each doc have content associated [title, [answer_id,questions] ] '''
   docs_parsed = get_all_documents_content(xml_docs)
   ''' print the first 2 documents '''
   print(docs_parsed[:2])

    

if __name__ == "__main__":
    main()
