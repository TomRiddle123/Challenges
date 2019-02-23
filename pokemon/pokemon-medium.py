__author__ = 'Tom Riddle'
import pokepy
# client for the api
client = pokepy.V2Client()

# a list of all types
types = ["normal", "fire", "water", "elecric", "grass", "ice", "fighting", "poison", "ground", "flying", "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]




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


def parse_query(inp):
    """
        A function that parse the input of the user, it returns the attacker and a list of defenders
        Input - the input of the user
        Output - attacker, [defenders]
    """
    at = inp.split(" ")[0]
    df = inp.split("->")[1].replace(" ", "").split(",")
    return at, df


def main():
    while True:
        query = raw_input("Please enter your qustion in the following format:\nattack_type -> defense_type1, defense_type2, ...\n")
        tot_ef = 1
        try:
            attacker, defenders = parse_query(query)
            if attacker not in types:
                raise

            for defender in defenders:
                if defender not in types:
                    raise

                tot_ef *= get_num(attacker, defender)

            print "X" + str(tot_ef)
        except Exception as e:
            print "[-] invalid input, please try again."

        print


if __name__ == "__main__":
    main()