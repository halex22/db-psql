import json

from models.models import GrowthRate
from my_engine import session

INPUT_PATH = './data/categories'


def populate_training():
    traning_path = INPUT_PATH + '/training.json'
    with open(traning_path, mode='r', encoding='utf8') as file:
        data = json.load(file)
    growth_rates = data['growth_rate']
    models = []
    for rate in growth_rates:
        models.append(GrowthRate(name=rate))
    print(models)



if __name__ == '__main__':
    populate_training()

