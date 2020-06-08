# Here are all the installs and imports you will need for your word cloud script and uploader widget

!pip install wordcloud
!pip install fileupload
!pip install ipywidgets
!jupyter nbextension install --py --user fileupload
!jupyter nbextension enable --py fileupload

import wordcloud
import numpy as np
from matplotlib import pyplot as plt
from IPython.display import display
import fileupload
import io
import re
import sys


#2

# This is the uploader widget

def _upload():

    _upload_widget = fileupload.FileUploadWidget()

    def _cb(change):
        global file_contents
        decoded = io.StringIO(change['owner'].data.decode('utf-8'))
        filename = change['owner'].filename
        print('Uploaded `{}` ({:.2f} kB)'.format(
            filename, len(decoded.read()) / 2 **10))
        file_contents = decoded.getvalue()

    _upload_widget.observe(_cb, names='data')
    display(_upload_widget)

_upload()
#Make a .txt file of some paras and upload here
#3

def split_and_lower(file_contents):
    file_contents = file_contents.lower()
    array_words = file_contents.split()
    return array_words

def remove_non_alphabetic(source):
    new_array =[]
    #First parameter is the replacement, second parameter is your input string
    for word in source:
        regex = re.compile('[^a-zA-Z]')
        extra = regex.sub('', word)
        new_array.append(extra)
    return new_array

def calculate_frequencies(file_contents):
    # Here is a list of punctuations and uninteresting words you can use to process your text
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    uninteresting_words = ["the", "a", "to", "if", "is", "it", "of", "and", "or", "an", "as", "i", "me", "my", \
    "we", "our", "ours", "you", "your", "yours", "he", "she", "him", "his", "her", "hers", "its", "they", "them", \
    "their", "what", "which", "who", "whom", "this", "that", "am", "are", "was", "were", "be", "been", "being", \
    "have", "has", "had", "do", "does", "did", "but", "at", "by", "with", "from", "here", "when", "where", "how", \
    "all", "any", "both", "each", "few", "more", "some", "such", "no", "nor", "too", "very", "can", "will", "just"]
    
    # LEARNER CODE START HERE
    new_array = split_and_lower(file_contents)
    original_words = remove_non_alphabetic(new_array)
    
    for word in original_words:
        if word.isnumeric():
             original_words.remove(word)
    
    new_list = []
    new_dictionary = {}
    
    for word in original_words:
        if word not in new_dictionary:
            new_dictionary[word] = 1
        elif word in new_dictionary:
            new_dictionary[word] += 1
            
    for words in uninteresting_words:
        if words in new_dictionary:
          del new_dictionary[words]
        
    #wordcloud
    cloud = wordcloud.WordCloud()
    cloud.generate_from_frequencies(new_dictionary)
    return cloud.to_array()
    
    #4
    
    # Display your wordcloud image

myimage = calculate_frequencies(file_contents)
plt.imshow(myimage, interpolation = 'nearest')
plt.axis('off')
plt.show()
