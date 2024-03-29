import requests
import json

def getRhymeWords(word):
    """
    Get the rhyme words in an array from a given word
    :param word: word as input for the rhyme word API
    :return: array of rhyme words
    """

    # Make the URL
    url = "https://api.datamuse.com/words?rel_rhy=" + str(word)
    # Get the JSON from the API
    response = requests.get(url)

    # If valid
    if response.status_code == 200:
        
        # Turn the JSON into an useful datastructure
        text = response.text
        dic = json.loads(text)
        words = [i["word"] for i in dic]
        
        return words
    
    # If fails, it returns an empty array
    return []

def checkWord(word):
    """
    Gets an input word from the user in a string form and checks if the word is in the english dictionary
    :param word: input string of user which is a word from a sentence to rhyme on
    :return: if the word exists in the dictionary
    """

    #######
    # Currently this is done with a directionary for which you need an account and token to access the API
    # Replace this with your own account or any word checker API
    #######
    
    app_id = '813b84fe'
    app_key = 'e6e31085db033e2d591816e4f809311d'
    language = 'en-gb'
    
    # Get request
    try:
        url = 'https://od-api.oxforddictionaries.com/api/v2/entries/'  + language + '/'  + word.lower()
        response = requests.get(url, headers = {'app_id' : app_id, 'app_key' : app_key})
    except Exception as e:
        print(e)
    # If valid
    if response.status_code == 200:
        return 1
    else:
        return 0

def checkName(word):
    """
    Gets an input word from the user in a string form and checks if the word is in the name dictionary
    :param word: input string of user which is a word from a sentence to rhyme on
    :return: if the word exists in the dictionary
    """
    # Make the URL
    url = f"https://www.behindthename.com/api/lookup.json?name='{str(word)}'&key=al061590979"

    # Get the JSON data from the API
    response = requests.get(url).json()

    # Check if word is in name dictionary
    if "error_code" not in response:
        return 1
    else:
        return 0