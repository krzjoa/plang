#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
from operator import add


class Syllabizer(object):
	
	vowels = [
		'a','ą','e','ę','i','o','ó','u','y',
		'A','Ą','E','Ę','I','O','Ó','U','Y'
	]
	conosants = [
		'b','c','ć','d','f','g','h','j','k','l','ł','m','n','ń','p','r','s','ś','t','w','v','z','ż','ź',
		'B','C','Ć','D','F','G','H','J','K','L','Ł','M','N','Ń','P','R','S','Ś','T','W','V','Z','Ż','Ź'	
	]
	bivowels = [
		'ia','ią','ie','ię','iu','ió',
		'IA','IĄ','IE','IĘ','IU','IÓ'
	]
	biconosants = [
		'ch','cz','dż','dź','rz','sz',
		'Ch','Cz','Dż','Dź','Rz','Sz'
	]
	decoded_vowels = [char.decode('utf-8') for char in  vowels]
	decoded_conosants = [char.decode('utf-8') for char in conosants]
	decoded_bivowels = [char.decode('utf-8') for char in  bivowels]
	decoded_biconosants = [char.decode('utf-8') for char in biconosants]
						
	@property		
	def _all_conosants(self):
		return Syllabizer.conosants + Syllabizer.biconosants	
	@property		
	def _all_vowels(self):
		return Syllabizer.vowels + Syllabizer.bivowels	
	@property	
	def _all_bichars(self):
		return Syllabizer.biconosants + Syllabizer.bivowels		
	@property	
	def _all_decoded_conosants(self):
		return Syllabizer.decoded_conosants + Syllabizer.decoded_biconosants	
	@property		
	def _all_decoded_vowels(self):
		return Syllabizer.decoded_vowels + Syllabizer.decoded_vowels	
	@property	
	def _all_decoded_bichars(self):
		return Syllabizer.decoded_biconosants + Syllabizer.decoded_bivowels	

	def syllabize(self, word, as_one_list=False):
		if as_one_list:
			return [self.simple_cut(word),self.greedy_cut(word)]
		else:
			return self.simple_cut(word) + self.greedy_cut(word)
		
	def greedy_cut(self,word):
		symbols = self.chunk_symbols(word)
		charlist = self.split(word)
		syllables = []
		newSyllable = ""
		prevSymbol = ""
		charleng = len(charlist)
		for char, symbol, index in zip(charlist, symbols, range(charleng)):
			if (prevSymbol == 'v' and symbol=='c') or (index==(charleng-1) and symbol=='v' and prevSymbol=='c'):
				newSyllable+=char
				syllables.append(newSyllable)
				newSyllable = ""
			elif (index==(charleng-1) and symbol=='v' and prevSymbol=='v'):
				syllables.append(newSyllable)
				syllables.append(char)
			elif (prevSymbol == 'v' and symbol=='v'):
				syllables.append(newSyllable)
				newSyllable=char	
			else:
				newSyllable+=char						
			prevSymbol=symbol	
		return syllables				
				
	def simple_cut(self,word):
		symbols = self.chunk_symbols(word, as_list=True)
		charlist = self.split(word)
		syllables = []
		charleng = len(charlist)
		newSyllable = ""
		lastChar, lastSymbol = "","" 
		for char, symbol, index in zip(charlist, symbols, range(charleng)):
			newSyllable+=char
			lastChar,lastSymbol = char, symbol
			if symbol == 'v':
				syllables.append(newSyllable)
				newSyllable = ""
			if index == (len(charlist) - 1) and syllables: syllables[-1]=syllables[-1]+newSyllable
			if index == (len(charlist) - 1) and not syllables: syllables.append(newSyllable)				
		return syllables				
		
	def symbols(self,word, as_list=False):
		charlist = list(word.decode('utf-8'))
		for indx in range(len(charlist)):
			if charlist[indx] in Syllabizer.decoded_vowels:
				charlist[indx]='v'
			elif charlist[indx] in Syllabizer.decoded_conosants:
				charlist[indx]='c'
			else:
				charlist[indx]='u'
		if as_list:		
			return reduce(add,charlist)
		else:
			return charlist				
			
	def chunk_symbols(self,word,as_list=False):
		chunklist = self.split(word)
		for indx in range(len(chunklist)):
			if chunklist[indx] in self._all_vowels:
				chunklist[indx]='v'
			elif chunklist[indx] in self._all_conosants:
				chunklist[indx]='c'
			else:
				chunklist[indx]='u'
		if as_list:		
			return reduce(add,chunklist)
		else:
			return chunklist						
			
	def split(self,word):
		charlist = [char.encode('utf-8') for char in list(word.decode('utf-8'))]
		chunklist = []
		lastIndex = len(charlist) - 1
		index = 0
		while index  <= lastIndex:
			bichar = charlist[index]+charlist[index+1] if (index<lastIndex) else ""
			if bichar in self._all_bichars:
				chunklist.append(bichar)
				index+=2
			else:		
				chunklist.append(charlist[index])
				index+=1
		return chunklist			
	
