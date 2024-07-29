from sqlalchemy import text

from engine import session

result = session.execute(text('SELECT now();'))
for row in result:
    print(row)