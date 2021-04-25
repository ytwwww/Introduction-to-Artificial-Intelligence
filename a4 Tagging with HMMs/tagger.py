# The tagger.py starter code for CSC384 A4.
# Currently reads in the names of the training files, test file and output file,
# and calls the tagger (which you need to implement)
import os
import sys


def find_most_frequent_tag(tags):
    """find most frequently used tag out of the input list of tags"""
    return max(set(tags), key=tags.count)


def guess_tag(word):
    """guess the tag of a word using grammar, suffixes, or other properties"""
    res = ""
    if len(word) == 1:
        # single alphabet
        if word.isalpha():
            res = "ZZ0"
        # single number
        if word.isdigit():
            res = "CRD"
        # punctuation marks below
        elif word in ["[", "("]:
            res = "PUL"
        elif word in ["]", ")"]:
            res = "PUR"
        elif word in ["\"", "\'"]:
            res = "PUQ"
        else:
            res = "PUN"
    else:
        # proper nouns such as names
        if word[0].isupper():
            res = "NP0"
        # numbers
        elif word[-1].isdigit() or word[0].isdigit():
            if word.startswith("£"):
                res = "NN0"
            else:
                res = "CRD"
        # suffix for verb
        elif word.endswith(("ed")):
            res = "VVD"
        # suffixes for adverbs
        elif word.endswith(("ward", "wise", "ly")):
            res = "AV0"
        # suffixes for nouns
        elif word.endswith(("ness", "ment", "ion", "ity")):
            res = "NN1"
        # suffixes for adjective
        elif word.endswith(("able", "ible", "al", "ful", "ic", "ous", "less", "-like")):
            res = "AJ0"
        # suffix for plural nouns
        elif word[-1] == "s":
            res = "NN2"
        else:
            res = "NN1"
    return res


def tag(training_list, test_file, output_file):
    """Tag the words from the untagged input file and write them into the output file."""
    print("Tagging the file.")

    # read training files and convert to dict with word as key and list of tags as value
    t_dict = dict()
    for train_file in training_list:
        with open(train_file, "r") as train:
            for line in train:
                word, tag = line.rstrip().split(" : ")
                if word in t_dict:
                    t_dict[word] = t_dict[word] + [tag]
                else:
                    t_dict[word] = [tag]

    # read test file and generate output by reading from dict or guessing
    with open(test_file, "r") as test, open(output_file, "w") as output:
        for line in test:
            word = line.rstrip()
            if word in t_dict:
                tags = find_most_frequent_tag(t_dict[word])
            else:
                tags = guess_tag(word)
            output.write(word + " : " + tags + "\n")


if __name__ == '__main__':
    # Run the tagger function.
    print("Starting the tagging process.")

    # Tagger expects the input call: "python3 tagger.py -d <training files> -t <test file> -o <output file>"
    parameters = sys.argv
    training_list = parameters[parameters.index("-d")+1:parameters.index("-t")]
    test_file = parameters[parameters.index("-t")+1]
    output_file = parameters[parameters.index("-o")+1]
    # print("Training files: " + str(training_list))
    # print("Test file: " + test_file)
    # print("Ouptut file: " + output_file)

    # Start the training and tagging operation.
    tag(training_list, test_file, output_file)
