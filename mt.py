import random
import sys
import os

class MT:
    work = {"0", "1", "_", "#"}

    def __init__(self, name, states, i, f, transitions, k, identifier):
        """create a new turing machine"""
        self.name = name
        self.alpha = {"0", "1", "#"}
        self.work = {"0", "1", "_", "#"}
        self.states = states
        self.init = i
        self.accept = f
        self.transitions = transitions
        self.current = i
        self.bands = [[] for _ in range(k)]
        self.heads = [0] * k
        self.k = k
        self.identifier = identifier

    def __str__(self):
        """display the configuration of the machine"""
        print(f"\nname: ", self.name)
        print("alphabet: ", self.alpha)
        print("work alphabet: ", self.work)
        print("states: ", self.states)
        print("init: ", self.init)
        print("accept: ", self.accept)
        print("current state: ", self.current)
        print("number of bands: ", self.k)
        print("heads: ", self.heads)
        print("\nbands:")
        for band in self.bands: print(band)
        print("\ntransitions:")
        for key, content in self.transitions.items():
            print(key)
            print(",".join(content))
            print()
        return ""

    def reset(self):
        """reset the machine to its initial state"""
        self.current = self.init
        self.bands = [[] for _ in range(self.k)]
        self.heads = [0] * self.k

    def set_word(self, word):
        """set a word to the first band of the machine"""
        self.bands[0] = list(word)

    def step(self):
        """execute a step"""
        key = self.current
        for j in range(len(self.bands)):
            key += ","
            if 0 <= self.heads[j] < len(self.bands[j]):
                key += self.bands[j][self.heads[j]]
            else:
                key += "_"

        if key in self.transitions:
            transition = self.transitions[key]
            self.current = transition[0]
            for j in range(self.k):
                if 0 <= self.heads[j] < len(self.bands[j]):
                    self.bands[j][self.heads[j]] = transition[j + 1]
                elif self.heads[j] == -1:
                    self.bands[j] = list(transition[j + 1]) + self.bands[j]
                    self.heads[j] = 0
                elif self.heads[j] == len(self.bands[j]):
                    self.bands[j] += transition[j + 1]

                move = transition[self.k + 1 + j]
                if move == "<":
                    self.heads[j] -= 1
                elif move == ">":
                    self.heads[j] += 1
        else:
            self.current = "reject"

    def execute(self):
        """execute the machine until it accepts or rejects"""
        while self.current not in ["reject", self.accept]:
            self.step()
        return self.current


def is_normal_transition(transition):
    """check if the given transition is normal"""
    for item in transition[1:]:
        if item not in MT.work:
            return False
    else:
        return True


def to_second(item, identifier):
    """add identifier to the state to make it unique"""
    content = item.split(",")
    content[0] += identifier
    return ",".join(content)


def mt_from_file(file_path):
    """return the turing maching if file exists"""
    try:
        return read_file(file_path)
    except Exception:
        print(f"No such file: {file_path}")
        exit(2)


