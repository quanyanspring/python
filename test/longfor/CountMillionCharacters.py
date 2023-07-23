"""
Get the number of each character in any given text.
Inputs:
A txt file -- You will be asked for an input file. Simply input the name
of the txt file in which you have the desired text.
"""

from collections import Counter
import pprint


def main():
    file_input = input("File name..")
    try:
        with open(file_input, "r") as info:
            counter = Counter(info.read().upper())
    except FileNotFoundError:
        print("Please enter a valid file name.")
        main()

    value = pprint.pformat(counter)
    print(value)
    exit()


if __name__ == "__main__":
    main()
