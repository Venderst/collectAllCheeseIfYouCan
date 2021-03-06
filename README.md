# Collect all cheese if you can

##### Table of Contents  
* [Preparing the workspace](#preparing-the-workspace)
* [Running the program](#running-the-program)
* [Adding a model](#adding-a-model)
* [Models evaluation](#models-evaluation)
* [License](#license)


<a name="preparing-the-workspace"></a>
### Preparing the workspace

Upgrade pip
> Windows:
>```
>\> pip install --upgrade pip
>```

> Linux:
>```
> $ sudo pip install --upgrade pip
>```

Install the required libraries
> Windows:
> ```
>\> pip install -r requirements.txt
> ```

> Linux:
>```
> $ sudo pip install -r requirements.txt
>```

<a name="running-the-program"></a>
### Running the program

>Windows:
>```
>\> python main.py
>```

>Linux:
>```
>$ python3 main.py
>```

<a name="adding-a-model"></a>
### Adding a model
To add a model, follow these steps:
1. Add a .py file to the model directory:

Windows:
```
> type NUL > models\<model_name>.py
```
Linux:
```
$ touch models/<model_name>.py
```

2. Open the created file in a text editor
3. Add next code:
```python
from game_objects import Model, ACTIONS, ENTITIES_STATES
from utils.world_updater import GAME_RESULTS


class YourCatModelName(Model):

    def __init__(self):
        super().__init__()
        # TODO change
        self._name = '<Your cat model displayed name>'

    def act(self, states_map, player_x, player_y):
        """Method responsible for the model action.

        Parameters
        ----------
        states_map : list
            Current state of the field, 2D array.
            Each element represents one of the ENTITIES_STATES values.
        player_x : int
            The player's current position on the X axis.
        player_y : type
            The player's current position on the Y axis.

        Returns
        -------
        tuple
            The direction of the player's movement, one of the ACTIONS values

        """
        # TODO implement
        return ACTIONS['DO_NOTHING']

    def set_game_result(self, game_result):
        """Optional method that is called after each move set the current result of the game.

        Parameters
        ----------
        game_result : int
            Current current score of the game.
            One of the GAME_RESULTS values.
        """
        pass


class YourMouseModelName(Model):

    def __init__(self):
        super().__init__()
        # TODO change
        self._name = '<Your mouse model displayed name>'

    def act(self, states_map, player_x, player_y):
        """Method responsible for the model action.

        Parameters
        ----------
        states_map : list
            Current state of the field, 2D array.
            Each element represents one of the ENTITIES_STATES values.
        player_x : int
            The player's current position on the X axis.
        player_y : type
            The player's current position on the Y axis.

        Returns
        -------
        tuple
            The direction of the player's movement, one of the ACTIONS values

        """
        # TODO implement
        return ACTIONS['DO_NOTHING']

    def set_game_result(self, game_result):
        """Optional method that is called after each move to set the current result of the game.

        Parameters
        ----------
        game_result : int
            Current current score of the game.
            One of the GAME_RESULTS values.
        """
        pass
```
4. For each added model, you must change the (display) name and the act method.
For convenience, the sections where you need to make changes are marked
**"# TODO"**
5. Add your model to *models.yaml*:
>```yaml
>...
><model_file_name>: [<YourCatModelClassName>, <YourMouseModelName>]
>```

<a name="models-evaluation"></a>
### Models evaluation
Mouse:

>Score function for one game:
>
><img src="https://render.githubusercontent.com/render/math?math=game\: score\: for\: mouse = \begin{cases}1 %2B C / N,\: mouse\: won\\-1 %2B C / T,\: cat\: won\\C / T,\: draw\end{cases}">
>
><img src="https://render.githubusercontent.com/render/math?math=N-actions\: number, C - the\: amount\: of\: cheese\: eaten\: by\: the\: mouse, T - total\: cheese">
>
>Code:
>
>```python
>def calc_game_score_for_mouse(game_result, actions_number, mouse_cheese_score, total_cheese_amount):
>   if game_result == GAME_RESULTS['MOUSE_WON']:
>       return 1 + mouse_cheese_score / actions_number
>   elif game_result == GAME_RESULTS['CAT_WON']:
>       return -1 + mouse_cheese_score / total_cheese_amount
>   else:
>       return mouse_cheese_score / total_cheese_amount
>```

>The final score is calculated as the sum of points for each game
>
><img src="https://render.githubusercontent.com/render/math?math=final\ score = \sum_{i=0}^{\vec{|G|}} game\ score\ for\ mouse(G_i)">
>
>Code:

>```python
>def calc_final_mouse_score(games_results):
>	result = 0
>	for i in range(len(game_results)):
>		game_result, actions_number, mouse_cheese_score, total_cheese_amount = game_results[i]
>		result += calc_game_score_for_mouse(game_result, actions_number, mouse_cheese_score, total_cheese_amount)
>	return result
>```

Cat:
>Score function for one game:
>
><img src="https://render.githubusercontent.com/render/math?math=game\: score\: for\: cat = \begin{cases}1 - N / M,\: cat\: won\\-1,\: mouse\: won\\-1 * C / T,\: draw\end{cases}">
>
><img src="https://render.githubusercontent.com/render/math?math=N-actions\: number, C - the\: amount\: of\: cheese\: eaten\: by\: the\: mouse, M - max\: actions\: number, T - total\: cheese">
>
>```python
>def calc_game_score_for_cat(game_result, actions_number, mouse_cheese_score, max_actions_number, total_cheese_amount):
>    if game_result == GAME_RESULTS['CAT_WON']:
>        return 1 - actions_number / max_actions_number
>    elif game_result == GAME_RESULTS['MOUSE_WON']:
>        return -1
>    else:
>        return -1 * mouse_cheese_score / total_cheese_amount
>```

>The final score is calculated as the sum of points for each game
>
><img src="https://render.githubusercontent.com/render/math?math=final\ score = \sum_{i=0}^{\vec{|G|}} game\ score\ for\ cat(G_i)">
>
>Code:

>```python
>def calc_final_cat_score(games_results):
>	result = 0
>	for i in range(len(game_results)):
>		game_result, actions_number, mouse_cheese_score, max_actions_number, total_cheese_amount = game_results[i]
>		result += calc_game_score_for_cat(
>           game_result, actions_number, mouse_cheese_score, max_actions_number, total_cheese_amount
>       )
>	return result
>```

<a name="license"></a>
### License

* [Mozilla Public License 2.0](https://www.mozilla.org/en-US/MPL/2.0/)
* Copyright 2019-2020 © [Venderst](https://github.com/Venderst).
