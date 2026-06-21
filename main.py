import csv
import itertools
import os
import time
import pandas as pd
import pylast
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler 
from dotenv import load_dotenv
load_dotenv()

def process_tags(tags_list: list[pylast.TopItem]) -> list[str]:
    target_tags = []
    
    for tag in tags_list:
        # Replace any spaces in the tag names so as to not affect the final cosine matrix 
        name = (tag.item.get_name() or "").replace(" ", "_")

        # int(tag.weight): Converts the weight attribute of the tag object into a whole number.
        # // 10: Performs floor division, dividing the number by 10 and rounding down to the nearest whole integer (e.g., 28 ÷ 10 = 2).
        # max(1, ...): Compares 1 to the divided value and returns the higher number. This prevents the final weight from becoming 0 or negative.
        # If tag.weight is 85: int(85) ÷ 10 = 8. The max(1, 8) evaluates to 8.
        # If tag.weight is 9: int(9) ÷ 10 = 0. The max(1, 0) evaluates to 1.
        weight = max(1, int(tag.weight) // 10)

        print("TAG_NAME/WEIGHT: ", name, "/", weight)

        target_tags.extend([name] * weight)

    return target_tags

def extract_track_info(track:pylast.Track) -> dict[str, str | None]:
    # Ensure track_dict is always defined even if an exception occurs
    track_dict: dict[str, str | None] = dict(track_name=None, track_artist=None, track_tags=None)
    try:
        track_name = track.get_title()
        track_artist_obj = track.get_artist()
        track_artist = track_artist_obj.get_name() if track_artist_obj else ""
            
        
        print("TRACK_OBJ: ",track)
        print("TRACK_NAME: ",track_name)

        print("TRACK_ARTIST_OBJ: ",track_artist_obj)
        print("TRACK_ARTIST: ",track_artist)

        tags_list = process_tags(track.get_top_tags(limit=3))
        print("TARGET_TAGS_LIST: ",tags_list)

        track_dict = dict(track_name=track_name,track_artist=track_artist,track_tags=tags_list)
        print("TRACK_DICT: ",track_dict)
    except Exception as e:
        print("Something went wrong when extracting track data.\nError: ",e)
    
    return track_dict



def main():
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")

    network = pylast.LastFMNetwork(    
        api_key=str(API_KEY),
        api_secret=str(API_SECRET)
    )

    # User input
    user_song_selection = (input('Input a track name to get similar results: ')).rstrip()
    user_artist_selection = (input('Input an artist name for the song: ')).rstrip()

    # Steps:
    # Get user input and search for a track based on the artist name and song name 
    # # Get tags for that specific track
    # 
    # Take the tag weights (represented by 'count' in responses) and multiply each instance of that tag * its flattened weight, add it to a tags list
    # # i.e. if the track has a tag called 'EDM' with a weight of 64, the weight needs to be normalized into an int from 1-10.
    # # # Then the 'EDM' tag is multiplied by the normalized weight. i.e. 'EDM' * 6 = EDM, EDM, EDM, EDM, EDM, EDM
    # # # # Then each tag is added to the tags list 
    # 
    # Turn track into a dictionary with the keys: track_name, track_artist, track_tags
    #
    # Get the baseline tracks for the list 
    # # Turn baseline tracks into dictionaries in the same way
    # 
    # Get similar tracks to the selected track 
    # # Turn similar tracks into dictionaries 
    # 
    # Get similar artists to the selected track's artist
    # # Retrieve the top x number of tracks from each similar artist 
    # # # Turn each track into dictionary 
    # 
    # Add all of the dictionaries together into one big list 
    # # Turn that list of dictionaries into a dataframe  



    try:
        target_track_search = network.search_for_track(user_artist_selection, user_song_selection)
        results = target_track_search.get_next_page()
        target_track = results[0] if results else None
        if not target_track:
            print("Could not find that track on Last.fm.")
            return
        
        target_track_dict = extract_track_info(target_track)

    except Exception as e:
        print(f"Could not find that track on Last.fm. Error: {e}")
        return

    separator = "-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"
    print(separator)

    print("Building music recommendation model based on your selection...")
    

    baseline_tracks_list = []
    baseline_top_tracks = [track.item for track in network.get_top_tracks(limit=3)]
    print("BASELINE_TOP_TRACKS: ", baseline_top_tracks)
    for track in baseline_top_tracks:

        time.sleep(0.2) # Add a delay to avoid hitting API rate limits

        if isinstance(track, pylast.Track):
            baseline_tracks_dict = extract_track_info(track)
            baseline_tracks_list.append(baseline_tracks_dict)


    print("BASELINE_TRACKS_LIST: ", baseline_tracks_list)
    print(separator)

    similar_tracks_list = []
    similar_tracks = [track.item for track in target_track.get_similar(limit=2)]
    print("SIMILAR_TRACKS: ", similar_tracks)
    for track in similar_tracks:

        time.sleep(0.2) 

        if isinstance(track, pylast.Track):
            similar_tracks_dict = extract_track_info(track)
            similar_tracks_list.append(similar_tracks_dict)


    print("SIMILAR_TRACKS_LIST: ", similar_tracks_list)
    print(separator)


    target_artist = target_track.get_artist()

    similar_artist_tracks_list = []
    similar_artists = [artist.item for artist in target_artist.get_similar(limit=1)] if target_artist else []
    print("SIMILAR_ARTISTS: ", similar_artists)
    for artist in similar_artists:

        time.sleep(0.2)

        similar_artist_tracks = [track.item for track in artist.get_top_tracks(limit=1)]
        print("SIMILAR_ARTIST_TRACKS: ", similar_artist_tracks)

        for track in similar_artist_tracks:

            time.sleep(0.2) 

            if isinstance(track, pylast.Track):
                similar_artist_track_dict = extract_track_info(track)
                similar_artist_tracks_list.append(similar_artist_track_dict)


    print("SIMILAR_ARTIST_TRACKS_LIST: ", similar_artist_tracks_list)
    print(separator)

    # Combine all track dictionaries into one list
    all_tracks_list = [target_track_dict] + baseline_tracks_list + similar_tracks_list + similar_artist_tracks_list
    print("ALL_TRACKS_LIST: ", all_tracks_list)

    extracted_data_df = pd.DataFrame(all_tracks_list)
    print("EXTRACTED_DATA_DF: ", extracted_data_df)

    song_characteristics_to_compare = pd.get_dummies(extracted_data_df['track_tags'].apply(pd.Series).stack()).groupby(level=0).sum()
    print("SONG_CHARACTERISTICS_TO_COMPARE: ", song_characteristics_to_compare)

    similarity_matrix = cosine_similarity(song_characteristics_to_compare)
    print(similarity_matrix)

    selected_song_index = 0
    similarity_scores = similarity_matrix[selected_song_index]
    similar_songs = list(enumerate(similarity_scores))
    similar_songs = sorted(similar_songs, key=lambda x: x[1], reverse=True)
    print("SIMILAR_SONGS: ", similar_songs)

    top_recommendations = similar_songs[1:30]
    print(f"If you like: '{target_track_dict['track_name']}' by '{target_track_dict['track_artist']}'")
    print("You might also like: ")
    # Loop through the songs 
    for song_index, similarity_score in top_recommendations:
        recommended_song_row = extracted_data_df.iloc[song_index]
        song_title = recommended_song_row['track_name']
        artist_name = recommended_song_row['track_artist']
        print(f"- {song_title} by {artist_name} (Score: {similarity_score:.2f})")


if __name__ == "__main__":
    main()


