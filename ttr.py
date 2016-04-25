#!/usr/bin/python
#
# This example shows how to use the MITIE Python API to perform named entity
# recognition and also how to run a binary relation detector on top of the
# named entity recognition outputs.
#
import sys, os

# Make sure you put the mitielib folder into the python search path.  There are
# a lot of ways to do this, here we do it programmatically with the following
# two statements:
# next two statements commented by shubham arora
#parent = os.path.dirname(os.path.realpath(__file__))
#sys.path.append(parent + '/../../mitielib')

import mitie
import urllib2
from bs4 import BeautifulSoup
from mitie import *
from collections import defaultdict
from py2neo import Graph
from py2neo import Node, Relationship

# create neo4j DB connection
graph = Graph("http://neo4j:itsatrap@localhost:7474/db/data/")




print "loading NER model..."
# ner = named_entity_extractor('../../MITIE-models/english/ner_model.dat')
ner = named_entity_extractor('./MITIE-models/english/ner_model.dat')
print "\nTags output by this NER model:", ner.get_possible_ner_tags()

# Load a text file and convert it into a list of words.  
tokens = tokenize(load_entire_file('./sample_text.txt'))
print "Tokenized input:", tokens

#load the text, images etc from an internet resource
# $req = urllib2.Request('https://en.wikipedia.org/wiki/Barack_Obama')
# response = urllib2.urlopen(req)
# html_page = response.read()

#initialise beautiful soup
# soup = BeautifulSoup(html_page, 'html.parser')



entities = ner.extract_entities(tokens)
print "\nEntities found:", entities
print "\nNumber of entities detected:", len(entities)

# entities is a list of tuples, each containing an xrange that indicates which
# tokens are part of the entity, the entity tag, and an associate score.  The
# entities are also listed in the order they appear in the input text file.
# Here we just print the score, tag, and text for each entity to the screen.
# The larger the score the more confident MITIE is in its prediction.
for e in entities:
    range = e[0]
    tag = e[1]
    score = e[2]
    score_text = "{:0.3f}".format(score)
    entity_text = " ".join(tokens[i] for i in range)
    print "   Score: " + score_text + ": " + tag + ": " + entity_text






# Now let's run one of MITIE's binary relation detectors.  MITIE comes with a
# bunch of different types of relation detector and includes tools allowing you
# to train new detectors.  However, here we simply use one, the "person born in
# place" relation detector.
rel_place_of_birth = binary_relation_detector("./MITIE-models/english/binary_relations/rel_classifier_people.person.place_of_birth.svm")
rel_nationality = binary_relation_detector("./MITIE-models/english/binary_relations/rel_classifier_people.person.nationality.svm")
rel_religion = binary_relation_detector("./MITIE-models/english/binary_relations/rel_classifier_people.person.religion.svm")

# First, let's make a list of neighboring entities.  Once we have this list we
# will ask the relation detector if any of these entity pairs is an example of
# the "person born in place" relation. 
neighboring_entities = [(entities[i], entities[i+1]) for i in xrange(len(entities)-1)]
# Also swap the entities and add those in as well.  We do this because "person
# born in place" mentions can appear in the text in as "place is birthplace of
# person".  So we must consider both possible orderings of the arguments.
neighboring_entities += [(r,l) for (l,r) in neighboring_entities]

# Now that we have our list, let's check each entity pair and see which one the
# detector selects.
for person, place in neighboring_entities:
    # Detection has two steps in MITIE. First, you convert a pair of entities
    # into a special representation.
    rel = ner.extract_binary_relation(tokens, person[0], place[0])
    # Then you ask the detector to classify that pair of entities.  If the
    # score value is > 0 then it is saying that it has found a relation.  The
    # larger the score the more confident it is.  Finally, the reason we do
    # detection in two parts is so you can reuse the intermediate rel in many
    # calls to different relation detectors without needing to redo the
    # processing done in extract_binary_relation().
    score = rel_place_of_birth(rel)
    # Print out any matching relations.
    if (score > 0):
        person_text     = " ".join(tokens[i] for i in person[0])
        birthplace_text = " ".join(tokens[i] for i in place[0])
        print person_text, "BORN_IN", birthplace_text
        subject = Node( person[1], name=person_text )
        predicate = Node( place[1], name=birthplace_text)
        relationship = Relationship(subject, "BORN_IN", predicate)
        graph.create(relationship)

    #now doing the same for religion
    score = rel_nationality(rel)
    if (score > 0):
        first_text     = " ".join(tokens[i] for i in person[0])
        second_text = " ".join(tokens[i] for i in place[0])
        print first_text, "PRACTICES", second_text
        subject = Node( person[1], name=first_text )
        predicate = Node( place[1], name=second_text)
        relationship = Relationship(subject, "PRACTICES", predicate)
        graph.create(relationship)