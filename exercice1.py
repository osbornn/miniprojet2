from bottle import *
from lxml import etree as ET
from re import *

local_input = "dblp.xml"

p = ET.XMLParser(recover=True)
tree = ET.parse(local_input, parser=p)

root = tree.getroot()

testList = [] #cette liste va être utilisée pour renvoyer divers éléments

@route('/publication/<id:int>')
def publication(id):
    """Cette route renvoie une publication de la position indiquée par le paramètre id depuis le fichier xml. Par exemple pour l'id 0, on renvoie la première publication"""
    testList.clear()
    modifiedList = []

    count = request.query.count
    start = request.query.start

    if(not count):
        count = 100
    if(not start):
        start = 0

    for article in root[id]:
        testList.append(article.tag + ": " + article.text + " ")

    if(int(count) > len(testList)):
        count = len(testList)

    for i in range (int(start), int(start) + int(count)):
        modifiedList.append(testList[i])

    return modifiedList

@route('/publication')
def publication():
    """Cette route renvoie par défaut une liste des 100 premières publications du fichier xml. La valeur 100 peut être modifiée par un paramètre limit"""
    testList.clear()
    countPublications = 0

    if(request.query.limit): #si il y a une limite en paramètre celle-ci est prise en compte
        for i in range (0, int(request.query.limit)):
            attributesList = []
            for article in root[i]:
                attributesList.append(article.tag + ": " + str(article.text) + " ")
            testList.append(str(attributesList))

    else:
        for i in range (0,100): #si il n'y a pas de paramètre limite, on retourne les 100 premiers articles
            attributesList = []
            for article in root[i]:
                attributesList.append(article.tag + ": " + str(article.text) + " ")
            testList.append(str(attributesList))

    return testList

@route('/authors/<name>')
def author(name):
    """Cette route retourne le nombre de publications dont l'auteur donné en paramètre est co-auteur, ainsi que son nombre de co-auteurs"""
    testList.clear()
    nbCoauteur = 0
    nbPublications = 0
    for article in root:
        for child in article:
            if(child.tag == "author" and child.text == name):
                authors = article.findall("author")
                if(len(authors) > 1):
                    nbPublications += 1 #on compte le nombre de publications où l'auteur est coauteur
                for i in authors:
                    testList.append(i.text)

    for authorName in testList:
        if(authorName != name):
            nbCoauteur += 1 #on compte le nombre de coauteurs

    return "Nombre de coauteurs : " + str(nbCoauteur) + ", Nombre de publications dont " + name + " est coauteur : " + str(nbPublications)

@route('/authors/<name>/publications')
def author(name):
    """Cette route liste les publications d'un auteur donné en paramètre. Affiche par défaut une liste de 100 éléments mais ceci peut être modifié via les paramètres start et count"""
    testList.clear()
    modifiedList = []

    count = request.query.count
    start = request.query.start

    if(not count):
        count = 100
    if(not start):
        start = 0

    for article in root:
        for child in article:
            if(child.tag == "author" and child.text == name):
                for i in article:
                    if(i.tag == "title"):
                        testList.append(str(i.text) + " ; ")

    if(int(count) > len(testList)):
        count = len(testList)

    for i in range (int(start), int(start) + int(count)):
        modifiedList.append(testList[i])
    return modifiedList

@route('/authors/<name>/coauthors')
def author(name):
    """Cette route liste les co-auteurs d'un auteur donné en paramètre. Retourne par défaut maximum 100 éléments, mais ceci peut être modifié par les paramètres start et count"""
    testList.clear()
    modifiedList = []

    count = request.query.count
    start = request.query.start

    if(not count):
        count = 100
    if(not start):
        start = 0

    for article in root:
        for child in article:
            if(child.tag == "author" and child.text == name):
                authors = article.findall("author")
                for i in authors:
                    if(i.text != name):
                        testList.append(i.text + " ")

    if(int(count) > len(testList)):
        count = len(testList)

    for i in range (int(start), int(start) + int(count)):
        modifiedList.append(testList[i])

    return "Coauthors : " + str(modifiedList)

@route('/search/authors/<searchString>')
def author(searchString):
    """Cette route retourne la liste des auteurs dont le nom contient la chaine de caractères searchString. Retourne par défaut 100 éléments, ceci peut être modifié par les query start et count"""
    testList.clear()
    modifiedList = []

    count = request.query.count
    start = request.query.start

    if(not count):
        count = 100
    if(not start):
        start = 0

    re = compile('%s+'%searchString, flags = IGNORECASE)
    for article in root:
        authors = article.findall("author")
        for i in authors:
            if(re.search(str(i.text))):
                #print(re.search(str(i.text)))
                testList.append(i.text)

    if(int(count) > len(testList)):
        count = len(testList)

    for i in range (int(start), int(start) + int(count)):
        modifiedList.append(testList[i])

    return str(testList)

@route('/search/publications/<searchString>')
def publication(searchString):
    """Cette route retourne la liste des publications (affiche le titre uniquement) dont le titre contient la chaine de caractères searchString. Accepte un paramètre filter pour filtrer la recherche aux paramètres indiqués (par exemple si on veut les publications dont l'auteur a un nom qui commence par la lettre A uniquement)"""
    testList.clear()
    modifiedList = []

    count = request.query.count
    start = request.query.start

    if(not count):
        count = 100
    if(not start):
        start = 0

    filters = request.query.filter
    idfilter = filters.split(',')
    re = compile('%s+'%searchString, flags = IGNORECASE)

    if(not filters):
        for article in root:
            for child in article:
                if(child.tag == "title" and re.search(str(child.text))):
                    testList.append(child.text)
    else:
        for article in root:
            for child in article:
                if(child.tag == "title" and re.search(str(child.text))):
                    counter = 0
                    for f in idfilter:
                        tag = f.split(':')[0]
                        text = f.split(':')[1]
                        #print(text, tag)
                        re2 = compile('%s'%text, flags = IGNORECASE)
                        for a in article:
                            if(a.tag == tag and re2.search(str(a.text))):
                                counter+=1
                    if(counter == len(idfilter)):
                        testList.append(child.text)

    if(int(count) > len(testList)):
        count = len(testList)

    for i in range (int(start), int(start) + int(count)):
        modifiedList.append(testList[i])

    return 'Publications :' + str(modifiedList)

run(host = 'localhost', port = 8080)
