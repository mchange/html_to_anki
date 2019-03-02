#!/usr/local/bin/python
import os
import sys
import csv
from operator import itemgetter
from bs4 import BeautifulSoup
#from anki_vector import Collection as aopen
#from AnkiTools import AnkiDirect as aopen

from anki import Collection as aopen
 

 
usmle_rx = open("Japanese200.html",'r').read()
#csvfile = "/Users/drlulz/Desktop/usmle.csv"
anki_coll   = "collection.anki2"
 

 
 
def get_cards(content):
    soup = BeautifulSoup(usmle_rx)
    qas  = soup.select(".item")
    
    results = []
    for qa in qas:
        #print(qa)
        #question = (qa.find("span", class_="transliteration").next_element.text).encode('utf-8')
        #answer   = (qa.find("p", class_="response").text).encode('utf-8')
		japanese = (qa.find("p", class_="text").text).encode('utf-8')
		english = (qa.find("p", class_="response").text).encode('utf-8')
		ex1 = (qa.findAll("p", class_="translation")[0].text).encode('utf-8')
		ex2 = (qa.findAll("p", class_="translation")[1].text).encode('utf-8')
		jp1 = (qa.findAll("p", class_="transliteration")[0].text).encode('utf-8')
		jp2 = (qa.findAll("p", class_="transliteration")[1].text).encode('utf-8')
		pos = (qa.find("div", class_="part-of-speech").text).encode('utf-8')
		japanese = "<strong>" + japanese +"</strong> &nbsp&nbsp&nbsp POS: " + pos +"<br><br>" + ex1 +"<br>" + jp1 +"<br>" + ex2 +"<br>" + jp2
		results.append((english, japanese,pos))
    return results
    
    
 
def make_cards(cards):
    qas = get_cards(cards)
    card_type = 'Basic'
    deck_name = 'iknow_200'
    for qa in qas:
        card_front = itemgetter(0)(qa)
        card_back  = itemgetter(1)(qa)
        card_pos  = itemgetter(2)(qa)
        deck = aopen( anki_coll );
        deck_id = deck.decks.id(deck_name)
        deck.decks.select( deck_id )
        model = deck.models.byName( card_type )
        model['did'] = deck_id
        deck.models.save( model )
        deck.models.setCurrent( model )
        fact            = deck.newNote()
        fact['Front']   = card_front.decode('utf-8')
        fact['Back']    = card_back.decode('utf-8')
        #fact['Desc']   = card_pos.decode('utf-8')
        deck.addNote( fact )
        deck.save()
        deck.close()
    
    
 
make_cards(usmle_rx)
 

# =============================================================================
# 
#  
# soup = BeautifulSoup(usmle_rx)
# qas  = soup.select(".item")
#  
# for qa in qas:
#     ex1 = (qa.findAll("p", class_="translation")[0].text).encode('utf-8')
#     print(answer)
#     ex2 = (qa.findAll("p", class_="translation")[1].text).encode('utf-8')
#     #pos = (qa.find("div", class_="part-of-speech").text).encode('utf-8')
#     #question = (qa.find("p", class_="text").text).encode('utf-8')
#    # answer = (qa.find("p", class_="response").text).encode('utf-8')
#     print(answer1)
#     
# 
# =============================================================================


#with open(csvfile, "w") as output:
#    writer = csv.writer(output, delimiter=',', lineterminator='\n')
#    writer.writerows(get_cards(usmle_rx))