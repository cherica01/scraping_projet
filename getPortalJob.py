import requests
from bs4 import BeautifulSoup
import csv
from google.colab import drive
import google.generativeai as genai

genai.configure(api_key="AIzaSyB5-aizL3PkxXwZ-rg46yAHUUuN15u:94sw")
model = genai.GenerativeModel("gemini-1.5-flash")
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
                    titre = offre.find('h4')
                    description = offre.find('a', class_='description')
                    hh3 = offre.find('strong')
                    dateAnnonce = offre.find('aside')
                    dateLimite = offre.find('i', class_="date_lim")

                    # Vérifie si les éléments existent avant d'extraire le texte
                    titre = titre.text.strip() if titre else "Non spécifié"
                    description = description.text.strip() if description else "Non spécifié"
                    hh3 = hh3.text.strip() if hh3 else "Non spécifié"
                    dateAnnonce = dateAnnonce.text.strip() if dateAnnonce else "Non spécifié"
                    dateLimite = dateLimite.text.strip() if dateLimite else "Non spécifié"

                    offre_data = {
                        'poste': hh3,
                        'description': description,
                        'dateAnnonce': dateAnnonce,
                        'entreprise': titre,
                        'dateLimite': dateLimite,
                    }

                    data.append(offre_data)
                except Exception as e:
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

def sauvegarder_en_csv(data, filename="offres_emploi.csv"):
    """Sauvegarde les données dans un fichier CSV."""
    if data:
        # Détermine les noms de colonnes à partir des clés du premier dictionnaire
        colonnes = data[0].keys()

        try:
            # Sauvegarde dans Google Drive
            with open(f'/content/drive/MyDrive/{filename}', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=colonnes)

                # Écrit l'en-tête
                writer.writeheader()

                # Écrit les données
                writer.writerows(data)

            print(f"Les données ont été sauvegardées dans le fichier '{filename}' sur Google Drive.")
        except Exception as e:
            print(f"Erreur lors de l'écriture du fichier CSV: {e}")
    else:
        print("Aucune donnée à sauvegarder.")

# URL de la page à scraper
url = "https://www.portaljob-madagascar.com/emploi/liste"

# Exécute le scraper
resultats = scraper_portaljob(url)
prompt = f"Pouvez vous analyser ce tableau et me dire d'après vous quelle est la compétence qui se répète le plus dans ce tableau{resultats}"
response = model.generate_content(prompt)

# Affiche les résultats
if resultats:
    for offre in resultats:
        print(offre)

    # Sauvegarde les résultats dans un fichier CSV sur Google Drive
    sauvegarder_en_csv(resultats)
else:
    print("Aucune offre d'emploi n'a été trouvée ou une erreur s'est produite.")


print(response.text)
