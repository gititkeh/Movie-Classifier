# Extract the plot description of given movie categories, then clean, remove frequent words
# and stem it, to create train and test files of the form: "category", "plot" (in each line)

import nltk
from nltk.corpus import stopwords
from wikitools import wiki
from wikitools import page
from wikitools import category

# List of movie categories to be extracted
categories = ["American horror films",
              "American Western (genre) films",
              "American children's films"]
   
site = wiki.Wiki("http://en.wikipedia.org/w/api.php")
porter = nltk.stem.porter.PorterStemmer() #to be used in stemming below

for c in categories:
    i = 0
    cat = category.Category(site, title=c)
    pageList = cat.getAllMembersGen() #Page generator
    for page in pageList:
        print i
        text = page.getWikiText()
        # Find the Plot section in the page
        plot = ""
        beg_i = text.find('==Plot')
        if beg_i == -1:
            continue
        plot = text[beg_i+2:]
        end_i = plot.find('\n==')
        if end_i == -1:
            continue
        plot = plot[:end_i]
        # lowercasing, removing stopwords and stemming
        if plot != "":
            plot = [s.lower() for s in nltk.word_tokenize(plot) if s.isalnum()]
            plot = [porter.stem(s) for s in plot if not s in stopwords.words('english')]
            
        # Take every 10th page for the test set
        if i%10 == 0:
            with open('test', 'a') as test:
                test.write(('"'+c+'",'+'"'+str(' '.join(plot))+'"\n').encode('ascii', 'ignore'))
        else:
            with open('train', 'a') as train:
                train.write(('"'+c+'",'+'"'+str(' '.join(plot))+'"\n').encode('ascii', 'ignore'))
        i += 1
           
