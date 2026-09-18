import os

# Définir l'hôte sur localhost pour pouvoir se connecter à la base de données 
# en dehors du réseau Docker
os.environ["POSTGRES_HOST"] = "localhost"

from src.extraction.youtube_api import extract_youtube_data
from src.database.load_staging import load_staging
from src.transformation.transform import transform_videos

def run_all():
    print("🚀 Démarrage du pipeline manuel...")
    
    print("\n[1/3] Exécution de l'extraction de l'API YouTube...")
    extract_youtube_data()
    
    print("\n[2/3] Chargement des données dans la base Staging...")
    load_staging()
    
    print("\n[3/3] Transformation des données et chargement dans Core...")
    transform_videos()
    
    print("\n✅ Pipeline terminé avec succès !")

if __name__ == "__main__":
    run_all()
