import playsound # to play saved mp3 file
from gtts import gTTS # google text to speech
import os # to save/open files
import wolframalpha # to calculate strings into formula
import wikipedia
import requests

appId = 'Enter wolframalpha appId' #go to wolframalpha website
client = wolframalpha.Client(appId)

num = 1
def assistant_speaks(output):
    global num

    # num to rename every audio file
    # with different name to remove ambiguity
    num += 1
    print("PerSon : ", output)

    toSpeak = gTTS(text = output, lang ='en', slow = False)
    # saving the audio file given by google text to speech
    file = str(num)+".mp3"
    toSpeak.save(file)

    # playsound package is used to play the same file.
    playsound.playsound(file, True)
    os.remove(file)

def removeBrackets(variable):
      return variable.split('(')[0]

def resolveListOrDict(variable):
  if isinstance(variable, list):
    return variable[0]['plaintext']
  else:
    return variable['plaintext']

def search_wiki(keyword=''):
      # running the query
  searchResults = wikipedia.search(keyword)
  # If there is no result, print no result
  if not searchResults:
    print("No result from Wikipedia")
    return
  # Search for page... try block
  try:
    page = wikipedia.page(searchResults[0])
  except wikipedia.DisambiguationError:
    # Select the first item in the list
    page = wikipedia.page(err.options[0])
  #encoding the response to utf-8
  wikiTitle = str(page.title.encode('utf-8'))
  wikiSummary = str(page.summary.encode('ascii', 'ignore'))
  # printing the result
  assistant_speaks(wikiSummary)


def search(text=''):
  res = client.query(text)
  # Wolfram cannot resolve the question
  if res['@success'] == 'false':
     assistant_speaks('Question cannot be resolved')
  # Wolfram was able to resolve question
  else:
    result = ''
    # pod[0] is the question
    pod0 = res['pod'][0]
    # pod[1] may contains the answer
    pod1 = res['pod'][1]
    # checking if pod1 has primary=true or title=result|definition
    if (('definition' in pod1['@title'].lower()) or ('result' in  pod1['@title'].lower()) or (pod1.get('@primary','false') == 'true')):
      # extracting result from pod1
      result = resolveListOrDict(pod1['subpod'])
      assistant_speaks(result)
      question = resolveListOrDict(pod0['subpod'])
      question = removeBrackets(question)
    else:
      # extracting wolfram question interpretation from pod0
      question = resolveListOrDict(pod0['subpod'])
      # removing unnecessary parenthesis
      question = removeBrackets(question)
      # searching for response from wikipedia
      search_wiki(question)





# Driver Code
if __name__ == "__main__":
    assistant_speaks("What's your name, Friend")
    name ='Human'
    name = input("Answer: ")
    assistant_speaks("Hello, " + name + '.')

    while(1):

        assistant_speaks("What can i do for you?")
        text = input("Answer: ")

        if "exit" in str(text) or "bye" in str(text) or "sleep" in str(text):
            assistant_speaks("Ok bye, "+ name+'.')
            break

        # calling process text to process the query
        search(text)
