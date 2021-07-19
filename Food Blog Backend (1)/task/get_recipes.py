import sys
import sqlite3


def main():
    ingr_list = sys.argv[2].replace('--ingredients=', '').split(',')
    meals_list = sys.argv[3].replace('--meals=', '').split(',')

    print(meals_list)
    print(ingr_list)

    conn = sqlite3.connect(sys.argv[1])
    cur = conn.cursor()

    meals_ids = set()
    for meal in meals_list:
        res = cur.execute(f'SELECT meal_id FROM meals '
                          'WHERE meal_name = ?;', (meal,))
        result = res.fetchone()
        if result:
            meals_ids.add(result[0])
    print(f'Meals IDs: {meals_ids}')

    ingrs_ids = set()
    for ingr in ingr_list:
        res = cur.execute('SELECT ingredient_id FROM ingredients '
                          'WHERE ingredient_name = ?;', (ingr,))
        result = res.fetchone()
        if result:
            ingrs_ids.add(result[0])
        else:
            ingrs_ids.add(-1)
    print(f'Ingredients IDs: {ingrs_ids}')

    recipe_ids_from_meals = set()
    for id in meals_ids:
        res = cur.execute('SELECT recipe_id FROM serve '
                          'WHERE meal_id == ?;', (str(id),))
        res_list = [obj[0] for obj in res.fetchall()]
        for obj in res_list:
            recipe_ids_from_meals.add(obj)
    print(recipe_ids_from_meals)

    recipe_ids = {}
    for id in ingrs_ids:
        res = cur.execute('SELECT recipe_id FROM quantity '
                          'WHERE ingredient_id == ?;', (str(id),))
        recipe_ids[id] = [obj[0] for obj in res.fetchall()]
        print(f'recipe_ids[{id}] = {recipe_ids[id]}')
    recipe_ids_filtered = set()
    for id in ingrs_ids:
        if not recipe_ids_filtered:
            recipe_ids_filtered = set(recipe_ids[id])
        else:
            recipe_ids_filtered = recipe_ids_filtered & set(recipe_ids[id])
        print(f'recipe_ids_filtered = {recipe_ids_filtered}')

    recipe_ids_final = recipe_ids_filtered & recipe_ids_from_meals

    recipe_names = set()
    for id in recipe_ids_final:
        res = cur.execute('SELECT recipe_name FROM recipes '
                          'WHERE recipe_id = ?;', (str(id),))
        recipe_names.add(res.fetchone()[0])
    print(recipe_names)

    if len(recipe_names) == 0:
        print('There are no such recipes in the database.')
    else:
        print(f"Recipes selected for you: {', '.join(recipe_names)}")
