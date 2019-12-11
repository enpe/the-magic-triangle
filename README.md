# The Magic Triangle

This project presents a simple solver for an old puzzle published by
[Heye puzzle], which I recently came across. Apparently, the game is
available in different flavors ([triangles][1], [squares][2]).

![Snoopy - The Magic Triangle, Heye](doc/snoopy_the_magic_triangle.jpg)

The version of puzzle used here consists of nine equilateral triangles
with lower and upper parts of figures printed on them. The objective is
to form a large triangle in such a way that the shapes and colors of the
parts of the figures on neighbouring triangles match.

# Approach

The following triangles come with the game:

                    / \                 |                 / \
                   /   \                |                /   \
                  /HO BW\               |               /a   b\
                 /       \              |              /   0   \
                /    HW   \             |             /    c    \
                -----------             |             -----------
              / \    HW   / \           |           / \    c    / \
             /   \       /   \          |          /   \   1   /   \
            /BG HG\BG HG/HO BW\         |         /a   b\b   a/a   b\
           /       \   /       \        |        /   2   \   /   8   \
          /    HO   \ /    BO   \       |       /    c    \ /    c    \
          ----------- -----------       |       ----------- -----------
        / \    BW   / \    HO   / \     |     / \    c    / \    c    / \
       /   \       /   \       /   \    |    /   \   3   /   \   6   /   \
      /BO BG\BG HO/BO HO\BG HG/BW BG\   |   /a   b\b   a/a   b\b   a/a   b\
     /       \   /       \   /       \  |  /   4   \   /   5   \   /   7   \
    /    HO   \ /    BG   \ /    HW   \ | /    c    \ /    c    \ /    c    \
    ----------- ----------- ----------- | ----------- ----------- -----------

    All triangles (cf. the image above)    Indices of the triangles and sides


where

* HO -- head orange
* HG -- head green
* HW -- head white
* BO -- body orange
* BG -- body green
* BW -- body white

The solver uses [backtracking][3] in order to find the solutions. Given
a set containing nine triangles, a total of 362880 permutations exist to
form a large triangle. For each of these (spatial) permutations, every
triangle can be rotated in one of three ways (0, 120, 240 degrees),
which amounts to 19683 possible combinations. That means, all in all
approximately 7.1e9 different possible configurations exist.
Backtracking helps to discard most of these (possible but wrong)
configurations.

When evaluating one of the configurations above, nine pairs of
neighboring triangles are tested. A test is valid if one of the
neighboring triangle has a head of figure printed on it while a body
printed on the other triangle and both are of the same color.

According to the publisher of the game, two solutions exist. The solver
will find six solutions, though. That is because each of the two
solutions can be rotated into three different position.

# Usage

Just run

    $ python ./the_magic_triangle.py deck_of_cards.csv edge_matches.csv

----

For the impatient, the solutions can also be found [here](doc/solutions.txt).

[1]: http://www.google.de/search?q=heye+magische+dreieck&prmd=ivns&source=lnms&tbm=isch
[2]: http://heye-puzzle.de/kategorie/crazy9/
[3]: https://en.wikipedia.org/wiki/Backtracking
[Heye puzzle]: http://heye-puzzle.de
