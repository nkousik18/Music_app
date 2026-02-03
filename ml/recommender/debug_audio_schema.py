from utils import load_songs, load_events

songs = load_songs()
events = load_events()

song_ids = set(songs.track_id)
event_ids = set(events.track_id)

print("Songs:", len(song_ids))
print("Events:", len(event_ids))
print("Intersection:", len(song_ids & event_ids))
