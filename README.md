# xkcd loader

A simple loader to download all xkcd comics.
Inspired by "Automate the boring stuff" by Al Sweigart.

A few additions and changes where made:
* Variable names where changed to be PEP8 conform
* argparse was added to enable target directory specification
* Major code chunks where structured into functions including a main() module function
* If a file already exists it is not downloaded and written again
