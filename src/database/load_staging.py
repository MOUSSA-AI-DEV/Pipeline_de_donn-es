import json
from src.database.connection import get_connection

conn = get_connection()
cursor = conn.cursor()

print("Connexion PostgreSQL réussie !")


# Lire le JSON
with open(
    "data/raw/YT_data_2026-09-14.json",
    "r",
    encoding="utf-8"
) as file:
    videos = json.load(file)

print("Nombre de vidéos :", len(videos))


# Insérer les données dans Staging
for video in videos:

    cursor.execute(
        """
        INSERT INTO staging.youtube_videos (
            video_id,
            title,
            published_at,
            duration,
            views,
            likes,
            comments
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s)

        ON CONFLICT (video_id)
        DO UPDATE SET
            title = EXCLUDED.title,
            views = EXCLUDED.views,
            likes = EXCLUDED.likes,
            comments = EXCLUDED.comments;
        """,
        (
            video["video_id"],
            video["title"],
            video["published_at"],
            video["duration"],
            video["views"],
            video["likes"],
            video["comments"]
        )
    )


conn.commit()

print("Données chargées dans Staging !")


cursor.close()
conn.close()