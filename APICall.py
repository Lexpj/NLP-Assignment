import requests
import json

def getRhymeWords(word, blacklist):
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
        
        # Return the words
        for unwanted in blacklist:
            if unwanted in words:
                words.remove(unwanted)
        return words
    
    # If fails, it returns an empty array
    return []

##############################################################################

# # Make the URL
# url = "https://api.datamuse.com/words?rel_rhy=" + str("panda")
# # Get the JSON from the API
# response = requests.get(url)

# blacklist = ["propaganda"]

# # If valid
# if response.status_code == 200:
    
#     # Turn the JSON into an useful datastructure
#     text = response.text
#     dic = json.loads(text)
#     words = [i["word"] for i in dic]
    
#     # Return the words
#     #print([i["word"] for i in dic])
#     for unwanted in blacklist:
#         if unwanted in words:
#             words.remove(unwanted)
#     print(words)