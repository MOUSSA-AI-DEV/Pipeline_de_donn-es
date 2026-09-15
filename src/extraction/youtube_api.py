import os
from dotenv import load_dotenv
from googleapiclient.discovery import build
import json
from datetime import date
# Load .env
load_dotenv()

# Get API key
API_KEY = os.getenv("YOUTUBE_API_KEY")

# Connect to YouTube API
youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

# ICT channel handle
HANDLE = "@InnerCircleTrader"

# Find the channel using the handle
response = youtube.channels().list(
    part="contentDetails",
    forHandle=HANDLE
).execute()

# Check if channel was found
if not response.get("items"):
    print("Channel not found")
    exit()

# Get channel ID
channel_id = response["items"][0]["id"]

print("Channel ID:", channel_id)

# Get the uploads playlist
uploads_playlist_id = response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

print("Uploads Playlist ID:", uploads_playlist_id)

# Get videos
videos = []
next_page_token = None

while len(videos) < 200:

    request = youtube.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=uploads_playlist_id,
        maxResults=50,
        pageToken=next_page_token
    )

    response = request.execute()

    videos.extend(response["items"])

    next_page_token = response.get("nextPageToken")

    if not next_page_token:
        break

# Garder seulement 200 vidéos
videos = videos[:200]

print("Nombre de vidéos récupérées :", len(videos))
# Get video IDs
video_ids = []

for item in videos:
    video_ids.append(item["contentDetails"]["videoId"])

print("Nombre d'IDs :", len(video_ids))


video_details = []

for i in range(0, len(video_ids), 50):

    batch_ids = video_ids[i:i + 50]

    response = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=",".join(batch_ids)
    ).execute()

    video_details.extend(response["items"])



data = []

for video in video_details:

    snippet = video["snippet"]
    content = video["contentDetails"]
    statistics = video.get("statistics", {})

    video_data = {
        "video_id": video["id"],
        "title": snippet["title"],
        "published_at": snippet["publishedAt"],
        "duration": content["duration"],
        "views": int(statistics.get("viewCount", 0)),
        "likes": int(statistics.get("likeCount", 0)),
        "comments": int(statistics.get("commentCount", 0))
    }

    data.append(video_data)



for item in videos:
    title = item["snippet"]["title"]
    video_id = item["contentDetails"]["videoId"]

    print("Titre :", title)
    print("Video ID :", video_id)
    print("-" * 50)

# Display videos
filename = f"data/YT_data_{date.today()}.json"

with open(filename, "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)

print("JSON créé :", filename)