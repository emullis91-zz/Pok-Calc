This program will calculate the probability of catching any Pokemon given its approximate HP percentage, status effects, and the type of Pokeball used.

Currently plans are to include calculation methods from all generations of the main series, as well as all special Pokeballs included in later main series games. In addition, success/fail simulations will later be implemented to derive the probability of a successful catch. This method, as opposed to implmenting mathematical formulas, will presumably result in slower but more accurate probabilities.

After these steps are implemented a simple GUI will be designed, allowing this program to be used as a web app.

####How to use
At the command line, in the source directory, run CatchProb.py as follows:

`python CatchProb.py <pokemon> <current HP> <max HP> <ball> <status>`

- If a Pokemon with a space in its name is used (e.g. Mr. Mime), enclose the name in single or double quotes.
- If exact HP values are not known, the ideal substitute is to use a number between 1-100 (representing a percentage) and 100 for current and max HP respectively.
- Do not include "ball" at the end of the ball variable (i.e. simply type "poke", "great", "ultra", etc.)
- Status effects must be in present tense ("paralyze", "freeze", "sleep", etc.), or can be left blank if there is no status effect.
- All text variables are case-insensitive.
