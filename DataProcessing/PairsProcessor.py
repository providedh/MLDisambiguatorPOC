import csv
import itertools
import json
from pprint import pprint

from DataRetrieval.Persons import Persons
from DataProcessing.geography import *
from DataProcessing.names import *
from DataProcessing.time import days_apart


def gather_dataset():
    pairs = get_pairs(4)
    dataset = calculate_features(pairs)
    return dataset


def calculate_features(pairs):
    dataset = []
    for pair in pairs:
        sim_vector = [
            levenshtein_distance(pair[0]["title"], pair[1]["title"]),

            ratcliff_obershelp_sim(pair[0]["first_name"], pair[1]["first_name"]),
            phonetics_sim(pair[0]["first_name"], pair[1]["first_name"]),
            levenshtein_distance(pair[0]["first_name"], pair[1]["first_name"]),
            nlp_sim(pair[0]["first_name"], pair[1]["first_name"]),

            ratcliff_obershelp_sim(pair[0]["last_name"], pair[1]["last_name"]),
            phonetics_sim(pair[0]["last_name"], pair[1]["last_name"]),
            levenshtein_distance(pair[0]["last_name"], pair[1]["last_name"]),
            nlp_sim(pair[0]["last_name"], pair[1]["last_name"]),

            pair[0]["name_suffix"] == pair[1]["name_suffix"],
            pair[0]["gender"] == pair[1]["gender"],

            names_to_distance(f"{pair[0]['city']}, {pair[0]['country']}", f"{pair[1]['city']}, {pair[1]['country']}"),

            days_apart(pair[0]['birth_date'], pair[1]['birth_date']),
        ]
        dataset.append((pair, sim_vector))
    return dataset


def get_pairs(n: int):
    persons = Persons().get(n)
    pairs = itertools.combinations(persons, 2)
    return pairs


def dump_pairs(n: int, filename: str = "pairs.json"):
    pairs = get_pairs(n)
    pairs = [[a, b, 0] for a, b in pairs]
    with open(filename, 'w') as F:
        json.dump(pairs, F)


def dump_copies(n: int, filename: str = "pairs.json"):
    people = Persons().get(n)
    people = [[a, a, 1] for a in people]
    with open(filename, 'w') as F:
        json.dump(people, F)


def load_pairs(filename: str = "pairs.json"):
    with open(filename, 'r') as F:
        pairs = json.load(F)

    return pairs


def load_and_calc():
    # positive = load_pairs("../data/positive.json")
    negative = load_pairs("../data/negative.json")

    # pairs = itertools.chain(positive, negative)

    with_features = calculate_features(negative)

    with open("../data/with_features_n.json", 'w') as F:
        json.dump(with_features, F)

    return with_features


if __name__ == "__main__":
    # pprint(gather_dataset())
    # dump_copies(100, "positive.json")
    load_and_calc()
    # dump_pairs(25)
