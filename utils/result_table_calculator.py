from copy import copy

from .world_updater import GAME_RESULTS


def calc_game_score_for_mouse(game_result, actions_number, mouse_cheese_score,
                              total_cheese_amount):
    if game_result == GAME_RESULTS['MOUSE_WON']:
        return mouse_cheese_score / (actions_number + 1)
    elif game_result == GAME_RESULTS['CAT_WON']:
        return -1 * (total_cheese_amount - mouse_cheese_score + actions_number / (mouse_cheese_score + 1))
    else:
        return -1 * actions_number / (mouse_cheese_score + 1)


def calc_game_score_for_cat(game_result, actions_number, mouse_cheese_score,
                            max_actions_number):
    if game_result == GAME_RESULTS['CAT_WON']:
        return (max_actions_number - actions_number) / ((mouse_cheese_score + 1) ** 2)
    elif game_result == GAME_RESULTS['MOUSE_WON']:
        return -1 * (mouse_cheese_score ** 2) + mouse_cheese_score * actions_number / max_actions_number
    else:
        return -1 * (mouse_cheese_score ** 2) * actions_number / max_actions_number


def calculate_result_rating(game_results: list, cat_models: list,
                            mouse_models: list, max_actions_number=216, max_cheese_number=9):
    game_results.append([])
    game_results[-1].append('')

    for mouse_index in range(1, len(mouse_models) + 1):
        mouse_score = 0
        for cat_index in range(1, len(cat_models) + 1):
            if mouse_index == cat_index:
                continue
            mouse_score += calc_game_score_for_mouse(
                game_results[mouse_index][cat_index][0],
                game_results[mouse_index][cat_index][1],
                game_results[mouse_index][cat_index][2],
                max_cheese_number
            )
        game_results[mouse_index].append(mouse_score)

    for cat_index in range(1, len(cat_models) + 1):
        cat_score = 0
        for mouse_index in range(1, len(mouse_models) + 1):
            if mouse_index == cat_index:
                continue
            cat_score += calc_game_score_for_cat(
                game_results[mouse_index][cat_index][0],
                game_results[mouse_index][cat_index][1],
                game_results[mouse_index][cat_index][2],
                max_actions_number
            )
        game_results[-1].append(cat_score)


def sort_calculated_results_table(results_table: list):
    # mice sorting
    for i in range(1, len(results_table) - 1):
        for j in range(i + 1, len(results_table) - 1):
            if results_table[i][-1] < results_table[j][-1]:
                temp = results_table[i]
                results_table[i] = copy(results_table[j])
                results_table[j] = copy(temp)

    # cat sorting
    for i in range(1, len(results_table[-1])):
        for j in range(i + 1, len(results_table[-1])):
            if results_table[-1][i] > results_table[-1][j]:
                for k in range(len(results_table)):
                    temp = copy(results_table[k][i])
                    results_table[k][i] = copy(results_table[k][j])
                    results_table[k][j] = temp
