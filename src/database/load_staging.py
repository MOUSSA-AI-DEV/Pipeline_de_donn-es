import json
from datetime import date
from src.database.connection import get_connection
def  load_staging():
    conn = get_connection()
    try:
        cursor = conn.cursor()

        print("Connexion PostgreSQL réussie !")


        # Lire le JSON
        filename = f"data/raw/YT_data_{date.today()}.json"
        with open(
            filename,
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
        pass

    finally:
        conn.close()