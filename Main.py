# Imports
import importlib
import os

# Variables
people = []
yesno = ["Yes", "No"]


# Functions
def get_from_module(file_name, folder, var):
    return importlib.import_module('.' + file_name, folder).__getattribute__(var)


def check_input(prompt, answers):
    while True:
        answer = input(prompt)
        if answer in answers:
            return answer


def initialize_characters():
    for character_file in os.listdir('Characters'):
        if not character_file.startswith('_'):
            character = character_file.removesuffix('.py')
            people.append(character)
            exec("global " + character + "\n" + character + " = NPC(\"" + character + "\")")


def interpret():
    keyword = ""
    subject = ""
    arguments = []
    dictionary = {
        "Keyword": ["List of arguments lists"],
        "Talk": ["dialogue_topics"],
        "Stop": ["methods"]
    }
    while True:
        answer = user_input_to_list("What would you like to do?")
        for item in answer:
            if item in dictionary:
                keyword = item
            if item in people:
                subject = item
        if keyword and subject:
            for item in answer:
                for x in dictionary[keyword]:
                    if type(x) is str:
                        if item in eval(subject + '.' + x):
                            arguments.append(item)
            try:
                return exec(subject + "." + keyword + "(" + "*" + str(arguments) + ")")
            except TypeError:
                pass


def user_input_to_list(prompt):
    input_list = input(prompt).split()
    for index, item in enumerate(input_list):
        if '.' or '!' or '?' in item:
            new_item = item.strip('.!?')
            input_list = [new_item if x == input_list[index] else x for x in input_list]
    return input_list


# Classes
class NPC:
    def __init__(self, name):
        # Name
        self.name = name
        # Dialogue
        self.dialogue_intro = get_from_module(name, 'Characters', "dialogue_intro")
        self.dialogue_ask_to_continue = get_from_module(name, 'Characters', "dialogue_ask_to_continue")
        self.dialogue_continue = get_from_module(name, 'Characters', "dialogue_continue")
        self.dialogue_dictionary = get_from_module(name, 'Characters', "dialogue_dictionary")
        self.dialogue_topics = []
        for topic in self.dialogue_dictionary:
            self.dialogue_topics.append(topic)
        # Stats
        self.stats_dictionary = get_from_module(name, 'Characters', "stats_dictionary")
        for stat in self.stats_dictionary:
            exec('self.' + stat + ' = ' + str(self.stats_dictionary[stat]))
        # Sates
        self.holding_hands_state = False
        # Methods
        self.methods = [method for method in dir(NPC) if method.startswith('__') is False]
        self.methods.remove("Stop")

    def Talk(self, topic):
        for condition in self.dialogue_dictionary[topic]:
            if eval(condition):
                exec(self.dialogue_dictionary[topic][condition])
                if check_input(self.dialogue_ask_to_continue, yesno) == "Yes":
                    topic = check_input(self.dialogue_continue, self.dialogue_topics)
                    self.Talk(topic=topic)
                else:
                    return

    def Holding_Hands(self, approval=None, stop=None):
        if self.holding_hands_state == True and not stop:
            return print("You are already holding hands with " + self.name)
        elif self.holding_hands_state == False and stop:
            return print("You are no longer holding hands with " + self.name)
        elif not self.holding_hands_state and stop:
            return print("You aren't holding " + self.name +"'s hand.")
        elif not self.holding_hands_state and not stop:
            if approval:
                return print("You are now holding hands with " + self.name + ".")
            elif not approval:
                if check_input("Do it anyway?", yesno) == "Yes":
                    self.holding_hands_state = True
                    return print("You grab " + self.name + "'s hand she tries to move it away but you hold on.")
                else:
                    return print("You don't hold hands with " + self.name)

    def Stop(self, function):
        exec("self." + function + "(stop=True)")

initialize_characters()
interpret()
