from spellchecker import SpellChecker


SPELL = SpellChecker()

while True:
    user_input = input("Please do not enter numbers or misspelled words. \nPlease enter a keyword(s) to search: ")
    try:
        _ = int(user_input)
    except ValueError:
        pass
    else:
        print("Please do not enter numbers!")
        continue
    user_search = user_input.replace(' ', '+')
    input_validate = user_input
    misspelled = SPELL.unknown(input_validate.split())
    if len(input_validate) >= 30:
        print("Please enter a shorter message.")
        continue
    elif len(input_validate.split()) > 3:
        print("Please type no more than 4 words")
        continue
    elif misspelled == set():
        print("Searching newegg.com for " + user_input)
        break
    else:
        print("Please enter a word in the english dictionary. \nThe word '" + user_input + "' is not valid")