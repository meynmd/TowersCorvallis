Files included

- main.py
Contains the main script, arguments parser, and settings object.

- towerState.py
This records the state of the towers of corvallis, and provides handy methods to create towers from files or randomly, as well as necessary output functions.  Also carries the semantics for moving discs, state recognition, and state expansion.

- searchState.py
This file contains the data structure we use when searching.  In particular, we have a TowerState and connect it to estimates of the heuristic, and the search state we had occupied prior to here.  We implement a comparator for this class so that we can sort (for easy beam pruning).

This file also contains our heuristic functions.  The final heuristic functions we reported on were weightedNumDiscsOutOfPlaceAllPeg() (the admissible heuristic) and manhattanDistanceAllPeg() (the inadmissible heuristic)

- searcher.py
Contains 3 functions, BFS, A*, and Beam search.  Each is embedded with some amount of timing and io code, so it may not be as clean looking as we might like.

- unitTests.py
Simply some tests that we built that were useful along the way

- perms-X.txt 
Input files to the program

-timingresults-X.Y.txt
Record of console out from a timing test with specified parameters. X and Y denote the date of file creation.

- solutions-X-yy.txt
Record of console out from a search test with specified parameters.  X denotes the problem size, and yy denotes the search type (aa = admissible A*, hb = inadmissible Heuristic Beam)