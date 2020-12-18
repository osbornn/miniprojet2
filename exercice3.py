from bottle import *
from requests import get

server_ip = "127.0.0.1"
server_port = 8080

@route("/input")
def input():
    return '''
    <form action="/input" method="post">
    Auteur: <input name="s" type="text" />
    <input value="Rechercher" type="submit" />
    Rechercher un auteur: <input name="s2" type="text"/>
    <input value="Rechercher" type="submit" />
    </form>
    '''

@route("/input", method = 'POST')
def do_input():
    s = request.forms['s']
    publications = get(f"http://{server_ip}:{server_port}/authors/{s}/publications")
    coauthors = get(f"http://{server_ip}:{server_port}/authors/{s}/coauthors")

    return f'''
    <h2> Publications : {publications.text} </h2>
    <br> </br>
    <h2> {coauthors.text} </h2>
    '''


run(host='localhost', port = 8081)
