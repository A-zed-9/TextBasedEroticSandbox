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
        "Talk": ["dialogue_topics"]
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
                for list in dictionary[keyword]:
                    if type(list) is str:
                        if item in eval(subject + '.' + list):
                            arguments.append(item)
            try:
                return exec(subject + "." + keyword + "(" + "*" + str(arguments) + ")")
            except TypeError:
                pass


def user_input_to_list(prompt):
    input_list = input(prompt).split()
    for index, item in enumerate(input_list):
        if '-' in item:
            new_item = item.replace('-', ' ')
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

    def Talk(self, topic):
        for condition in self.dialogue_dictionary[topic]:
            if eval(condition):
                exec(self.dialogue_dictionary[topic][condition])
                if check_input(self.dialogue_ask_to_continue, yesno) == "Yes":
                    topic = check_input(self.dialogue_continue, self.dialogue_topics)
                    self.Talk(topic=topic)

    def hold_hands(self):
        print("You are now holding hands with " + self.name + ".")


initialize_characters()
interpret()
