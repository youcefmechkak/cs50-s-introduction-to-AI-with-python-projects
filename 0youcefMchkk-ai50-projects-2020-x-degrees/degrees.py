import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


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
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
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
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")







def explore (state , exp) :
# a function that checks if a state has been explored

    for ex in exp :
        if ex.state == state :
            return True
    return False



def track_back (n , exp) :
# a function that returns the path from the source actor to the goal actor

    path = list ()


    tmp_n = n
    tmp = tmp_n.parent

    while tmp != None :
        tmp_t = (tmp_n.action, tmp_n.state)
        path.append(tmp_t)

        # search for the node of the parent
        for ex in exp :
            tmp_n = ex

            if tmp == tmp_n.state :
                break
        

        tmp = tmp_n.parent
    
    # reverse the list
    path = path[::-1]

    return path





def shortest_path(source, target):


    explored = list ()

    # store the source in a node
    tmp_source = Node(state = source , parent = None , action = None)

    # add it to the queue
    que = QueueFrontier ()
    que.add (tmp_source)

    while True :
        # if the queue is empty return None
        if que.empty() :
            return None

        # remove a node from the queue and add it to the explored list
        p_node = que.remove()
        explored.append (p_node)

        # explore the neighbors of the node
        neig = neighbors_for_person (p_node.state)
        

        # store each neighbor

        for n in neig :
            # create a node for each neighbor
            tmp_node = Node (state = n[1] ,parent = p_node.state ,action = n[0])

            # if the tmp_node is the target node track back to the source node

            if tmp_node.state == target :
                return track_back (tmp_node , explored)

            # else add it to the queue (but first check if the node is not in explored)
 
            check = explore (tmp_node.state , explored)

            if check == False :
                que.add (tmp_node)


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
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
