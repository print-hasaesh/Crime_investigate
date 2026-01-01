from collections import Counter

n = int(input("Enter the number of crimes happened: "))

crimes = []
places = []

for i in range(n):
    crime = input(f"Enter crime {i+1}: ").lower()
    place = input(f"Enter place of crime {i+1}: ").lower()  # store in lowercase for uniformity
    crimes.append(crime)
    places.append(place)

crime_count = Counter(crimes)
max_count = max(crime_count.values())

most_repeated_crimes = [crime for crime, count in crime_count.items() if count == max_count]

if max_count == 1:
    print("\nNo crime is repeated.")
    print("All crimes happened in the same ratio:\n")
    for i in range(n):
        print(f"{crimes[i].capitalize()} at {places[i].capitalize()}")
else:
    # Loop 1: Print repeated crime
    print("\nMost repeated crime(s):")
    for crime in most_repeated_crimes:
        print(crime.capitalize())

    # Loop 2: Print number of times it happened
    print("\nNumber of times the crime happened:")
    for crime in most_repeated_crimes:
        print(crime.capitalize(), ":", crime_count[crime])

    # Loop 3: Print places where the repeated crime happened
    print("\nPlace(s) where the repeated crime(s) happened:")
    repeated_places = []
    for crime in most_repeated_crimes:
        for i in range(n):
            if crimes[i] == crime:
                repeated_places.append(places[i])
                print(places[i].capitalize())

    # Loop 4: Print repeated places only
    place_count = Counter(repeated_places)
    repeated_place_only = [place for place, count in place_count.items() if count > 1]
    
    if repeated_place_only:
        print("\nRepeated place(s) for the crime(s):")
        for place in repeated_place_only:
            print(place.capitalize())
