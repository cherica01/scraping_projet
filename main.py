import requests
from bs4 import BeautifulSoup

url = "https://www.portaljob-madagascar.com/"


response = requests.get(url)


if response.status_code == 200:
    # Parser le contenu HTML avec BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.title.string
    print(f"Titre de la page : {title}")

    
    links = soup.find_all("a")
    print("\nListe des liens trouvés :")
    for link in links:
        href = link.get("href")  
        if href:
            print(href)
else:
    print("Erreur lors de la récupération de la page")
