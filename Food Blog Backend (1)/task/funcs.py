def measure_check(input_measure, measure_table):
    measure_choice = None

    for k in measure_table:
        if k[1].startswith(input_measure):
            if not measure_choice:
                measure_choice = k[0]

    return measure_choice


def ingredient_check(input_ingr, ingr_table):
    ingr_choice = None

    for k in ingr_table:
        if k[1].find(input_ingr) != -1:
            if not ingr_choice:
                ingr_choice = k[0]
            else:
                # more than one ingredient includes {ingr}
                return None

    return ingr_choice
