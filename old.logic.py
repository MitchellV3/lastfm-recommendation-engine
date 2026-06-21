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
        target_track = network.get_track(user_artist_selection, user_song_selection)
        target_track_name = target_track.get_title()
        target_artist = target_track.get_artist()
        
        target_tags_list = target_track.get_top_tags(limit=15)
        target_tags = []
        for tag in target_tags_list:
            name = (tag.item.get_name() or "").replace(" ", "_")
            weight = weight = max(1, int(tag.weight) // 10)
            target_tags.extend([name] * weight)

        baseline_top_tracks= [track for track in network.get_top_tracks(limit=3)]

    except Exception as e:
        print(f"Could not find that track on Last.fm. Error: {e}")
        return
    
    print("Building music recommendation model based on your selection...")
    
    similar_tracks = [track for track in target_track.get_similar()]
    similar_artists = [artist for artist in target_artist.get_similar(limit=3)]
    # 3. Gather raw candidates safely extracting (Artist String, Track String)
    raw_candidates = set()

    similar_artist_tracks = []
    for artist in similar_artists:
        time.sleep(0.5)
        similar_artist_tracks.append(artist.get_top_tracks(limit=1))
    
    unique_candidates = set(baseline_top_tracks + similar_tracks + similar_artist_tracks)
   
    track_tags = []
    for track in unique_candidates:
        track_tags.append(track.get_top_tags(limit=15))

    combined_df = pd.DataFrame[list(unique_candidates), columns=['track_name', 'track_artist', 'track_tags']]

    # Create a minmax scaler to normalize value variance (i.e. tempo 160 vs loudness .8)
    scaler = MinMaxScaler()
    # Create a dataframe with the desired song characteristics to compare
    # Use pd.getdummies to normalize strings like genre and subgenre into numbers 
    song_characteristics_to_compare =  pd.get_dummies(combined_df[['track_tags']])
    # Apply the minmax scaler to the data and fill any N/A values with 0 
    song_characteristics_to_compare = scaler.fit_transform(song_characteristics_to_compare.fillna(0))
    
    # Create the cosine similarity matrix using the normalized dataframe
    similarity_matrix = cosine_similarity(song_characteristics_to_compare)
    print(similarity_matrix)

    print("================================================================================")
    # Find the index for the user's specific song
    selected_song_index = user_song_selection.index[0]
    print(selected_song_index)

    # Create an array of similarity scores by using the similarity matrix with the selected song's index
    similarity_scores = similarity_matrix[selected_song_index]

    # Enumerate the scores into a list of songs paired with their similarity scores
    similar_songs = list(enumerate(similarity_scores))
    # Sort the songs by similarity score
    similar_songs = sorted(similar_songs, key=lambda x: x[1], reverse=True)
    print(similar_songs)
    print("================================================================================")

    # Get the top 30 recommendations 
    top_recommendations = similar_songs[1:30]
    print(f"If you like: '{user_song_selection['track_name'].iloc[0]}' by '{user_song_selection['track_artist'].iloc[0]}'")
    print("You might also like: ")
    # Loop through the songs 
    for song_index, similarity_score in top_recommendations:
        recommended_song_row = combined_df.iloc[song_index]
        song_title = recommended_song_row['track_name']
        artist_name = recommended_song_row['track_artist']
        print(f"- {song_title} by {artist_name} (Score: {similarity_score:.2f})")

if __name__ == "__main__":
    main()
