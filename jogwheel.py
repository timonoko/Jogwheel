
from machine import Pin,ADC
import time,math,random,os

YEL = ADC(Pin(32))
GRE = ADC(Pin(33))
ORA = ADC(Pin(25))

YEL.atten(ADC.ATTN_11DB)
GRE.atten(ADC.ATTN_11DB)
ORA.atten(ADC.ATTN_11DB)

nolla=[3,3,0]

def clear():
    print("\x1B\x5B2J", end="")
    print("\x1B\x5BH", end="")

def lue():
    return [int(YEL.read()/1000),
          int(GRE.read()/1000),
          int(ORA.read()/1000)]

def odota():
    while not(lue()[0]==3 and lue()[1]==3):
        pass
laskuri=0

edellinen=[0,0,0]
while True:
    luku=lue();
    le=luku[0]
    ri=luku[1]
    if luku==nolla:
        pass
        Suunta=''
    elif edellinen!=luku:
        if luku[2]>0:
            kaksi=[luku[0],luku[1]]
            if Suunta=='':
                if kaksi==[0,4] : Suunta='V'
                if kaksi==[4,0] : Suunta='O'
                LoppuVoima=0
                Voima=0
                EdVoima=0
            laskuri=0
            if Suunta=='O':
                if kaksi==[4,0]: Voima=1
                if kaksi==[0,4]: Voima=3
            else:
                if kaksi==[4,0]: Voima=3
                if kaksi==[0,4]: Voima=1
            if kaksi==[0,0]: Voima=2
            if kaksi==[4,4]: Voima=4
            if EdVoima+1==Voima and Voima==3: LoppuVoima+=1 ; print(Suunta,LoppuVoima)
            if EdVoima-1==Voima and Voima==1: LoppuVoima-=1 ; print(Suunta,LoppuVoima)
            EdVoima=Voima
        else:
            if ri>2 and le<2:
                print("JL")
                laskuri-=1
                odota()
            if le>2 and ri<2:
                print("JR")
                laskuri+=1
                odota()
    edellinen=luku

    