def read_file(file_path):
    """create a MT object from a file"""
    with open(file_path) as file:

        line_1 = True
        states = []
        transitions = {}
        identifier ="'"
        name = None
        i = None
        f = None
        k = None

        for idx, line in enumerate(file.readlines()):
            line = line.strip()

            # empty line
            if not line:
                continue
            # comment line
            elif line.startswith("//"):
                continue
            # keep non comment part
            elif "//" in line:
                line = line.split("//")[0]

            line = line.replace(" ", "")
            if line_1:
                # get name
                if line.startswith("name:"):
                    name = line[5:].strip()

                # get initial state
                elif line.startswith("init:"):
                    if "," in line:
                        print("error in init")
                        print(line)
                        exit(3)
                    else:
                        i = line[5:].strip()

                # get final state
                elif line.startswith("accept:"):
                    if "," in line:
                        print("error in accept")
                        print(line)
                        exit(4)
                    else:
                        f = line[7:].strip()

                # first line of transitions
                else:
                    elements = line.split(",")

                    if is_normal_transition(elements):
                        if k == None:
                            k = len(elements) - 1
                        elif k != len(elements) - 1:
                            print(file_path)
                            print(f"wrong number of bands at line {idx}, should be {k}")
                            print(line)
                            exit(5)
                        line_1 = False
                        if elements[0] not in states:
                            states.append(elements[0])
                        key = line
                    else:
                        if k == None:
                            k = len(elements) - 3
                        elif k != len(elements) - 3:
                            print(file_path)
                            print(f"wrong number of bands at line {idx}, should be {k}")
                            print(line)
                            exit(6)
                        try:
                            second_machine = read_file(elements[-2])

                        except Exception as e:
                            print(f"No such file {elements[-2]} at line {idx}")
                            print(e)
                            exit(7)
                        key = ",".join(elements[:-2])
                        transitions[key] = [second_machine.init+identifier] + elements[1:-2] + ["-"]*k
                        for key, transition in second_machine.transitions.items():
                            key = to_second(key, identifier)
                            if transition[0] == second_machine.accept:
                                transition[0] = elements[-1]
                            else:
                                transition[0] += identifier
                            transitions[key] = transition
                        identifier += second_machine.identifier

            # deuxieme ligne
            else:
                elements = line.split(",")
                if (len(elements) - 1) / 2 - k == 0:
                    transitions[key] = line.split(",")
                    line_1 = True
                    if elements[0] not in states:
                        states.append(elements[0])
                else:
                    print(file_path)
                    print(f"wrong number of bands at line {idx+1}")
                    print(line)
                    exit(8)

        if name is None:
            name = file_path
        elif i is None:
            print("'init:' is missing")
            exit(9)
        elif f is None:
            print("'accept:' is missing")
            exit(10)

        return MT(name, states, i, f, transitions, k, identifier)

def unittest_mul_egypt():
    """test the multiplication of the question 7 with random numbers"""
    mt = read_file("MUT")
    for _ in range(250):
        x = random.randrange(1000000)
        y = random.randrange(1000000)
        word = str(bin(x))[2:]+"#"+str(bin(y))[2:]
        mt.set_word(word)
        mt.execute()
        mt_res = "".join(mt.bands[2]).replace("_", "")
        res = str(bin(x*y))[2:]
        #print(f"{word} = {res} = {mt_res} : {res==mt_res}")
        print(res==mt_res)
        mt.reset()

def simplification(mt):
    """skip or remove useless transitions"""
    to_remove = []
    for key, content in mt.transitions.items():
        # if heads are not moved and the arrival state is not accept
        if content[-mt.k:] == ['-']*mt.k and content[0] != mt.accept:
            second_key = ",".join(content[:-mt.k])
            # then if the configuration can be read by a transition
            # then skip the intermediate transition
            if second_key in mt.transitions.keys():
                mt.transitions[key] = mt.transitions[second_key]
            # else the transition is going to be rejected so we can delete it
            else:
                to_remove.append(key)

    for key in to_remove: mt.transitions.pop(key)


def question1():
    file = input("Enter a turing machine file or press [enter] directly to use the one by default: ")
    if file == "":
        mt = read_file("PALINDROME")
        print("\nTuring machine used: fast binary palindrome from turingmachinesimulator.com")
    else:
        mt = read_file(file)
        print("\nTuring machine used: ", mt.name)

    print(mt)


def question2():
    mt = read_file("PALINDROME")
    print("\nTuring machine used: fast binary palindrome from turingmachinesimulator.com")
    word = input("Word to test: ")
    mt.set_word(word)
    print("\nInitial bands:")
    for band in mt.bands: print(band)
    mt.step()
    print("\nBands after step:")
    for band in mt.bands: print(band)


def question3():
    file = input("Enter a turing machine file or press [enter] directly to use the one by default: ")
    if file == "":
        mt = read_file("PALINDROME")
        print("\nTuring machine used: fast binary palindrome from turingmachinesimulator.com")
    else:
        mt = read_file(file)
        print("\nTuring machine used: ", mt.name)
    word = input("Word to test: ")
    mt.set_word(word)
    print("\nInitial bands:")
    for band in mt.bands: print(band)
    state = mt.execute()
    print("\nFinal bands:")
    if state == mt.accept: print("Accepted!")
    else: print("Rejected.")
    for band in mt.bands: print(band)


