import sqlite3
import texts
from Medcine_bot.texts import product1, product2, product3, product4

connection = sqlite3.connect('database.db')
cursor = connection.cursor()

def initiate_db():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
);
''')
initiate_db()
# cursor.execute('INSERT INTO Products(title, description, price) VALUES(?, ?, ?)', (f'{product1.name}', f'{product1.info}', f'{product1.price}'))
# cursor.execute('INSERT INTO Products(title, description, price) VALUES(?, ?, ?)', (f'{product2.name}', f'{product2.info}', f'{product2.price}'))
# cursor.execute('INSERT INTO Products(title, description, price) VALUES(?, ?, ?)', (f'{product3.name}', f'{product3.info}', f'{product3.price}'))
# cursor.execute('INSERT INTO Products(title, description, price) VALUES(?, ?, ?)', (f'{product4.name}', f'{product4.info}', f'{product4.price}'))
def get_all_products():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products_ = cursor.fetchall()
    connection.close()
    return products_

connection.commit()
connection.close()
