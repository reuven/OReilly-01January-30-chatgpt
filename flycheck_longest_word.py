def longest_word(filename):
    output = ''

    for one_line in open(filename):
        for one_word in one_line.split():
            if len(one_word) > len(output):  # is the current word longer than output?
                output = one_word            # now it has become the longest word

    return output