def question4():
    file = input("Enter a turing machine file or press [enter] directly to use the one by default: ")
    if file == "":
        mt = read_file("PALINDROME")
        print("\nTuring machine used: fast binary palindrome from turingmachinesimulator.com")
    else:
        mt = read_file(file)
        print("\nTuring machine used: ", mt.name)

    print(mt)

    word = input("\nWord to test: ")
    mt.set_word(word)
    while mt.current not in ["reject", mt.accept]:
        mt.step()
        print("\ncurrent state: ", mt.current)
        print("heads: ", mt.heads)
        print("bands:")
        for band in mt.bands: print(band)

    if mt.current == mt.accept: print("\nAccepted!")
    else: print("\nRejected.")


def question5():
    text = """Choose the file for which you want to view the code:
    [1] LEFT - used in question 7
    [2] SEARCH - used in question 7
    [3] ERASE - never used
    [4] COPY - used in question 8
    [q] quit the program
> """
    while True:
        i = input(text)
        print()
        if i == 'q': break
        elif i == '1':
            with open("Q7/XLEFT") as f:
                print("go all the way to the left for the first band")
                print("see question 7 for an example\n")
                print(f.read())
        elif i == '2':
            with open("Q7/XSEARCH") as f:
                print("search for the first occurence of '#' on the first band")
                print("see question 7 for an example\n")
                print(f.read())
        elif i == '3':
            with open("ERASE1") as f:
                print("erase the first band")
                print(f.read())

            mt = read_file("ERASE1")
            word = input("\nWord to test: ")
            mt.set_word(word)
            while mt.current not in ["reject", mt.accept]:
                mt.step()
                print("\ncurrent state: ", mt.current)
                print("heads: ", mt.heads)
                print("bands:")
                for band in mt.bands: print(band)

            if mt.current == mt.accept:
                print("\nAccepted!")
            else: print("\nRejected.")
        elif i == '4':
            with open("Q8/COPY32_42_52") as f:
                print("copy the third band to the second")
                print("then copy the fourth band to the second")
                print("and finally copy the fifth band to the second")
                print("see question 8 for an example\n")
                print(f.read())


def question6():
    file = input("Enter a turing machine file or press [enter] directly to use the one by default: ")
    if file == "":
        mt = read_file("CALLER")
        print("\nTuring machine used: a caller machine which calls a copy machine")
    else:
        mt = read_file(file)
        print("\nTuring machine used: ", mt.name)

    print(mt)

    word = input("\nWord to test: ")
    mt.set_word(word)
    while mt.current not in ["reject", mt.accept]:
        mt.step()
        print("\ncurrent state: ", mt.current)
        print("heads: ", mt.heads)
        print("bands:")
        for band in mt.bands: print(band)

    if mt.current == mt.accept: print("\nAccepted!")
    else: print("\nRejected.")


def question7():
    os.chdir("Q7")
    mt = read_file("MUL")
    print("\nTuring machine used: ", mt.name)
    print("Word input should have a '#' which is the multiplication symbol.")
    print("For example: '11#110' is like 3x6")
    word = input("\nWord to test: ")
    mt.set_word(word)
    while mt.current not in ["reject", mt.accept]:
        mt.step()
        print("\ncurrent state: ", mt.current)
        print("heads: ", mt.heads)
        print("bands:")
        for band in mt.bands: print(band)

    if mt.current == mt.accept:
        print("\nAccepted!")
        print("".join(mt.bands[1]), " is the answer")
    else: print("\nRejected.")


