import re

ID =    'id'
FAQ  = 'faq'
QUESTION = 'pergunta'
ANSWER = 'resposta'
DOCUMENT = 'documento'
TITLE  = 'titulo'


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
    l = re.sub("[?|\.|!|:|,|;|\"|\']", '', l)
    l = re.sub("\n", ' ', l)
    # fica so com as perguntas
    l = re.sub("^\w+\t+[^\w]", '', l)
    return l