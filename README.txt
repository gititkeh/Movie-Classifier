# Movie-Classifier
Movie Classifier using Google prediction API
--------------------------------------------------------
Files in this project:
- README
- extractWiki.py - used for data extraction and processing, creates train and test files.
- train - csv, used to build the model (uploaded to the cloud and trained directly in google consol).
- test - same foramt as train, used for testing the model.
- predice.py - uses the google python client and prediction API to print model information,
  get predictions, and calculate accuracy on the test set (requires credentials! - json file).
- Are these predictions good? - a short analysis and explanations of the results.
---------------------------------------------------------
The task:
Given a movie's plot, classify it to one of these three genres:
- American westerns
- American horror films
- American children's films
(I tried to find classes that do not frequently intersect each other)
----------------------------------------------------------
The data:
The "Plot" section of ~2000 Wikipedia pages from the above Wikipedia categories, after removing stopwords
(very frequent and mostly non-informative word) and stemming (e.g. driving -> driv). 
The labels are the categories' names as in Wikipedia, and the features are the whole plot section as one string
(bag-of-words according to google's tutorial).
----------------------------------------------------------
Needed external packages:
nltk, wikitools, google api python client, json
