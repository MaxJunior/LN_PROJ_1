import nltk
from nltk.metrics.scores import accuracy
import xml_parser
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

def dice_distance_m(label1, label2):
    """Distance metric comparing set-similarity """
    return 2 *(len(label1.union(label2)) - len(label1.intersection(label2))) / (len(label1) + len(label2))

def dice_distance(data):
    q_train,a_train,q_test,a_test = data
    best_answers = []
    for test_q in q_test :
        best = 1
        a_id = 0
        el_index = 0

        for el_index in range(len(q_train)) :
                 
            if set(test_q.split()) != 0 and set(q_train[el_index].split()) :
                res_aux = dice_distance_m(set(test_q.split()),set(q_train[el_index].split()))
                
                if res_aux < best :
                    best = res_aux 
                    a_id = a_train[el_index]
        best_answers.append(a_id)
    #print("Accuracy : ", accuracy(a_test, best_answers))
    return accuracy(a_test, best_answers)

def jaccard_distance(data):
    q_train,a_train,q_test,a_test = data
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
 
    return  accuracy(a_test, best_answers)

def tfidf_cosine(data):
    q_train,a_train,q_test,a_test = data
    best_answers = []
    sentences = q_train[:]
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
            best_answers.append('0')
        else:
            best_answers.append(a_train[a_id])

        sentences = sentences[:-1]

    #print("Accuracy : ", accuracy(a_test, best_answers))
    return accuracy(a_test, best_answers)
    

def user_op():
     opcao = -1
     
     while opcao < 0  or opcao > 12 :
         opcao = int(input("Introduza um opcao : "))
     
    
     return opcao
    

def test_algoritm():
    
    result = xml_parser.get_documents_xml_file('KB.xml')
    faqs = xml_parser.get_all_documents_content(result)
    ''' data without stemming and removing stopwords'''
    #q_train_w , a_train_w , q_test_w , a_test_w = xml_parser.get_train_test(faqs,True,False)
    data_w = xml_parser.get_train_test(faqs,True,False)
    ''' data with stremming and removing stopwords'''
    #q_train_s_w , a_train_s_w , q_test_s_w , a_test_s_w = xml_parser.get_train_test(faqs,True,True)
    data_s_w = xml_parser.get_train_test(faqs,True,True)
    ''' data without stemming and keeping stopwords'''
    #q_train , a_train , q_test , a_test = xml_parser.get_train_test(faqs,False,False)
    data = xml_parser.get_train_test(faqs,False,False)
    ''' data with stremming and keeping stopwords'''
    #q_train_s , a_train_s , q_test_s , a_test_s = xml_parser.get_train_test(faqs,False,True)
    data_s = xml_parser.get_train_test(faqs,False,True)
    
    user_opcao = -1
    while(user_opcao != 0) :
        print("==========   Lista de op algoritmos para testar ================  ")
        print(" Jaccard Distance : Op 1 ")
        print(" Jaccard Distance (with Stemming) : Op 2")
        print(" Dice Distance : Op 3")
        print(" Dice Distance (with Stemming) : Op 4")
        print(" TF-IDF and Cosine Similarity : Op 5")
        print(" TF-IDF and Cosine Similarity (with Stemming) : Op 6")
        print(" Jaccard Distance (with no Stopwords): Op 7 ")
        print(" Jaccard Distance (with Stemming and no Stopwords) : Op 8")
        print(" Dice Distance (with no Stopwords): Op 9")
        print(" Dice Distance (with Stemming and no Stopwords) : Op 10")
        print(" TF-IDF and Cosine Similarity (with no Stopwords): Op 11")
        print(" TF-IDF and Cosine Similarity (with Stemming and no Stopwords) : Op 12")
        
        print(" Sair : 0")
        
        
        user_opcao = user_op()
        if user_opcao == 0 :
            return  0
        elif user_opcao == 1 :
            #print("Accuracy : ",jaccard_distance(q_train,a_train,q_test,a_test))
            print("Accuracy : ",jaccard_distance(data))
        elif user_opcao == 2 : 
            print("Accuracy : ",jaccard_distance(data_s))
        elif user_opcao == 3 : 
            print("Accuracy : ",dice_distance(data))
        elif user_opcao == 4 : 
            print("Accuracy : ",dice_distance(data_s))
        elif user_opcao == 5 : 
            print("Accuracy : ",tfidf_cosine(data))
        elif user_opcao == 6 :
            print("Accuracy : ",tfidf_cosine(data_s))
        elif user_opcao == 7 :
            print("Accuracy : ",jaccard_distance(data_w))
        elif user_opcao == 8 : 
            print("Accuracy : ",jaccard_distance(data_s_w))
        elif user_opcao == 9 : 
            print("Accuracy : ",dice_distance(data_w))
        elif user_opcao == 10 : 
            print("Accuracy : ",dice_distance(data_s_w))
        elif user_opcao == 11 : 
            print("Accuracy : ",tfidf_cosine(data_w))
        elif user_opcao == 12 :
            print("Accuracy : ",tfidf_cosine(data_s_w))
        
#test_algoritm()
 





def get_average_accuracy():
    result = xml_parser.get_documents_xml_file('KB.xml')
    faqs = xml_parser.get_all_documents_content(result)
    print("\nJaccard Distance\n")
    results = [ jaccard_distance(xml_parser.get_train_test(faqs,False,False)) for _ in range(10) ]# a,b,c,d = xml_parser.get_train_test(faqs,False,False)]
    print(results)
    print("\nAverage Accuracy : ", sum(results)/10,"\n")
    
    results = []

get_average_accuracy()

get_average_accuracy()

"""
def av_acc(metric, faqs, noStop, Stem):
    results = []
    for _ in range(10):
        data = xml_parser.get_train_test(faqs,noStop,Stem)
        acc = metric(data)
        print(" Accuracy : {:.4f}".format(acc))
        results.append(acc)
    print("\nAverage Accuracy : {:.4f} \n".format( sum(results)/10))
    return sum(results)/10

def get_all_av_acc():

    funcs = [jaccard_distance, dice_distance, tfidf_cosine]
    names = ['jaccard_distance', 'dice_distance', 'tfidf_cosine']

    result = xml_parser.get_documents_xml_file('KB.xml')
    faqs = xml_parser.get_all_documents_content(result)

    for noStop in [False, True]:
        for Stem in [False, True]:
            for i, metric in enumerate(funcs):
                print("\n"+names[i]+"\tnoStop =",noStop,"\tStem=",Stem,"\n")
                av_acc(metric, faqs, noStop, Stem)

get_all_av_acc()
"""