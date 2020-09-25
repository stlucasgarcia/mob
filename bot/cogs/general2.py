from discord.ext import tasks
from discord.ext.commands import command, Cog

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
        alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        key = randint(2,25)
        print(f"Key: {key}")
        def check(index, key):
	        if key > 26:
		        key = key%26
		
	        if index + key >= 26:
		        newKey =  index + key - 26
		        return 0, newKey
	
	        else:
		        return index, key
        def cipher(listText, key):
            global cipherText
            cipherText= ''
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
    
        
        listText = list(text)


        for i in range(len(listText)):
            #print(list(listText[i]))
            cipher(list(listText[i]), key)
            
        print(f"Text: {text}")
        print(f"Text: {listText}")
        print(f"Cipher Text: {cipherText}")
        await ctx.channel.purge(limit=1)

        embed = main_messages_style("Cipher text",cipherText)
        await ctx.send(embed=embed)


    @command(name='roll', aliases=['ROLL', 'Roll'])
    async def roll(self,ctx, number=6):
        print("Dice!")
        embed = main_messages_style("Rolling dice... 🎲")
        await ctx.send(embed=embed)
        await ctx.channel.purge(limit=1)
        num = int(number)
        embed = main_messages_style("🎲 Your results were", f"{randint(1,num)}")
        await ctx.send(embed=embed)

        

        

def setup(client):
    client.add_cog(General2(client))