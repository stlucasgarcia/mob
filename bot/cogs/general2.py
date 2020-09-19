import discord
from moodleapi.security import Cryptography
from moodleapi.token import Token

from discord.ext import commands, tasks
from settings import *
from utilities import *
import pandas as pd
from random import randint

class General2(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    #Creates a Caesar Cipher
    @commands.command()
    async def Cipher(self,ctx, *text):
        print(text)
        key = randint(2,26)
        print(key)
        def check(index, key):
	        if key > 26:
		        key = key%26
		
	        if index + key >= 26:
		        newKey =  index + key - 26
		        return 0, newKey
	
	        else:
		        return index, key
        
        alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        
        listText = list(text)
        print(listText)

        cipherText = ''

        aux = key
        for i in range(len(listText)):
            
            key = aux

            if not listText[i].isalpha():
                cipherText += listText[i]

            if listText[i].islower():
                index = alphabet.index(listText[i].upper())
                index, key = check(index, key)
                result = alphabet[index+key]
                cipherText += result.lower()

            elif listText[i].isupper():
                index = alphabet.index(listText[i])
                index, key = check(index, key)
                result = alphabet[index+key]
                cipherText += result
    
        embed = main_messages_style("Cipher text",cipherText)
        await ctx.send(embed=embed)


        

def setup(client):
    client.add_cog(General2(client))