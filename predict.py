# This file uses functionality from prediction.py (from Google prediction samples)

import pprint
from apiclient import sample_tools
from oauth2client import client
import json

# Print information about pre-created classification model (which was created by
# Google prediction API), and send prediction requests for a given test set.
# Then, calculate accuracy of the test set.
def main(model_name, test_set):

  # Extract samples from labeled test file into a dictionary 
  lines = open(test_set).readlines()
  ind = 0
  testDict = {}
  for line in lines:
    # Dictionary values: [label, features(movie plot text)]
    testDict[ind] = [line.split(',')[0], line.split(',')[1]]
    ind += 1
  
  # Initialization
  service = sample_tools.init("", 'prediction', 'v1.6', __doc__, __file__)[0]

  # Confusion matrix:
  # Create a dictionary with keys as actual labels and values as no. of predictions a label
  # got in all 3 classes (order = western, children, horror)
  resDict = {"American Western (genre) films":[0,0,0],
             "American children's films":[0,0,0],
             "American horror films":[0,0,0]}
  
  # Updating the dictionary after each prediction
  def update_resDict(lab, pred):        
    if pred == "American Western (genre) films":
        resDict[lab][0] += 1
    elif pred == "American children's films":
        resDict[lab][1] += 1
    else:
        resDict[lab][2] += 1
        
  try:
    # Get access to the Prediction API.
    papi = service.trainedmodels()

    # Print model description
    result = papi.analyze(id=model_name,project="441770761352").execute()
    print 'Analyze results:\n'
    pprint.pprint(result)

    # Create prediction for every sample in the test set
    for sample in testDict.keys():
      label = testDict[sample][0].strip('"')
      body = {'input': {'csvInstance': [testDict[sample][1]]}}
      result = papi.predict(body=body, id=model_name, project="441770761352").execute()
      predicted = result["outputLabel"]
      testDict[sample].append(predicted) #add to the dictionary for json.dump
      update_resDict(label, predicted)
    

  except client.AccessTokenRefreshError:
    print ("The credentials have been revoked or expired, please re-run"
      "the application to re-authorize")

  # Calculating accuracy, precision and recall of test set
  west = resDict["American Western (genre) films"]
  children = resDict["American children's films"]
  horror = resDict["American horror films"]

  print "\n\n-------------------------------------------"
  print "Accuracy, precision and recall of test set:\n"
  print "-------------------------------------------"
  print "accuracy =", float(west[0]+children[1]+horror[2])/ind
  print "recall_west =", float(west[0])/sum(west)
  print "precision_west =", float(west[0])/(west[0]+children[0]+horror[0])
  print "recall_children =", float(children[1])/sum(children)
  print "precision_children =", float(children[1])/(west[1]+children[1]+horror[1])
  print "recall_horror =", float(horror[2])/sum(horror)
  print "precision_horror =", float(horror[2])/(west[2]+children[2]+horror[2])


  # Print test+predictions into file
  json.dump(testDict, open('testDict.json','w'))


if __name__ == '__main__':
  main("movie_classifier", 'test')

