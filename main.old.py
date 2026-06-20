import csv
import itertools
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler 

def main():

    #fruits = [
    #    "Apple", 
    #    "Pear", 
    #    "Grape",
    #    "Grapefruit",
    #    "Cantaloupe",
    #    "Honeydew",
    #    "Watermelon",
    #    "Raspberry",
    #    "Blackberry",
    #    "Blueberry",
    #    "Orange",
    #    "Nectarine",
    #    "Peach",
    #    "Kiwi",
    #    "Banana",
    #    "Strawberry",
    #   ]
    #colors = [
    #    "Red",
    #    "Green",
    #    "Green",
    #    "Yellow",
    #    "Orange",
    #    "Green",
    #    "Red",
    #    "Red",
    #    "Black",
    #    "Blue",
    #    "Orange",
    #    "Orange",
    #    "Orange",
    #    "Green",
    #    "Yellow",
    #    "Red",
    #]
#
    #loud_fruits = [
    #    fruit.upper() for fruit in fruits 
    #]
#
    #print(fruits)
    #print(loud_fruits)
    #print(colors)
#
    #fruits_dict =  dict(zip(fruits,colors))
    #print(fruits_dict)
#
    #numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    #squareNumbers = lambda x, y: x ** y
#
    #for num in numbers: 
    #    print(squareNumbers(num,num))
#
    #with open("fruits.csv", mode='r', encoding='utf-8') as fruits_file:
    #    reader = csv.DictReader(fruits_file)
    #    for row in reader:
    #        print(row["Fruits"], row["Colors"])
    
    #with open("spotify_data clean.csv", mode='r', encoding='utf-8') as spotify_data:
    #    reader= csv.DictReader(spotify_data)
    #    print(
    #            'Artist Name',
    #            'Track Name',
    #            'Album Name',
    #            'Artist Genres'
    #            )
    #    for row in itertools.islice(reader, 25):
    #        print(
    #            row['artist_name'],
    #            row['track_name'],
    #            row['album_name'],
    #            row['artist_genres']
    #            )

    # Read csv file
    dataframe = pd.read_csv('spotify_data clean.csv')
    # Create a filtered dataframe
    filtered_dataframe = dataframe[['artist_name','track_name','album_name','artist_genres']].head(25) 
    print(filtered_dataframe)

    # Create a new set from the genres contained within the csv, Sets are always unique
    genres_set = set(dataframe['artist_genres'])
    print(genres_set)

    # Display all rows 
    pd.set_option('display.max_rows', None)

    # Get user input for genre
    choice = input("Enter a genre to filter by: ")
    # Filter dataframe by genres containing user input 
    filtered_by_genre = dataframe[dataframe['artist_genres'].str.contains(choice, case=False, na=False)]
    print(filtered_by_genre[['artist_name','track_name','album_name','artist_genres']])

    # Get user input for sorting
    choice2 = input("Sort by popularity? (yes/no): ")

    # If the user typed 'yes'
    if choice2.lower() == 'yes':
        # Sort by track popularity
        sorted_by_popularity = filtered_by_genre.sort_values(by='track_popularity', ascending=False)
        print(sorted_by_popularity[['track_popularity', 'artist_name','track_name','album_name','artist_genres']])
    else:
        # If user did not type 'yes'
        return
    
    print("================================================================================")

    # Load the CSV files into DataFrames
    df1 = pd.read_csv('high_popularity_spotify_data.csv')
    df2 = pd.read_csv('low_popularity_spotify_data.csv')
    combined_df = pd.concat([df1, df2], ignore_index=True)
    
    # User input
    user_song_selection = (input('Input a track name to get similar results: ')).rstrip()
    user_artist_selection = (input('Input an artist name for the song: ')).rstrip()

    # Get selected artist, then get song from that artist
    user_selected_artist=combined_df[combined_df['track_artist'].str.contains(user_artist_selection,case=False, na=False)]
    user_selected_song=user_selected_artist[user_selected_artist['track_name'].str.contains(user_song_selection,case=False, na=False)].head(1)
    
    print("ARTIST: ", user_selected_artist[['track_artist', 'track_name']])
    print("SONG: ", user_selected_song[['track_artist', 'track_name']])

    # Create a minmax scaler to normalize value variance (i.e. tempo 160 vs loudness .8)
    scaler = MinMaxScaler()
    # Create a dataframe with the desired song characteristics to compare
    # Use pd.getdummies to normalize strings like genre and subgenre into numbers 
    song_characteristics_to_compare =  pd.get_dummies(combined_df[['time_signature', 'speechiness', 'danceability', 'energy', 'playlist_genre', 'playlist_subgenre', 'mode', 'instrumentalness', 'valence', 'key', 'tempo', 'loudness', 'acousticness', 'liveness']], columns=['playlist_genre', 'playlist_subgenre'])

    # Apply the minmax scaler to the data and fill any N/A values with 0 
    song_characteristics_to_compare = scaler.fit_transform(song_characteristics_to_compare.fillna(0))
    
    # Create the cosine similarity matrix using the normalized dataframe
    similarity_matrix = cosine_similarity(song_characteristics_to_compare)
    print(similarity_matrix)

    print("================================================================================")
    # Find the index for the user's specific song
    selected_song_index = user_selected_song.index[0]
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
    print(f"If you like: '{user_selected_song['track_name'].iloc[0]}' by '{user_selected_song['track_artist'].iloc[0]}'")
    print("You might also like: ")
    # Loop through the songs 
    for song_index, similarity_score in top_recommendations:
        recommended_song_row = combined_df.iloc[song_index]
        song_title = recommended_song_row['track_name']
        artist_name = recommended_song_row['track_artist']
        print(f"- {song_title} by {artist_name} (Score: {similarity_score:.2f})")

if __name__ == "__main__":
    main()
