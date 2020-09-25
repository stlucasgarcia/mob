import discord
from moodleapi.security import Cryptography
from moodleapi.token import Token

from discord.ext import commands, tasks
from settings import *
from utilities import *
import pandas as pd
from random import randint

class General2(Cog):
    def __init__(self, client):
        self.client = client
    
    #Creates a Caesar Cipher
    @command(name='cipher', aliases=['CIPHER', 'Cipher'])
    async def cipher(self,ctx, *text):
        # Check if key value + letter index is greater than 26
        def check(index, key):
	        if key > 26:
		        key = key%26
		
	        if index + key >= 26:
		        newKey =  index + key - 26
		        return 0, newKey # Returns new key for the letter index
	
	        else:
		        return index, key

        # Cipher text
        def cipher(listText, key):
            global cipherText
            cipherText= ''
            aux = key
            for i in range(len(listText)):
                
                key = aux
                
                # Checks if the character is alphabetical
                if not listText[i].isalpha():
                    cipherText += listText[i]

                # Check if character is lower case
                if listText[i].islower():
                    index = alphabet.index(listText[i].upper())
                    index, key = check(index, key)
                    result = alphabet[index+key]
                    cipherText += result.lower()

                # Check if character is upper case
                elif listText[i].isupper():
                    index = alphabet.index(listText[i])
                    index, key = check(index, key)
                    result = alphabet[index+key]
                    cipherText += result
    
        # Setup Alphabet and random Key
        alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        key = randint(2,25)
        print(f"Key: {key}")
        listText = list(text)

        # Execute cipher for each block of text found in the text message
        for i in range(len(listText)):
            cipher(list(listText[i]), key)

        # Prints values on Console for verification  
        print(f"Text: {text}")
        print(f"Text: {listText}")
        print(f"Cipher Text: {cipherText}")

        # Returns cipher message
        await ctx.channel.purge(limit=1)
        embed = main_messages_style("Cipher text",cipherText)
        await ctx.send(embed=embed)

    # Creates a dice command
    @command(name='roll', aliases=['ROLL', 'Roll'])
    async def roll(self,ctx, number=6): #Sets default roll number to 6
        print("Dice!")
        embed = main_messages_style("Rolling dice... 🎲")
        await ctx.send(embed=embed)
        await ctx.channel.purge(limit=1)
        num = int(number)
        embed = main_messages_style("🎲 Your results were", f"{randint(1,num)}")
        await ctx.send(embed=embed)

        

        

def setup(client):
    client.add_cog(General2(client))