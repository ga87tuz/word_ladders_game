# word_ladders_game

Word ladders is a word game where a player tries to get from one word, the "start word" to another, the "goal word" in as few steps as possible. In each step, the player must either add one letter to the word from the previous step, or take away one letter, and then rearrange the letters to make a new word.

Here an example:

* Star word: croissant

* Goal word: baritone

* Solution: croissant -> arsonist -> aroints -> notaries -> baritones -> baritone


This is a simple implementation of the game "word ladders" in Python 3.x using the approach of a iterative deepening search algorithm.

It reads in the word list and saves the words depending on their length in different lists (wordLengthList). Then search for possible child nodes by using the wordLengthList and the characters of the currend node names.
