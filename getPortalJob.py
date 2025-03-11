import requests
from bs4 import BeautifulSoup
import csv
from google.colab import drive


def scraper_portaljob(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Trouve le conteneur des offres
        conteneur_offres = soup.find('div', class_='max')

        if conteneur_offres:
            # Trouve les offres individuelles
            offres = conteneur_offres.find_all('article')  # Remplacez 'article' par la balise correcte

            # Initialise une liste pour stocker les données
            data = []

            # Itère sur chaque offre et extrait les informations
            for offre in offres:
                try:
                    titre = offre.find('h4').text.strip() 
                    urgence  = offre.find('div', class_='urgent_flag').text.strip() 
                    description  = offre.find('a', class_='description').text.strip() 
                    hh3  = offre.find('strong').text.strip() 
                    dateAnnonce =  offre.find('aside').text.strip() 

                    offre_data = {
                        'poste': hh3,
                        'description': description,
                        'dateAnnonce': dateAnnonce,
                        'entreprise': titre,
                        'urgence': urgence,
                    }

                    data.append(offre_data)
                except AttributeError as e:
                    print(f"Erreur lors de l'extraction des données d'une offre: {e}")
                    continue

            return data
        else:
            print("Aucun conteneur d'offres trouvé.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête HTTP: {e}")
        return None
    except Exception as e:
        print(f"Une erreur inattendue s'est produite: {e}")
        return None

# URL de la page à scraper
url = "https://www.portaljob-madagascar.com/emploi/liste"

# Exécute le scraper
resultats = scraper_portaljob(url)

# Affiche les résultats
if resultats:
    for offre in resultats:
        print(offre)
else:
    print("Aucune offre d'emploi n'a été trouvée ou une erreur s'est produite.")
