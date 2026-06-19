import csv

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
    
if __name__ == "__main__":
    main()
