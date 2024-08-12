from utils import authenticate_spotify, fetch_top_tracks, process_top_tracks, fetch_top_artists, process_top_artists
from database import save_top_tracks, save_top_artists
from logs import logger
scope = "user-top-read"
logger.name = "Main"


def main():
    """
    Authenticates with Spotify, fetches top tracks for different time frames,
    processes the data, and saves each time frame to the database.
    """
    try:
        sp = authenticate_spotify(scope)
        logger.info("Authenticated with Spotify successfully.")
    except Exception as e:
        logger.error(f"Error authenticating with Spotify: {e}")
        return

    # Fetch top tracks and artists
    top_tracks = fetch_top_tracks(sp, limit=50)
    top_artists = fetch_top_artists(sp, limit=50)

    
    # Process and save each time frame individually
    processed_tracks = process_top_tracks(sp, top_tracks)
    processed_artists = process_top_artists(top_artists)

    for time_frame in range(3):
        save_top_tracks(processed_tracks[time_frame])
        save_top_artists(processed_artists[time_frame])


if __name__ == '__main__':
    main()