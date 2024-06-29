import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}

front = []


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set() #Since there is no row with movies in people.csv, we're using set() to create an empty list of iterables. 
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"]) #Add() adds elements to a set. It turn this int into a list of ints.

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f) # is this what makes python special. It has ready made functions like this that just does everything for you? like reading dictionaries.
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"]) # what does the second [] mean. What is .add
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError: # what is this? I'm guessing the try and except structure is used to prevent errors from doing what to the program?
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]") #.exit allows the program to stop with explaination
    directory = sys.argv[1] if len(sys.argv) == 2 else "large" # arg len starts from python3 but the list starts from filename

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")
    tmp = shortest_path("Tom Hanks", "Tom Holland")
    print(tmp)

front = []
def shortest_path(source, target):
    search_list = neighbors_for_person(person_id_for_name(source))
    for neighbor in search_list:
        #print(neighbor[1] == person_id_for_name(target), people[neighbor[1]]["name"], source)
        if neighbor[1] == person_id_for_name(target): 
            return [people[neighbor[1]]["name"], movies[neighbor[0]]["title"]]
        global front
        front.append(people[neighbor[1]]["name"])  
    new_source = front[0]
    front = front[1:]
    shortest_path(new_source, target) 
    """for i in range(len(front)):
        shortest_path(front[i], target)
        front = front.append(neighbor[1])
    print("no path found",front)
    node = people[frontier[0]]["name"]
    frontier = frontier[1:]
    return [source, target].append(shortest_path(node,target))
    #raise NotImplementedError"""

def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for costar in movies[movie_id]["stars"]:
            if costar != person_id:
                neighbors.add((movie_id, costar))
    return neighbors


if __name__ == "__main__":
    main()
