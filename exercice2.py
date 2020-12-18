from requests import *
import unittest

class TestAPIMethods(unittest.TestCase):
    server_ip, server_port = '127.0.0.1', 8080

    def test_publication_id(self):
        r = get(f"http://{self.server_ip}:{self.server_port}/publication/0")
        self.assertIn('Louise A. Dennis', r.text)

    def test_publication(self):
        r = get(f'http://{self.server_ip}:{self.server_port}/publication?limit=10')
        list = r.text.split('][') #on obtient une liste de chaque article à partir du get qui nous renvoie uniquement un string
        self.assertEqual(len(list), 10)

    def test_author(self):
        r = get(f'http://{self.server_ip}:{self.server_port}/authors/Louise A. Dennis')
        list = r.text.split(',') #même chose qu'à la fonction précédente, on obtient une liste avec d'un côté le nombre de coauteurs, de l'autre le nombre de publications dont l'auteur est coauteur
        coauteurs = list[0].split(' : ')[1]
        publications = list[1].split(' : ')[1]

        self.assertEqual(int(coauteurs), 4)
        self.assertEqual(int(publications), 3)

    def test_author_publications(self):
        r = get(f'http://{self.server_ip}:{self.server_port}/authors/Louise A. Dennis/publications')
        self.assertIn('Verifiable Self-Aware Agent-Based Autonomous Systems.', r.text)

    def test_author_coauthors(self):
        r = get(f'http://{self.server_ip}:{self.server_port}/authors/Louise A. Dennis/coauthors')
        self.assertIn('Peter Stringer', r.text)

    def test_author_searchstring(self):
        r = get(f'http://{self.server_ip}:{self.server_port}/search/authors/Lou')
        self.assertIn('Dong Lou', r.text)

    def test_publications_searchstring(self):
        r = get(f'http://{self.server_ip}:{self.server_port}/search/publications/mo?filter=author:Louise A. Dennis')
        self.assertIn('Verifiable Self-Aware Agent-Based Autonomous Systems.', r.text)


if __name__ == '__main__':
    unittest.main()
