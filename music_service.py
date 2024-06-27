import datetime
import json
import os

class Song:
    def __init__(self, name, artist, duration):
        self.name = name
        self.artist = artist
        self.duration = duration

    def to_dict(self):
        return {
            "name": self.name,
            "artist": self.artist,
            "duration": str(self.duration)
        }

    @classmethod
    def from_dict(cls, data):
        duration = datetime.datetime.strptime(data["duration"], "%H:%M:%S").time()
        duration = datetime.timedelta(hours=duration.hour, minutes=duration.minute, seconds=duration.second)
        return cls(data["name"], data["artist"], duration)

class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []
        self.duration = datetime.timedelta()

    def add_song(self, song):
        self.songs.append(song)
        self.duration += song.duration

    def remove_song(self, song):
        if song in self.songs:
            self.songs.remove(song)
            self.duration -= song.duration

    def to_dict(self):
        return {
            "name": self.name,
            "songs": [song.to_dict() for song in self.songs],
            "duration": str(self.duration)
        }

    @classmethod
    def from_dict(cls, data):
        playlist = cls(data["name"])
        for song_data in data["songs"]:
            playlist.add_song(Song.from_dict(song_data))
        return playlist

class MusicManager:
    def __init__(self, filename="music_manager_data.json"):
        self.songs = []
        self.playlists = []
        self.filename = filename
        self.load_from_file()

    def create_song(self, name, artist, duration):
        song = Song(name, artist, duration)
        self.songs.append(song)
        self.save_to_file()
        return song

    def delete_song(self, song):
        if song in self.songs:
            self.songs.remove(song)
            for playlist in self.playlists:
                playlist.remove_song(song)
            self.save_to_file()

    def create_playlist(self, name):
        playlist = Playlist(name)
        self.playlists.append(playlist)
        self.save_to_file()
        return playlist

    def delete_playlist(self, playlist):
        if playlist in self.playlists:
            self.playlists.remove(playlist)
            self.save_to_file()

    def add_song_to_playlist(self, song, playlist):
        if song in self.songs and playlist in self.playlists:
            playlist.add_song(song)
            self.save_to_file()
            return True
        return False

    def save_to_file(self):
        data = {
            "songs": [song.to_dict() for song in self.songs],
            "playlists": [playlist.to_dict() for playlist in self.playlists]
        }
        with open(self.filename, 'w') as f:
            json.dump(data, f, indent=2)

    def load_from_file(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
            
            self.songs = [Song.from_dict(song_data) for song_data in data["songs"]]
            self.playlists = [Playlist.from_dict(playlist_data) for playlist_data in data["playlists"]]
        else:
            self.songs = []
            self.playlists = []

def print_songs(songs):
    for i, song in enumerate(songs, 1):
        print(f"{i}. {song.name} by {song.artist} ({song.duration})")

def print_playlists(playlists):
    for i, playlist in enumerate(playlists, 1):
        print(f"{i}. {playlist.name} ({len(playlist.songs)} songs, {playlist.duration})")

def main():
    manager = MusicManager()
    print("Welcome to Music Manager!")

    while True:
        print("\n--- Music Manager ---")
        print("1. Create Song")
        print("2. Delete Song")
        print("3. Create Playlist")
        print("4. Delete Playlist")
        print("5. Add Song to Playlist")
        print("6. View Songs")
        print("7. View Playlists")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter song name: ")
            artist = input("Enter artist name: ")
            duration_str = input("Enter duration (MM:SS): ")
            duration = datetime.datetime.strptime(duration_str, "%M:%S").time()
            duration = datetime.timedelta(minutes=duration.minute, seconds=duration.second)
            manager.create_song(name, artist, duration)
            print("Song created successfully.")

        elif choice == '2':
            print_songs(manager.songs)
            index = int(input("Enter the number of the song to delete: ")) - 1
            if 0 <= index < len(manager.songs):
                manager.delete_song(manager.songs[index])
                print("Song deleted successfully.")
            else:
                print("Invalid song number.")

        elif choice == '3':
            name = input("Enter playlist name: ")
            manager.create_playlist(name)
            print("Playlist created successfully.")

        elif choice == '4':
            print_playlists(manager.playlists)
            index = int(input("Enter the number of the playlist to delete: ")) - 1
            if 0 <= index < len(manager.playlists):
                manager.delete_playlist(manager.playlists[index])
                print("Playlist deleted successfully.")
            else:
                print("Invalid playlist number.")

        elif choice == '5':
            print_songs(manager.songs)
            song_index = int(input("Enter the number of the song to add: ")) - 1
            print_playlists(manager.playlists)
            playlist_index = int(input("Enter the number of the playlist to add to: ")) - 1
            if 0 <= song_index < len(manager.songs) and 0 <= playlist_index < len(manager.playlists):
                if manager.add_song_to_playlist(manager.songs[song_index], manager.playlists[playlist_index]):
                    print("Song added to playlist successfully.")
                else:
                    print("Failed to add song to playlist.")
            else:
                print("Invalid song or playlist number.")

        elif choice == '6':
            print_songs(manager.songs)

        elif choice == '7':
            print_playlists(manager.playlists)

        elif choice == '8':
            print("Thank you for using Music Manager. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()