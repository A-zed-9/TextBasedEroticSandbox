# Character name (note file must be Charactername.py with the characters name being capitalized)

# Dialogue
dialogue_intro = "This is what a character will say upon initiating dialogue."
dialogue_ask_to_continue = "This is what a character will say when asking if the character wants to continue dialogue."
dialogue_continue = "This is what a character will say when asking what topic a continued conversation should be about."
dialogue_dictionary = {
    "Topic": {
        "condition == bool": "print(\"Text you want the character to say goes inside of the parentheses\".)\nprint("
                             "\"You can use as many print statements or other function calls on the same line (you "
                             "can also use \\n for multi line dialogue instead of a new print statement. And ' can be "
                             "used for apostrophes as long as one uses quotation marks as shown here.))",
        "condition != \"string\" and condition2 == additional value": "print(\"Whichever response evaluates as true "
                                                                            "first (from the top) will be the only "
                                                                            "one used. No two conditions can be "
                                                                            "exactly the same. (You can have "
                                                                            "friendship > 0 and friendship > 0 "
                                                                            "and romance > 0 but not friendship > "
                                                                            "0 and friendship > 0). To use "
                                                                            "character stats or other character "
                                                                            "related data self. must be prefixed to "
                                                                            "the condition (such as self.friendship > "
                                                                            "0).)\") ",
        "condition == value": "self.function(\"parameter1\",\"parameter2\")\nprint(\"Functions, including character "
                              "methods (denoted by self.) can be called along side dialogue. For example this can be "
                              "used to call actions or change a characters stats.\")",
        "True": "Set the last condition to True to create a default response, this response will be said if no "
                "conditional responses are. You can only have one default response per topic. If you want a character "
                "to always say the same thing for a topic this should be the only conditional in this topic. "
    }
}
# Stats (Note stats must have an initial value in order to be used by the character, even if that value is 0 (or None))
stats_dictionary = {
    "stat": "value",
    "stat2": 0
}
