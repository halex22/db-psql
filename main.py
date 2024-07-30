from sqlalchemy import text

from my_engine import session
from my_engine.engine import DB_NAME

result = session.execute(text('SELECT now();'))
for row in result:
    print(row)

