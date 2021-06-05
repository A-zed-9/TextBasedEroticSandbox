# Bob

# Dialogue
dialogue_intro = "What did you want to talk about kiddo?"
dialogue_ask_to_continue = "Was there something else on your mind?"
dialogue_continue = "What else did you want to talk about?"
dialogue_initiate = "Hey buck-o, did you want to have a chat?"
dialogue_rejected = "Oh... Okay"
dialogue_dictionary = {
    "Game": {
        "True": "print(\"Are you winning son?\")"
    },
    "Grill": {
        "True": "print(\"I don't care much for politics, all I wanna do is grill god dammit.\")"
    },
    "Hold_Hands": {
        "self.romance > 50": "self.Hold_Hands(approval=[\"Asked\",True])",
        "not self.my_turn": "self.Hold_Hands(approval=[\"Asked\",False])"
    }
}
# Stats
stats_dictionary = {
    "friendship": 0,
    "romance": 0
}
