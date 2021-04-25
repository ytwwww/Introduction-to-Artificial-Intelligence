"""This is the main program file for the auto grader program.
The auto grader assumes that the following files are in the same directory as the autograder:
  - autotraining.txt  --> file of tagged words used to train the HMM tagger
  - autotest.txt      --> file of untagged words to be tagged by the HMM
  - autosolution.txt  --> file with correct tags for autotest words
This auto grader generates a file called results.txt that records the test results.
"""
import os
from random import randint, sample


if __name__ == '__main__':
    # # Invoke the shell command to train and test the HMM tagger
    # for _ in range(5):
    #     n = randint(4, 5)
    #     group = sample(range(1, 10), n)
    #     value = group[0]
    #     group = group[1:]
    #     test_name = f"test{value}.txt"
    #     sol_name = f"training{value}.txt"
    #     train_names = ""
    #     for x in group:
    #         train_names += f"training{x}.txt "
    #     print(f"Training on {train_names}, running tests on {test_name}. "
    #           "Output --> autooutput.txt")
    #     os.system(
    #         f"python3 tagger.py -d {train_names} -t {test_name} -o autooutput.txt")

    #     # Compare the contents of the HMM tagger output with the reference solution.
    #     # Store the missed cases and overall stats in results.txt
    #     with open("autooutput.txt", "r") as output_file, \
    #             open(sol_name, "r") as solution_file, \
    #             open("results.txt", "w") as results_file:
    #         # Each word is on a separate line in each file.
    #         output = output_file.readlines()
    #         solution = solution_file.readlines()
    #         total_matches = 0

    #         # generate the report
    #         for index in range(len(output)):
    #             if output[index] != solution[index]:
    #                 pass
    #                 # print(f"Line {index + 1}: "
    #                 #                    f"expected <{output[index].strip()}> "
    #                 #                    f"but got <{solution[index].strip()}>\n")
    #                 # results_file.write(f"Line {index + 1}: "
    #                 #                    f"expected <{output[index].strip()}> "
    #                 #                    f"but got <{solution[index].strip()}>\n")
    #             else:
    #                 total_matches = total_matches + 1

    #         # Add stats at the end of the results file.
    #         # results_file.write(f"Total words seen: {len(output)}.\n")
    #         # results_file.write(f"Total matches: {total_matches}.\n")
    #         # results_file.write(f"{total_matches/len(output)*100}%\n")
    #         print(f"Total words seen: {len(output)}.\nTotal matches: {total_matches}.\n{total_matches/len(output)*100}%\n")

    print("Training on autotraining.txt, running tests on autotest.txt. "
          "Output --> autooutput.txt")
    os.system(
        "python3 tagger.py -d autotraining.txt -t autotest.txt -o autooutput.txt")

    # Compare the contents of the HMM tagger output with the reference solution.
    # Store the missed cases and overall stats in results.txt
    with open("autooutput.txt", "r") as output_file, \
            open("autosolution.txt", "r") as solution_file, \
            open("results.txt", "w") as results_file:
        # Each word is on a separate line in each file.
        output = output_file.readlines()
        solution = solution_file.readlines()
        total_matches = 0

        # generate the report
        for index in range(len(output)):
            if output[index] != solution[index]:
                results_file.write(f"Line {index + 1}: "
                                   f"expected <{output[index].strip()}> "
                                   f"but got <{solution[index].strip()}>\n")
            else:
                total_matches = total_matches + 1

        # Add stats at the end of the results file.
        results_file.write(f"Total words seen: {len(output)}.\n")
        results_file.write(f"Total matches: {total_matches}.\n")
        results_file.write(f"{total_matches/len(output)*100}%\n")
