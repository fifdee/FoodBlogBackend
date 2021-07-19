import sys
import provide_recipes
import get_recipes

if len(sys.argv) <= 2:
    provide_recipes.main()
else:
    get_recipes.main()