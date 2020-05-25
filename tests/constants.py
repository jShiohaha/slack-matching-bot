# generate graphs to go with names
from pprint import pprint

# local project imports 
from src.match import *


NAMES = [
    'Alex','Andy','Angel','Ashley','Benny','Bernie',
    'Bertie','Beverley','Billie','Blair','Bobby','Brett',
    'Carol','Casey','Charlie','Cis','Chris','Christian',
    'Clem','Connie','Cory','Courtney','Dale','Danny','Darcy',
    'Daryl','Denny','Dorian','Eddie','Em','Ernie','Fran'
]

NAMES_TWO = [
    'Aaron','Abigail','Adam','Alan','Albert','Alexis',
    'Alice','Amanda','Amber','Amy','Andrea','Andrew',
    'Angela','Ann','Anna','Anthony','Arthur','Ashley',
    'Austin','Barbara','Benjamin','Betty','Bradley',
    'Brandon','Brenda','Brian','Brittany','Bruce','Bryan',
    'Carl','Carolyn','Catherine','Cheryl','Christina',
    'Christine','Christopher','Cynthia','Daniel','Danielle',
    'David','Deborah','Debra','Denise','Dennis','Diana',
    'Diane','Donald','Donna','Doris','Dorothy','Douglas',
    'Dylan','Edward','Elizabeth','Emily','Emma','Eric',
    'Ethan','Eugene','Evelyn','Frances','Frank','Gabriel',
    'Gary','George','Gerald','Gloria','Grace','Gregory',
    'Hannah','Harold','Heather','Helen','Henry','Jack',
    'Jacob','Jacqueline','James','Jane','Janet','Janice'
]

NAMES_THREE = [
    'Jason','Jean','Jeffrey','Jennifer','Jeremy','Jerry',
    'Jesse','Jessica','Joan','Joe','John','Johnny','Jonathan',
    'Jordan','Jose','Joseph','Joshua','Joyce','Juan','Judith',
    'Judy','Julia','Julie','Justin','Karen','Katherine','Kathleen',
    'Kathryn','Kayla','Keith','Kelly','Kenneth','Kevin','Kimberly',
    'Kyle','Larry','Laura','Lauren','Lawrence','Linda','Lisa',
    'Logan','Lori','Louis','Madison','Margaret','Maria','Marie',
    'Marilyn','Mark','Martha','Mary','Matthew','Megan','Melissa',
    'Michael','Michelle','Nancy','Natalie','Nathan','Nicholas',
    'Nicole','Noah','Olivia','Pamela','Patricia','Patrick','Paul',
    'Peter','Philip','Rachel','Ralph','Randy','Raymond','Rebecca',
    'Richard','Robert','Roger','Ronald','Rose','Roy','Russell',
    'Ruth','Ryan','Samantha','Samuel','Sandra','Sara','Sarah',
    'Scott','Sean','Sharon','Shirley','Sophia','Stephanie',
    'Stephen','Steven','Susan','Teresa','Terry','Theresa','Thomas',
    'Timothy','Tyler','Victoria','Vincent','Virginia','Walter',
    'Wayne','William','Willie','Zachary'
]

OTHER_NAME = 'Zedd'

''' DYNAMICALLY GENERATED TESTING VARS '''
generate_n_names = lambda n : [NAMES[i] for i in range(n)]

NO_INDIVIDUALS = list()
ONE_INDIVIDUAL = generate_n_names(1)
TWO_INDIVIDUALS = generate_n_names(2)
THREE_INDIVIDUALS = generate_n_names(3)
FOUR_INDIVIDUALS = generate_n_names(4)
FIVE_INDIVIDUALS = generate_n_names(5)

COMPLETE_GRAPH_TWO_INDIVIDUALS = build_graph(TWO_INDIVIDUALS, graph=None)
COMPLETE_GRAPH_THREE_INDIVIDUALS = build_graph(THREE_INDIVIDUALS, graph=None)
COMPLETE_GRAPH_FOUR_INDIVIDUALS = build_graph(FOUR_INDIVIDUALS, graph=None)
COMPLETE_GRAPH_FIVE_INDIVIDUALS = build_graph(FIVE_INDIVIDUALS, graph=None)

''' STATIC TESTING VARS '''
THREE_MEMBER_ONE_MATCH = { 
    'Alex': [],
    'Andy': [
        'Angel'
    ],
    'Angel': [
        'Andy'
    ]
}

THREE_MEMBER_ONE_MATCH_ALT = { 
    'Alex': [
        'Angel'
    ],
    'Andy': [],
    'Angel': [
        'Andy'
    ]
}

FOUR_MEMBERS_ONE_MATCHES = {
    'Alex': [],
    'Andy': [],
    'Angel': [
        'Ashley'
    ],
    'Ashley': [
        'Angel'
    ]
}

FOUR_MEMBERS_TWO_MATCHES = {
    'Alex': [
        'Andy'
    ],
    'Andy': [
        'Alex',
    ],
    'Angel': [
        'Ashley'
    ],
    'Ashley': [
        'Angel'
    ]
}