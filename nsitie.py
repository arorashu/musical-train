#!/usr/bin/python
#
import sys, os

# Make sure you put the mitielib folder into the python search path.  There are
# a lot of ways to do this, here we do it programmatically with the following
# two statements:
# next two statements commented by shubham arora
#parent = os.path.dirname(os.path.realpath(__file__))
#sys.path.append(parent + '/../../mitielib')

import mitie
from mitie import *
from py2neo import Graph
from py2neo import Node, Relationship

import getArticle
import getimage
import imageFunc


# create neo4j DB connection
graph = Graph("http://neo4j:itsatrap@localhost:7474/db/data/")
# to execute Cypher queries, use cypher.execute(query)
cypher = graph.cypher

print "loading NER model..."
# ner = named_entity_extractor('../../MITIE-models/english/ner_model.dat')
ner = named_entity_extractor('./MITIE-models/english/ner_model.dat')
print "\nTags output by this NER model:", ner.get_possible_ner_tags()

# Load a text file and convert it into a list of words.  
# tokens = tokenize(load_entire_file('./sample_text.txt'))
# print "Tokenized input:", tokens

pageTitle = load_entire_file('./sample_text.txt')
print "page Title: ", pageTitle
pageText = getArticle.getText(pageTitle)
print "\n page text : ", pageText
tokens = tokenize(pageText)

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


# Running MITIE's binary relation detectors.
# binary_relations is a list of lists, inner lists are of size two containing [relation_detector, relation_name]
binary_relations = []

# manually give a label for each relationship in relation_name
relation_detector = binary_relation_detector("./MITIE-models/english/binary_relations/rel_classifier_people.person.place_of_birth.svm")
relation_name = "PLACE_OF_BIRTH"
relation = [relation_detector, relation_name]
binary_relations.append(relation)

relation_detector = binary_relation_detector("./MITIE-models/english/binary_relations/rel_classifier_people.person.nationality.svm")
relation_name = "NATIONALITY"
relation = [relation_detector, relation_name]
binary_relations.append(relation)

relation_detector = binary_relation_detector("./MITIE-models/english/binary_relations/rel_classifier_people.person.religion.svm")
relation_name = "RELIGION"
relation = [relation_detector, relation_name]
binary_relations.append(relation)



# make a list of neighboring entities.  Once we have this list we
# will ask the relation detector if any of these entity pairs is an example of
# the "person born in place" relation. 
neighboring_entities = [(entities[i], entities[i+1]) for i in xrange(len(entities)-1)]
# Also swap the entities and add those in as well.  We do this because "person
# born in place" mentions can appear in the text in as "place is birthplace of
# person".  So we must consider both possible orderings of the arguments.
neighboring_entities += [(r,l) for (l,r) in neighboring_entities]

# print "\nNeighboring entities found: " , neighboring_entities

# Now that we have our list, let's check each entity pair and see which one the
# detector selects.
for entity1, entity2 in neighboring_entities:
    # Detection has two steps in MITIE. First, you convert a pair of entities
    # into a special representation.
    rel = ner.extract_binary_relation(tokens, entity1[0], entity2[0])
    # Then you ask the detector to classify that pair of entities.  If the
    # score value is > 0 then it is saying that it has found a relation.  The
    # larger the score the more confident it is.
    for relation in binary_relations:
        score = relation[0](rel)
        # Print out any matching relations.
        if (score > 0):
            entity1_text     = " ".join(tokens[i] for i in entity1[0])
            entity2_text = " ".join(tokens[i] for i in entity2[0])
            print entity1_text, relation[1], entity2_text
            query = "MERGE (u1:" + entity1[1] + "{ name: {a} }) MERGE (u2:"+ entity2[1] + "{ name:{b} }) MERGE (u1)-[:" + relation[1] + "]-(u2)"
            cypher.execute(query, a=entity1_text, b=entity2_text )

            # subject = Node( person[1], name=person_text )
            # predicate = Node( place[1], name=birthplace_text)
            # relationship = Relationship(subject, "BORN_IN", predicate)
            # graph.create(relationship)

# extract image and add image node
imageLink = getimage.getImageLink(pageTitle)
getimage.downloadImage(imageLink)
pc = imageFunc.PixelCounter('test.jpg')
# rgb average of image
rgbAverage = pc.averagePixels()[0:3]
print "rgb average is: " , rgbAverage

query = "MERGE (u1:" + "WikiPage" + "{ name: {a} }) MERGE (u2:"+ "Image" + "{ name:{b} }) MERGE (u1)-[:" + "ImageOf" + "]-(u2)"
cypher.execute(query, a=pageTitle, b=imageLink)