from bottle import *
from requests import get

server_ip = "127.0.0.1"
server_port = 8080

@route("/")
def wrongurl():
    redirect("/auteur")

@route("/pub")
def input():
    return '''
    <h1> Publications et Coauteurs </h1>
    <form action="/pub" method="post">
    Auteur: <input name="s" type="text" />
    <input value="Rechercher Infos" type="submit" />
    </form>
    '''

@route("/auteur")
def input():
    return '''
    <h1> Rechercher Auteur </h1>
    <form action = "/auteur" method="post">
    Rechercher auteur: <input name = "s" type="text" />
    <input value="Rechercher" type="submit" />
    </form>
    '''

@route("/pub", method = 'POST')
def do_input():
    s = request.forms['s']
    publications = get(f"http://{server_ip}:{server_port}/authors/{s}/publications")
    coauthors = get(f"http://{server_ip}:{server_port}/authors/{s}/coauthors")

    return f'''
    <h1> Publications Trouvées </h1>
    <br> </br>
    <h2> {publications.text} </h2>
    <br> </br>
    <h2> {coauthors.text} </h2>
    '''

@route("/auteur", method = 'POST')
def do_input():
    s = request.forms['s']
    auteurs = get(f'http://{server_ip}:{server_port}/search/authors/{s}')

    return f'''
    <h1> Auteurs Trouvés </h1>
    <br> </br>
    <h1> {auteurs.text} </h1>
    '''

run(host='localhost', port = 8081)
