# Imports
import importlib
import os
import re
import random

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
    templist = []
    print(prompt)
    user_input_list = input("==>").split()
    for item in user_input_list:
        new_item = item.strip(",.?!")
        new_item = re.sub("'s$", "", new_item)
        new_item = new_item.title()
        if "_" in new_item:
            temp2 = new_item.split("_")
            for word in temp2:
                templist.append(re.sub("ing$", "", word))
            new_item = '_'.join(templist)
        new_item = re.sub("ing$", "", new_item)
        new_user_input_list.append(new_item)
    return new_user_input_list


def get_from_module(file_name, folder, var):
    return importlib.import_module('.' + file_name, folder).__getattribute__(var)


def initialize_characters():
    for character_file in os.listdir('Main\Characters'):
        if not character_file.startswith('_'):
            character = character_file.removesuffix('.py')
            people.append(character)
            exec("global " + character + "\n" + character + " = NPC(\"" + character + "\")")


# Classes
class NPC:
    def __init__(self, name):
        # Name
        self.name = name
        # Appearance
        self.appearance_dictionary = get_from_module(name, 'Characters', "appearance_dictionary")
        self.look_args = []
        for x in self.appearance_dictionary:
            self.look_args.append(x)
            for y in self.appearance_dictionary[x]:
                self.look_args.append(y)
        # Dialogue
        self.dialogue_intro = get_from_module(name, 'Characters', "dialogue_intro")
        self.dialogue_ask_to_continue = get_from_module(name, 'Characters', "dialogue_ask_to_continue")
        self.dialogue_continue = get_from_module(name, 'Characters', "dialogue_continue")
        self.dialogue_initiate = get_from_module(name, 'Characters', "dialogue_initiate")
        self.dialogue_rejected = get_from_module(name, 'Characters', "dialogue_rejected")
        self.dialogue_dictionary = get_from_module(name, 'Characters', "dialogue_dictionary")
        self.dialogue_topics = [topic for topic in self.dialogue_dictionary]
        # Stats
        self.stats_dictionary = get_from_module(name, 'Characters', "stats_dictionary")
        for stat in self.stats_dictionary:
            exec('self.' + stat + ' = ' + str(self.stats_dictionary[stat]))
        # Sates
        self.Hold_Hands_state = False
        # Methods
        self.methods = [method for method in dir(NPC) if method.startswith('__') is False]
        self.methods.remove("Stop")
        self.my_turn = False

    def __take_turn__(self):
        self.my_turn = True
        self.Talk(character_initiated=True)
        self.my_turn = False

    def __say__(self, text):
        print(self.name + " says:")
        print(text)

    def __ask__(self, prompt, answers):
        while True:
            print(self.name + " asks:")
            answer = clean_input(prompt)
            for word in answers:
                if word in answer:
                    return word

    def __describe__(self, text):
        pass

    def Talk(self, topic=None, character_initiated=False):
        if character_initiated:
            if self.__ask__(self.dialogue_initiate, yesno) == "Yes":
                possible_topics = []
                for topic in self.dialogue_topics:
                    for condition in self.dialogue_dictionary[topic]:
                        try:
                            if eval(condition):
                                possible_topics.append(topic)
                                break
                        except NameError:
                            break
                topic = random.choice(possible_topics)
                for condition in self.dialogue_dictionary[topic]:
                    if eval(condition):
                        return exec(self.dialogue_dictionary[topic][condition])
            else:
                return self.__say__(self.dialogue_rejected)
        if not character_initiated:
            if not topic:
                topic = self.__ask__(self.dialogue_intro, self.dialogue_topics)
            for condition in self.dialogue_dictionary[topic]:
                if eval(condition):
                    return exec(self.dialogue_dictionary[topic][condition])

    def Hold_Hands(self, approval=None, stop=None):
        topic = "Hold_Hands"
        if self.my_turn:
            if stop:
                if self.__ask__(self.dialogue_dictionary[topic]["Ask Stop"], yesno) == "Yes":
                    self.Hold_Hands_state = False
                    exec(self.dialogue_dictionary[topic]["Stopping"])
                    return print("You are no longer holding hands with " + self.name)
                else:
                    exec(self.dialogue_dictionary[topic]["Forced"])
                    print(self.name + " tries moving their hand away but you hold on.")
            elif self.__ask__(self.dialogue_dictionary[topic]["Ask"], yesno) == "Yes":
                self.Hold_Hands_state = True
                exec(self.dialogue_dictionary[topic]["Initiated"])
                return print(self.name + " reaches for your hand.\nYou are now holding hands with " + self.name)
            else:
                if eval(self.dialogue_dictionary[topic]["Force"]):
                    exec(self.dialogue_dictionary[topic]["Forcing"])
                    return print(self.name + " grabs your hand anyway, holding it tight.")
                else:
                    exec(self.dialogue_dictionary[topic]["Rejected"])
                    return print("You don't hold hands with " + self.name + ".")
        elif self.Hold_Hands_state and not stop:
            exec(self.dialogue_dictionary[topic]["In progress"])
            return print("You are already holding hands with " + self.name + ".")
        elif not self.Hold_Hands_state and stop:
            return print("You aren't holding " + self.name + "'s hand.")
        elif self.Hold_Hands_state and stop:
            self.Hold_Hands_state = False
            exec(self.dialogue_dictionary[topic]["Stopped"])
            return print("You are no longer holding hands with " + self.name + ".")
        elif not self.Hold_Hands_state and not stop:
            if approval == ["Asked", True]:
                self.Hold_Hands_state = True
                exec(self.dialogue_dictionary[topic]["Accept"])
                return print("You are now holding hands with " + self.name + ".")
            elif approval == ["Asked", False]:
                exec(self.dialogue_dictionary[topic]["Reject"])
                if check_input("Do it anyway?", yesno) == "Yes":
                    self.Hold_Hands_state = True
                    exec(self.dialogue_topics[topic]["Forced"])
                    return print("You grab " + self.name + "'s hand. They try to move it away but you hold on.")
                else:
                    return print("You don't hold hands with " + self.name + ".")
            elif not approval:
                if check_input("Ask first?", yesno) == "Yes":
                    for condition in self.dialogue_dictionary[topic]:
                        if eval(condition):
                            return exec(self.dialogue_dictionary[topic][condition])
                else:
                    self.Hold_Hands_state = True
                    for condition in self.dialogue_dictionary[topic]:
                        if eval(condition):
                            exec(self.dialogue_dictionary[topic]["CNC"])
                            return print("You grab " + self.name + "'s hand. They're shocked but allow it.")
                    else:
                        exec(self.dialogue_dictionary[topic]["Forced"])
                        return print("You grab " + self.name + "'s hand. They try to move it away but you hold on.")

    def Stop(self, function):
        exec("self." + function + "(stop=True)")

    def Look(self, target):
        for targets in self.appearance_dictionary:
            if target == targets:
                return print("You look at " + self.name + "'s " + self.appearance_dictionary[target]["Description"])
            else:
                for subtargets in self.appearance_dictionary[targets]:
                    if target == subtargets:
                        return print("You look at " + self.name + "'s " + eval(self.appearance_dictionary[targets][target]["Description"]))


