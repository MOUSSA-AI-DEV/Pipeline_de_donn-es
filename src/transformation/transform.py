import re
from src.database.connection import get_connection


def duration_to_seconds(duration):
    

    if not duration:
        return 0

    hours = re.search(r"(\d+)H", duration)
    minutes = re.search(r"(\d+)M", duration)
    seconds = re.search(r"(\d+)S", duration)

    h = int(hours.group(1)) if hours else 0
    m = int(minutes.group(1)) if minutes else 0
    s = int(seconds.group(1)) if seconds else 0

    return h * 3600 + m * 60 + s


def transform_videos():

    connection = get_connection()
    cursor = connection.cursor()

    # 1. Lire les données depuis Staging
    cursor.execute("""
        SELECT
            video_id,
            title,
            published_at,
            duration,
            views,
            likes,
            comments,
            extracted_at
        FROM staging.youtube_videos;
    """)

    rows = cursor.fetchall()

    transformed_rows = []

    # 2. Transformation
    for row in rows:
# distruction:
        (
            video_id,
            title,
            published_at,
            duration,
            views,
            likes,
            comments,
            extracted_at
        ) = row

        title = title.strip() if title else "Unknown"

        views = views or 0
        likes = likes or 0
        comments = comments or 0

        duration_seconds = duration_to_seconds(duration)

      

        transformed_rows.append((
            video_id,
            title,
            published_at,
            duration_seconds,
            views,
            likes,
            comments,
            extracted_at
        ))

    # 3. Insérer les données transformées dans Core
    for row in transformed_rows:

        cursor.execute("""
            INSERT INTO core.videos (
                video_id,
                title,
                published_at,
                duration_seconds,
                views,
                likes,
                comments,
                extracted_at
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)

            ON CONFLICT (video_id)
            DO UPDATE SET
                title = EXCLUDED.title,
                published_at = EXCLUDED.published_at,
                duration_seconds = EXCLUDED.duration_seconds,
                views = EXCLUDED.views,
                likes = EXCLUDED.likes,
                comments = EXCLUDED.comments,
                extracted_at = EXCLUDED.extracted_at;
        """, row)

    # 4. DELETE  from core if not exist in core 
    cursor.execute("""
        DELETE FROM core.videos
        WHERE NOT EXISTS (
            SELECT 1
            FROM staging.youtube_videos
            WHERE staging.youtube_videos.video_id = core.videos.video_id
        );
    """)

    deleted_rows = cursor.rowcount

    # 4. Valider les INSERT / UPDATE
    connection.commit()

    # 5. Fermer la connexion
    cursor.close()
    connection.close()

    print(f"{len(transformed_rows)} vidéos transformées et chargées dans Core.")


if __name__ == "__main__":
    transform_videos()