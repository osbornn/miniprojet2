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
    testList.clear()
    modifiedList = []

    count = request.query.count
    start = request.query.start

    if(not count):
        count = 100
    if(not start):
        start = 0

    if(request.query.limit): #si il y a une limite en paramètre celle-ci est prise en compte
        for i in range (0, int(request.query.limit)):
            for article in root[i]:
                testList.append(article.tag + ": " + str(article.text) + " ")
    else:
        for i in range (0,99): #si il n'y a pas de paramètre limite, on retourne les 100 premiers articles
            for article in root[i]:
                testList.append(article.tag + ": " + str(article.text) + " ")

    if(int(count) > len(testList)):
        count = len(testList)

    for i in range (int(start), int(start) + int(count)):
        modifiedList.append(testList[i])

    return modifiedList

@route('/authors/<name>')
def author(name):
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
                    testList.append(str(i.tag) + " : " + str(i.text) + " ")

    if(int(count) > len(testList)):
        count = len(testList)

    for i in range (int(start), int(start) + int(count)):
        modifiedList.append(testList[i])
    return modifiedList

@route('/authors/<name>/coauthors')
def author(name):
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
                testList.append(i.text)

    if(int(count) > len(testList)):
        count = len(testList)

    for i in range (int(start), int(start) + int(count)):
        modifiedList.append(testList[i])

    return str(modifiedList)

@route('/search/publications/<searchString>')
def publication(searchString):
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
                        print(text, tag)
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
