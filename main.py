import csv
import itertools
import pandas as pd

def main():

    fruits = [
        "Apple", 
        "Pear", 
        "Grape",
        "Grapefruit",
        "Cantaloupe",
        "Honeydew",
        "Watermelon",
        "Raspberry",
        "Blackberry",
        "Blueberry",
        "Orange",
        "Nectarine",
        "Peach",
        "Kiwi",
        "Banana",
        "Strawberry",
       ]
    colors = [
        "Red",
        "Green",
        "Green",
        "Yellow",
        "Orange",
        "Green",
        "Red",
        "Red",
        "Black",
        "Blue",
        "Orange",
        "Orange",
        "Orange",
        "Green",
        "Yellow",
        "Red",
    ]

    loud_fruits = [
        fruit.upper() for fruit in fruits 
    ]

    print(fruits)
    print(loud_fruits)
    print(colors)

    fruits_dict =  dict(zip(fruits,colors))
    print(fruits_dict)

    numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    squareNumbers = lambda x, y: x ** y

    for num in numbers: 
        print(squareNumbers(num,num))

    with open("fruits.csv", mode='r', encoding='utf-8') as fruits_file:
        reader = csv.DictReader(fruits_file)
        for row in reader:
            print(row["Fruits"], row["Colors"])
    
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

if __name__ == "__main__":
    main()
