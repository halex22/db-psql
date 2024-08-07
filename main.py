from sqlalchemy import text

from data_population.categories import populate_training

populate_training()

# result = session.execute(text('SELECT now();'))
# for row in result:
#     print(row)

