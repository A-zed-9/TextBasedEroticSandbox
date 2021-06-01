# Imports
import importlib
import os

# Variables
yesno = ["Yes", "No"]


# Functions
def initialize_characters():
    for character_file in os.listdir('Characters'):
        if not character_file.startswith('_'):
            character = character_file.removesuffix('.py')
            exec("global " + character + "\n" + character + " = NPC(\"" + character + "\")")


def check_input(prompt, answers):
    while True:
        answer = input(prompt)
        if answer in answers:
            return answer


def get_from_module(name, var):
    return importlib.import_module('.' + name, 'Characters').__getattribute__(var)


# Classes
class NPC:
    def __init__(self, name):
        # Name
        self.name = name
        # Dialogue
        self.dialogue_intro = get_from_module(name, "dialogue_intro")
        self.dialogue_ask_to_continue = get_from_module(name, "dialogue_ask_to_continue")
        self.dialogue_continue = get_from_module(name, "dialogue_continue")
        self.dialogue_dictionary = get_from_module(name, "dialogue_dictionary")
        self.dialogue_topics = []
        for topic in self.dialogue_dictionary:
            self.dialogue_topics.append(topic)
        # Stats
        self.stats_dictionary = get_from_module(name, "stats_dictionary")
        for stat in self.stats_dictionary:
            exec('self.' + stat + ' = ' + str(self.stats_dictionary[stat]))

    def talk(self, topic=None):
        if not topic:
            topic = check_input(self.dialogue_intro, self.dialogue_topics)
        for condition in self.dialogue_dictionary[topic]:
            if eval(condition):
                exec(self.dialogue_dictionary[topic][condition])
                if check_input(self.dialogue_ask_to_continue, yesno) == "Yes":
                    topic = check_input(self.dialogue_continue, self.dialogue_topics)
                    self.talk(topic=topic)

    def hold_hands(self):
        print("You are now holding hands with " + self.name + ".")


class Player:
    def __init__(self, name):
        self.name = name

    def get_player_commands(self):
        pass
initialize_characters()
Sarah.talk()
Bob.talk()
