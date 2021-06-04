# Imports
import importlib
import os

# Variables
people = []
yesno = ["Yes", "No"]


# Functions
def check_input(prompt, answers):
    while True:
        answer = clean_input(prompt)
        for word in answers:
            if word in answer:
                return word


def clean_input(prompt):
    new_user_input_list = []
    print(prompt)
    user_input_list = input("==>").split()
    for item in user_input_list:
        new_item = item.strip(",.?!")
        new_item = new_item.title()
        new_user_input_list.append(new_item)
    return new_user_input_list


def get_from_module(file_name, folder, var):
    return importlib.import_module('.' + file_name, folder).__getattribute__(var)


def initialize_characters():
    for character_file in os.listdir('Characters'):
        if not character_file.startswith('_'):
            character = character_file.removesuffix('.py')
            people.append(character)
            exec("global " + character + "\n" + character + " = NPC(\"" + character + "\")")


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
        self.dialogue_topics = [topic for topic in self.dialogue_dictionary]
        # Stats
        self.stats_dictionary = get_from_module(name, 'Characters', "stats_dictionary")
        for stat in self.stats_dictionary:
            exec('self.' + stat + ' = ' + str(self.stats_dictionary[stat]))
        # Sates
        self.holding_hands_state = False
        # Methods
        self.methods = [method for method in dir(NPC) if method.startswith('__') is False]
        self.methods.remove("Stop")

    def Talk(self, topic=None):
        if not topic:
            topic = check_input(self.dialogue_intro, self.dialogue_topics)
        for condition in self.dialogue_dictionary[topic]:
            if eval(condition):
                exec(self.dialogue_dictionary[topic][condition])
                if check_input(self.dialogue_ask_to_continue, yesno) == "Yes":
                    topic = check_input(self.dialogue_continue, self.dialogue_topics)
                    return self.Talk(topic=topic)
                else:
                    return

    def Hold_Hands(self, approval=None, stop=None):
        topic = "Holding_Hands"
        if self.holding_hands_state and not stop:
            return print("You are already holding hands with " + self.name)
        elif not self.holding_hands_state and stop:
            return print("You aren't holding " + self.name + "'s hand.")
        elif self.holding_hands_state and stop:
            self.holding_hands_state = False
            return print("You are no longer holding hands with " + self.name)
        elif not self.holding_hands_state and not stop:
            if approval == ["Asked", True]:
                self.holding_hands_state = True
                return print("You are now holding hands with " + self.name + ".")
            elif approval == ["Asked", False]:
                if check_input("Do it anyway?", yesno) == "Yes":
                    self.holding_hands_state = True
                    return print("You grab " + self.name + "'s hand she tries to move it away but you hold on.")
                else:
                    return print("You don't hold hands with " + self.name)
            elif not approval:
                if check_input("Ask first?", yesno) == "Yes":
                    self.Talk(topic)
                else:
                    self.holding_hands_state = True
                    return print("You grab " + self.name + "'s hand. She tries to move it away but you hold on.")

    def Stop(self, function):
        exec("self." + function + "(stop=True)")


class PC:
    def __init__(self, name):
        self.name = name
        self.methods = [method for method in dir(NPC) if method.startswith('__') is False]

    def interpret_commands(self):
        keyword = ""
        subject = ""
        argument = ""
        dictionary = {
            "Talk": "dialogue_topics",
            "Stop": "methods",
            "Hold_Hands": None
        }
        while True:
            answer = clean_input("What would you like to do?")
            for item in answer:
                if item in dictionary and not keyword:
                    keyword = item
                if item in people and not subject:
                    subject = item
            if keyword:
                for item in answer:
                    if type(dictionary[keyword]) is str:
                        if item in eval(subject + '.' + dictionary[keyword]):
                            argument = item
                    elif type(dictionary[keyword]) is list:
                        if item in dictionary[keyword]:
                            argument = item
                    try:
                        if subject and argument:
                            return exec(subject + "." + keyword + "(" + "\"" + argument + "\"" + ")")
                        elif subject and not argument:
                            return exec(subject + "." + keyword + "()")
                        elif not subject and argument:
                            return exec(keyword + "(" + "\"" + argument + "\"" + ")")
                        elif not subject and not argument:
                            return exec(keyword + "()")
                        elif keyword in self.methods:
                            pass
                    except TypeError:
                        pass


# Main
def game_loop():
    while True:
        Player.interpret_commands()


initialize_characters()
Player = PC("player")
game_loop()
