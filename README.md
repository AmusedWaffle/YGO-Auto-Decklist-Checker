# YGO-Auto-Decklist-Checker
An automatic deck list checker I'm working on in my spare time

For now, this takes as input a simple text file with specific formating.
Example formating:

**********************************
3 Pot of Greed\n
3x Graceful Charity\n
2 Blue-Eyes White Dragon\n
\n
1x Blue-Eyes Ultimate Dragon\n
\n
3x Lightning Storm\n
3x Dark Ruler No More\n
**********************************

It expects:
1. Single newline character in between the main, side, and extra
2. Full name of each card to be typed out
3. Number before each card name

It doesn't care about:
1. Case
2. "x" being after the number