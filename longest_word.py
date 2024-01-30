#!/usr/bin/env python3

def longest_word(filename):
    output = ''

    for one_line in open(filename):
        for one_word in one_line.split():
            if len(one_word) > len(output):  # is the current word longer than output?
                output = one_word            # now it has become the longest word

    return output

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find the longest word in a file.')
    parser.add_argument('-f', '--filename', required=True, help='The filename to check')

    args = parser.parse_args()
    filename_to_check = args.filename

    print(longest_word(filename_to_check))
