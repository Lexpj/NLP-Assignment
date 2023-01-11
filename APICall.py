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
        
        # Return the words
        return [i["word"] for i in dic]
    
    # If fails, it returns an empty array
    return []

