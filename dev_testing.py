import nltk
from nltk.metrics.scores import accuracy
import xml_parser

def dice_distance(q_train,a_train,a_test,q_test):
    best_answers = []
    for test_q in q_test :
        best = 1
        a_id = 0
        el_index = 0

        for el_index in range(len(q_train)) :
                 
            if set(test_q.split()) != 0 and set(q_train[el_index].split()) :
                res_aux = nltk.jaccard_distance(set(test_q.split()),set(q_train[el_index].split()))
                res_aux = (2*res_aux)/(1 + res_aux)
                if res_aux < best :
                    best = res_aux 
                    a_id = a_train[el_index]
        best_answers.append(a_id)
    print("Accurancy : ", accuracy(a_test, best_answers))

def jaccard_distance(q_train,a_train,a_test,q_test):
    best_answers = []
    for test_q in q_test :
        best = 1
        a_id = 0
        el_index = 0

        for el_index in range(len(q_train)) :
                 
            if set(test_q.split()) != 0 and set(q_train[el_index].split()) :
                res_aux = nltk.jaccard_distance(set(test_q.split()),set(q_train[el_index].split()))
                
                if res_aux < best :
                    best = res_aux 
                    a_id = a_train[el_index]
        best_answers.append(a_id)
    print("Accurancy : ", accuracy(a_test, best_answers))
    

def user_op():
     opcao = -1
     
     while opcao < 0  or opcao > 4 :
         opcao = int(input("Introduza um opcao : "))
     
    
     return opcao
    

def test_algoritm():
    
    result = xml_parser.get_documents_xml_file('KB.xml')
    faqs = xml_parser.get_all_documents_content(result)
    ''' data without stemming '''
    q_train , a_train , q_test , a_test = xml_parser.get_train_test(faqs,False)
    ''' data with stremming '''
    q_train_s , a_train_s , q_test_s , a_test_s = xml_parser.get_train_test(faqs,True)
    
    user_opcao = -1
    while(user_opcao != 0) :
        print("==========   Lista de op algoritmos para testar ================  ")
        print(" Jaccard Distance : Op 1 ")
        print(" Jaccard Distance(with Stemming) : Op 2")
        print(" Dice Distance : Op 3")
        print(" Dice Distance(with Stemming) : Op 4")
        
        print(" Sair : 0")
        
        
        user_opcao = user_op()
        if user_opcao == 0 :
            return  0
        elif user_opcao == 1 :
            jaccard_distance(q_train,a_train,a_test,q_test)
        elif user_opcao == 2 : 
            jaccard_distance(q_train_s,a_train_s,a_test_s,q_test_s)
        elif user_opcao == 3 : 
             dice_distance(q_train,a_train,a_test,q_test)
        elif user_opcao == 4 : 
             dice_distance(q_train_s,a_train_s,a_test_s,q_test_s)
        
test_algoritm()
        