import requests
from bs4 import BeautifulSoup
import csv

# URL de la page des offres d'emploi
URL = "https://jobmada.zohorecruit.com/jobs/Careers"

# En-têtes HTTP pour simuler un vrai navigateur
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Envoyer une requête GET à Jobmada
response = requests.get(URL, headers=HEADERS)

# Vérifier si la requête a réussi
if response.status_code == 200:
    # Parser le HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Trouver les blocs contenant les offres d'emploi
    job_list = soup.find_all("div", class_="posR")
    print(f"🔍 {len(job_list)} offres d'emploi trouvées sur Jobmada")
    # Liste pour stocker les offres
    jobs = []

    for job in job_list:
        # Récupérer le titre du poste
        title = job.find("h3", class_="job-title").text.strip() if job.find("h3", class_="job-title") else "Non spécifié"

        # Récupérer le nom de l'entreprise
        company = job.find("div", class_="company-name").text.strip() if job.find("div", class_="company-name") else "Non spécifié"

        # Récupérer le lieu
        location = job.find("div", class_="job-location").text.strip() if job.find("div", class_="job-location") else "Non spécifié"

        # Récupérer la date de publication
        date = job.find("div", class_="job-date").text.strip() if job.find("div", class_="job-date") else "Non spécifié"

        # Ajouter les données dans la liste
        jobs.append([title, company, location, date])

    # Enregistrer les offres dans un fichier CSV
    with open("offres_emploi.csv", mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Titre du Poste", "Entreprise", "Lieu", "Date de Publication"])
        writer.writerows(jobs)

    print(f"✅ {len(jobs)} offres d'emploi ont été enregistrées dans 'offres_emploi.csv'")

else:
    print("❌ Erreur lors de la récupération des données. Vérifie l'URL ou ton réseau.")
