# Sarah

# Dialogue
dialogue_intro = "Hey there! What did you want to talk about?"
dialogue_ask_to_continue = "Was there something else you wanted to talk about?"
dialogue_continue = "What else did you want to talk about?"
dialogue_dictionary = {
    "Weekend": {
        "True": "print(\"I like to spend my weekends out, I'm sure you'll catch me at one of the bars around here if "
                "you like to dance.\") ",
    },
    "Hold_Hands": {
        "self.friendship >= 10 or self.romance >= 5": "self.Hold_Hands(approval=[\"Asked\",True])",
        "True": "\nself.Hold_Hands(approval=[\"Asked\",False])"
    },
    "Bob": {
        "True": "print(\"bob\")"
    }
}
# Stats
stats_dictionary = {
    "friendship": 10,
    "romance": 0
}
