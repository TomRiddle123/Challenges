from PIL import Image
import os


im = Image.open(os.path.join(os.getcwd(), "type_chart.png"))  # the image of the types and effectiveness
rgbim = im.convert('RGB')# rgb instance of the image

# A dictionary that translates between type and its position in the image as a defender and as an attacker
# x for defender and y for attacker
# type: [x, y]

type_and_xy = {
    "normal": [90, 54],
    "fire": [125,98],
    "water": [165,123],
    "elecric": [197, 168],
    "grass": [230, 203],
    "ice": [268, 243],
    "fighting": [306, 277],
    "poison": [350, 314],
    "ground": [381, 352],
    "flying": [419, 384],
    "psychic": [453, 428],
    "bug": [493, 461],
    "rock": [525, 498],
    "ghost": [567, 542],
    "dragon": [606, 576],
    "dark": [642, 612],
    "steel": [678, 651],
    "fairy": [713, 688]
}

# A dictionary that translate between color and effectiveness
# Color: effectiveness
effectiveness_and_color = {
    rgbim.getpixel((560, 51)): 0,
    rgbim.getpixel((152, 95)): 0.5,
    rgbim.getpixel((306, 57)): 1,
    rgbim.getpixel((134, 494)): 2
}


def parse_query(inp):
    """
        A function that parse the input of the user, it returns the attacker and a list of defenders
        Input - the input of the user
        Output - attacker, [defenders]
    """
    at = inp.split(" ")[0]
    df = inp.split("->")[1].replace(" ", "").split(",")
    return at, df

def get_num(at, df):
    """
        A function that return the effectiveness of one type against another
        Input - attacker, defender
        Output - effectiveness of attacker against defender
    """
    # The number that corresponds to the color in rgbim(defender x, attacker y)
    return effectiveness_and_color[rgbim.getpixel((type_and_xy[df][0], type_and_xy[at][1]))]


def main():
    while True:
        query = raw_input("Please enter your question in the following format:\nattack_type -> defense_type1, defense_type2, ...\n")
        tot_ef = 1
        try:
            attacker, defenders = parse_query(query)
            for defender in defenders:
                tot_ef *= get_num(attacker, defender)

            print "X" + str(tot_ef)
        except:
            print "[-] invalid input, please try again."




if __name__ == "__main__":
    main()







