class PC:
    def __init__(self, name):
        self.name = name
        self.methods = [method for method in dir(PC) if method.startswith('__') is False]

    def interpret_commands(self):
        keyword = ""
        subject = ""
        argument = ""
        dictionary = {
            "Talk": "dialogue_topics",
            "Stop": "methods",
            "Hold_Hands": None,
            "Wait": None,
            "Look": "look_args"
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
                    if type(dictionary[keyword]) is str and subject:
                        if item in eval(subject + '.' + dictionary[keyword]):
                            argument = item
                    elif type(dictionary[keyword]) is list:
                        if item in dictionary[keyword]:
                            argument = item
                try:
                    if keyword in self.methods:
                        if not argument:
                            return exec("self." + keyword + "()")
                        if argument:
                            return exec("self." + keyword + "(" + argument + ")")
                    elif subject and argument:
                        return exec(subject + "." + keyword + "(" + "\"" + argument + "\"" + ")")
                    elif subject and not argument:
                        return exec(subject + "." + keyword + "()")
                    elif not subject and argument:
                        return exec(keyword + "(" + "\"" + argument + "\"" + ")")
                    elif not subject and not argument:
                        return exec(keyword + "()")
                except (TypeError, NameError):
                    pass

    def Wait(self):
        pass


# Main
def game_loop():
    while True:
        Player.interpret_commands()
        for character in people:
            exec(character + ".__take_turn__()")


initialize_characters()
Player = PC("player")
game_loop()
