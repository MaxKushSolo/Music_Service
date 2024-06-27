import pytest
import datetime
from music_service import Song, Playlist, MusicManager

@pytest.fixture
def sample_song():
    return Song("Test Song", "Test Artist", datetime.timedelta(minutes=3, seconds=30))

@pytest.fixture
def sample_playlist():
    return Playlist("Test Playlist")

@pytest.fixture
def music_manager(tmp_path):
    return MusicManager(filename=str(tmp_path / "test_music_manager_data.json"))

def test_song_creation(sample_song):
    assert sample_song.name == "Test Song"
    assert sample_song.artist == "Test Artist"
    assert sample_song.duration == datetime.timedelta(minutes=3, seconds=30)

def test_song_to_dict(sample_song):
    song_dict = sample_song.to_dict()
    assert song_dict == {
        "name": "Test Song",
        "artist": "Test Artist",
        "duration": "0:03:30"
    }

def test_song_from_dict():
    song_dict = {
        "name": "Dict Song",
        "artist": "Dict Artist",
        "duration": "0:04:15"
    }
    song = Song.from_dict(song_dict)
    assert song.name == "Dict Song"
    assert song.artist == "Dict Artist"
    assert song.duration == datetime.timedelta(minutes=4, seconds=15)

def test_playlist_creation(sample_playlist):
    assert sample_playlist.name == "Test Playlist"
    assert len(sample_playlist.songs) == 0
    assert sample_playlist.duration == datetime.timedelta()

def test_playlist_add_remove_song(sample_playlist, sample_song):
    sample_playlist.add_song(sample_song)
    assert len(sample_playlist.songs) == 1
    assert sample_playlist.duration == sample_song.duration

    sample_playlist.remove_song(sample_song)
    assert len(sample_playlist.songs) == 0
    assert sample_playlist.duration == datetime.timedelta()

def test_playlist_to_dict(sample_playlist, sample_song):
    sample_playlist.add_song(sample_song)
    playlist_dict = sample_playlist.to_dict()
    assert playlist_dict == {
        "name": "Test Playlist",
        "songs": [sample_song.to_dict()],
        "duration": "0:03:30"
    }

def test_playlist_from_dict():
    playlist_dict = {
        "name": "Dict Playlist",
        "songs": [
            {
                "name": "Dict Song",
                "artist": "Dict Artist",
                "duration": "0:04:15"
            }
        ],
        "duration": "0:04:15"
    }
    playlist = Playlist.from_dict(playlist_dict)
    assert playlist.name == "Dict Playlist"
    assert len(playlist.songs) == 1
    assert playlist.songs[0].name == "Dict Song"
    assert playlist.duration == datetime.timedelta(minutes=4, seconds=15)

def test_music_manager_create_song(music_manager):
    song = music_manager.create_song("New Song", "New Artist", datetime.timedelta(minutes=2, seconds=45))
    assert len(music_manager.songs) == 1
    assert song in music_manager.songs

def test_music_manager_delete_song(music_manager):
    song = music_manager.create_song("Delete Song", "Delete Artist", datetime.timedelta(minutes=1, seconds=30))
    assert len(music_manager.songs) == 1
    music_manager.delete_song(song)
    assert len(music_manager.songs) == 0

def test_music_manager_create_playlist(music_manager):
    playlist = music_manager.create_playlist("New Playlist")
    assert len(music_manager.playlists) == 1
    assert playlist in music_manager.playlists

def test_music_manager_delete_playlist(music_manager):
    playlist = music_manager.create_playlist("Delete Playlist")
    assert len(music_manager.playlists) == 1
    music_manager.delete_playlist(playlist)
    assert len(music_manager.playlists) == 0

def test_music_manager_add_song_to_playlist(music_manager):
    song = music_manager.create_song("Playlist Song", "Playlist Artist", datetime.timedelta(minutes=3, seconds=15))
    playlist = music_manager.create_playlist("Test Playlist")
    assert music_manager.add_song_to_playlist(song, playlist)
    assert song in playlist.songs

def test_music_manager_save_load(music_manager):
    song = music_manager.create_song("Save Song", "Save Artist", datetime.timedelta(minutes=2, seconds=30))
    playlist = music_manager.create_playlist("Save Playlist")
    music_manager.add_song_to_playlist(song, playlist)

    # Create a new MusicManager instance with the same filename to test loading
    new_manager = MusicManager(filename=music_manager.filename)
    assert len(new_manager.songs) == 1
    assert len(new_manager.playlists) == 1
    assert new_manager.songs[0].name == "Save Song"
    assert new_manager.playlists[0].name == "Save Playlist"
    assert new_manager.playlists[0].songs[0].name == "Save Song"