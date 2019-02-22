__author__ = 'Guy'
import pokepy

# client for the api
client = pokepy.V2Client()

# a list of all types
types = ["normal", "fire", "water", "elecric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]

def parse_query(inp):
    """
        A function that translates the input to a list
    """
    return inp.split(" -> ")


def get_num(attacker, defender):
    """
        A function that gets the effectiveness of one type against another using the api
        Input - attacker, defender
        Output - the effectiveness of the attacker agaist the defender
    """


    global client
    type = client.get_type(attacker)[0]
    zero = [x.name for x in type.damage_relations.no_damage_to]

    half = [x.name for x in type.damage_relations.half_damage_to]

    double = [x.name for x in type.damage_relations.double_damage_to]

    if defender in zero:
        return 0
    if defender in half:
        return 0.5
    if defender in double:
        return 2
    return 1


def main():
    while True:
        query = raw_input("Please enter your question in the following format:\nattack_move -> pokemon_name\n")

        try:
            lines = []
            with open("cache.txt", "a+") as cache:
                lines = cache.read().split("\n")
            if query in lines:
                result = lines[lines.index(query) + 1]
                print "found in cache"
                print result
            else:
                attack, pokemon = parse_query(query)
                print attack, pokemon
                tp_pokemon = client.get_pokemon(pokemon)[0].types[0].type.name
                tp_attack = client.get_move(attack)[0].type.name
                print tp_attack, tp_pokemon
                answer = "X" + str(get_num(tp_attack, tp_pokemon))
                print answer
                with open("cache.txt", "a+") as cache:
                    cache.write(query + "\n" + answer + "\n")

        except Exception as e:
            #print e.message
            print "[-] invalid input, please try again."
        print


if __name__ == "__main__":
    main()