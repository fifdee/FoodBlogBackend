import sys
import sqlite3
import funcs


def main():
    db_name = 'test4.db'
    if len(sys.argv) > 1:
        db_name = sys.argv[1]

    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('PRAGMA foreign_keys = ON;')

    cur.execute('CREATE TABLE IF NOT EXISTS meals('
                'meal_id INTEGER PRIMARY KEY, meal_name TEXT UNIQUE NOT NULL'
                ');')

    cur.execute('CREATE TABLE IF NOT EXISTS ingredients('
                'ingredient_id INTEGER PRIMARY KEY, ingredient_name TEXT UNIQUE NOT NULL'
                ');')

    cur.execute('CREATE TABLE IF NOT EXISTS measures('
                'measure_id INTEGER PRIMARY KEY, measure_name TEXT UNIQUE'
                ');')

    conn.commit()

    data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
            "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
            "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

    for k, v in data.items():
        for val in v:
            params = (None, val)
            cur.execute(f'INSERT INTO {k} VALUES(?, ?);', params)

    cur.execute('CREATE TABLE IF NOT EXISTS recipes('
                'recipe_id INTEGER PRIMARY KEY,'
                'recipe_name TEXT NOT NULL,'
                'recipe_description TEXT'
                ');')

    conn.commit()

    cur.execute('CREATE TABLE IF NOT EXISTS serve('
                'serve_id INTEGER PRIMARY KEY,'
                'recipe_id INTEGER NOT NULL,'
                'meal_id INTEGER NOT NULL,'
                'FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id),'
                'FOREIGN KEY(meal_id) REFERENCES meals(meal_id)'
                ');')

    cur.execute('CREATE TABLE IF NOT EXISTS quantity('
                'quantity_id INTEGER PRIMARY KEY,'
                'measure_id INTEGER NOT NULL,'
                'ingredient_id INTEGER NOT NULL,'
                'recipe_id INTEGER NOT NULL,'
                'quantity INTEGER NOT NULL,'
                'FOREIGN KEY(measure_id) REFERENCES measures(measure_id),'
                'FOREIGN KEY(ingredient_id) REFERENCES ingredients(ingredient_id),'
                'FOREIGN KEY(recipe_id) REFERENCES recipes(recipe_id)'
                ');')

    conn.commit()

    while True:
        print('What is the recipe name?')
        recipe_name = input()

        if recipe_name == '':
            break

        print('What are the cooking directions?')
        recipe_description = input()

        params = (None, recipe_name, recipe_description)
        cur.execute('INSERT INTO recipes VALUES(?, ?, ?);', params)
        conn.commit()
        last_recipe_id = cur.execute('SELECT * FROM recipes').lastrowid

        result = cur.execute('SELECT meal_id, meal_name FROM meals;')
        meals = result.fetchall()

        for meal in meals:
            print(f'{meal[0]}) {meal[1]}', end='  ')
        print()
        print('When the dish can be served: ')
        when_served = input().split(' ')
        for when in when_served:
            params = (None, last_recipe_id, when)
            cur.execute('INSERT INTO serve VALUES(?, ?, ?);', params)

        while True:
            print('Input quantity of ingredient <press enter to stop>: ', end='')
            quan_ingr = input()
            if quan_ingr == '':
                break
            print()
            quan_ingr = quan_ingr.split(' ')
            if len(quan_ingr) == 2:
                # measure_name is empty string
                quantity = quan_ingr[0]
                measure = ''
                ingredient = quan_ingr[1]
            else:
                quantity = quan_ingr[0]
                measure = quan_ingr[1]
                ingredient = quan_ingr[2]

            measures = cur.execute('SELECT measure_id, measure_name FROM measures;').fetchall()
            measure_id = funcs.measure_check(measure, measures)
            if not ''.__eq__(measure) and not measure_id:
                print('The measure is not conclusive!')
                continue

            ingredients = cur.execute('SELECT ingredient_id, ingredient_name FROM ingredients;').fetchall()
            ingredient_id = funcs.ingredient_check(ingredient, ingredients)
            if not ingredient_id:
                print('The ingredient is not conclusive!')
                continue

            params = (None, measure_id, ingredient_id, last_recipe_id, quantity)
            cur.execute('INSERT INTO quantity VALUES(?, ?, ?, ?, ?);', params)
            conn.commit()

    conn.commit()
    conn.close()