def question8():
    os.chdir("Q8")
    mt = read_file("SORT")
    print("\nTuring machine used: ", mt.name)
    print("Word input should be a list of 2 bits binary separated by '#'")
    print("For example: '01#00#11#00#10' is like [1, 0, 3, 0, 2]")
    word = input("\nWord to test: ")
    mt.set_word(word)
    while mt.current not in ["reject", mt.accept]:
        mt.step()
        print("\ncurrent state: ", mt.current)
        print("heads: ", mt.heads)
        print("bands:")
        for band in mt.bands: print(band)

    if mt.current == mt.accept:
        print("\nAccepted!")
        print("".join(mt.bands[1]), " is the answer")
    else: print("\nRejected.")



def question9():
    file = input("Enter a turing machine file or press [enter] directly to use the one by default: ")
    if file == "":
        mt = read_file("CALLER")
        print("\nTuring machine used: a caller machine which calls a copy machine")
    else:
        mt = read_file(file)
        print("\nTuring machine used: ", mt.name)

    print(mt)

    simplification(mt)

    print("\ntransitions after optimization:")
    for key, content in mt.transitions.items():
        print(key)
        print(",".join(content))
        print()

    word = input("\nWord to test: ")
    mt.set_word(word)
    while mt.current not in ["reject", mt.accept]:
        mt.step()
        print("\ncurrent state: ", mt.current)
        print("heads: ", mt.heads)
        print("bands:")
        for band in mt.bands: print(band)

    if mt.current == mt.accept: print("\nAccepted!")
    else: print("\nRejected.")


def remove_dead_code(mt):
    """remove transitions which are unreachable except for the first band"""
    # unoptimisable
    if mt.k == 1: return

    # for each band
    for i in range(1, mt.k):
        # at first we can only read void
        readable_char = ['_']
        j = 0
        keys = list(mt.transitions.keys())
        while j != len(mt.transitions):
            key = keys[j]
            content = mt.transitions[key]
            x = key.split(',')[-i]
            y = content[-i-mt.k]
            # if we write a new character over a readable character
            if x.strip() != y.strip() and x in readable_char:
                # this character becomes readable
                readable_char.append(y)
                # and we start over from the beginning
                j = 0
            j += 1

        to_remove = []
        for key in mt.transitions.keys():
            x = key.split(',')[-i]
            # if the transition has an unreadable character
            if x not in readable_char:
                # delete it
                to_remove.append(key)

        for key in to_remove: mt.transitions.pop(key)




def question10():
    file = input("Enter a turing machine file or press [enter] directly to use the one by default: ")
    if file == "":
        mt = read_file("ERASE1")
        print("\nTuring machine used: a caller machine which calls a copy machine")
    else:
        mt = read_file(file)
        print("\nTuring machine used: ", mt.name)

    print(mt)

    remove_dead_code(mt)

    print("\ntransitions after optimization:")
    for key, content in mt.transitions.items():
        print(key)
        print(",".join(content))
        print()

    word = input("\nWord to test: ")
    mt.set_word(word)
    while mt.current not in ["reject", mt.accept]:
        mt.step()
        print("\ncurrent state: ", mt.current)
        print("heads: ", mt.heads)
        print("bands:")
        for band in mt.bands: print(band)

    if mt.current == mt.accept: print("\nAccepted!")
    else: print("\nRejected.")


def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == "question1":
            question1()
        elif sys.argv[1] == "question2":
            question2()
        elif sys.argv[1] == "question3":
            question3()
        elif sys.argv[1] == "question4":
            question4()
        elif sys.argv[1] == "question5":
            question5()
        elif sys.argv[1] == "question6":
            question6()
        elif sys.argv[1] == "question7":
            question7()
        elif sys.argv[1] == "question8":
            question8()
        elif sys.argv[1] == "question9":
            question9()
        elif sys.argv[1] == "question10":
            question10()
        else:
            print("wrong arguments - see README.MD")
            exit(1)
    elif len(sys.argv) >= 3:
        mt = read_file(sys.argv[1])
        mt.set_word(sys.argv[2])
        print(mt)
        state = mt.execute()
        print("\nFinal bands:")
        for band in mt.bands: print(band)
        if state == mt.accept: print("Accepted!")
        else: print("Rejected.")
    else:
        print("not enough arguments - see README.MD")
        exit(1)


if __name__ == "__main__":
    main()
