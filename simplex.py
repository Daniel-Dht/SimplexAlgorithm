# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 10:36:14 2017
x
@author: Daniel.D
"""

from tkinter import *
import time

WIDTH = 1000
HEIGHT = 800
SIZE = 50
tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="grey")
canvas.pack()

fen = 6

xmin = -fen
xmax =  fen
ymin = -fen
ymax =  fen

    
def xPixel2Domain(x):
    return x/WIDTH*(xmax-xmin) + xmin;
    
def yPixel2Domain(y):
    return y/HEIGHT*(ymax-ymin) + ymin;
 
    
def f(x,y):
    x = xPixel2Domain(x)
    y = yPixel2Domain(y)
    #return x**2+y**2
    return (x**2 + y - 11)**2 + (x + y**2 - 7)**2 #  Himmelblau’s function 

  
class Simplex:
    def __init__(self, mouseX,mouseY):
        self.points = [[mouseX-25,mouseY,0],[mouseX+25,mouseY,0],[mouseX,mouseY+50,0]] 
        self.line1 = canvas.create_line(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1])
        self.line2 = canvas.create_line(self.points[0][0], self.points[0][1], self.points[2][0], self.points[2][1])
        self.line3 = canvas.create_line(self.points[1][0], self.points[1][1], self.points[2][0], self.points[2][1])
        self.points[0][2] = f( self.points[0][0],  self.points[0][1] )
        self.points[1][2] = f( self.points[1][0],  self.points[0][1] )
        self.points[2][2] = f( self.points[2][0],  self.points[0][1] )
        self.indexTab = [0,1,2]
        
    def findBest(self):
        bestValue = self.points[0][2]
        bestIndex = 0
        for k in range(3):
            if self.points[k][2] < bestValue :
                bestValue = self.points[k][2] 
                bestIndex = k
        print("meilleur valeur ", bestValue," pos : (",xPixel2Domain(self.points[bestIndex][0]),yPixel2Domain(self.points[bestIndex][0]),")"  )
        x1 = self.points[bestIndex][0]-5#for debug
        x2 = self.points[bestIndex][0]+5#for debug
        canvas.create_oval( x1,  self.points[bestIndex][1]-5 , x2, self.points[bestIndex][1]+5, fill="green") #for debug
        return bestIndex

    def findWorst(self):
        worstValue = self.points[0][2]
        worstIndex = 0
        for k in range(3):
            if self.points[k][2] > worstValue :
                worstValue = self.points[k][2] 
                worstIndex = k
        self.indexTab.remove(worstIndex)        
        x1 = self.points[worstIndex][0]-5#for debug
        x2 = self.points[worstIndex][0]+5#for debug
        canvas.create_oval( x1,  self.points[worstIndex][1]-5 , x2, self.points[worstIndex][1]+5) #for debug
        #print("plus faible valeur ", worstValue)
        return worstIndex
        
    def moveWorstPoint(self,id,bestID): # On cherche le barycentre (x,y) des points restant
        reduction = False
        valA = self.points[self.indexTab[0]][2]
        valB = self.points[self.indexTab[1]][2]
        x = ( valA*self.points[self.indexTab[1]][0] + valB*self.points[self.indexTab[0]][0] ) / (valA+valB)
        y = ( valA*self.points[self.indexTab[1]][1] + valB*self.points[self.indexTab[0]][1] ) / (valA+valB)
        
        canvas.create_oval( x-5,  y-5 , x+5,y+5, fill="black") #for debug
        
        newx = 2*x - self.points[id][0]     
        newy = 2*y - self.points[id][1]
        newValue = f(newx,newy)
        finalx = newx
        finaly = newy
        # on regarde si on va vers la bonne direction == EXPANSION
        if newValue < self.points[self.indexTab[0]][2] and newValue < self.points[self.indexTab[1]][2]:
            print("expansion  !")
            newx = 2*newx - x
            newy = 2*newy - y
            finalx = newx
            finaly = newy
        # on check pour contraction si la nouvelle valeurs est la pluse mauvaise des 3 = CONTRACTION
        elif newValue > self.points[self.indexTab[0]][2] and newValue > self.points[self.indexTab[1]][2]:
            # si elle est meilleur que l'ancienne :
            if newValue < self.points[id][2] :
                print("contraction avec le nouveau point !")
                contractx = 0.5*newx + 0.5 * x
                contracty = 0.5*newy + 0.5 * y
            else :
                print("contraction avec l'ancien point !")
                contractx = 0.5*self.points[id][0] + 0.5 * x
                contracty = 0.5*self.points[id][1] + 0.5 * y 
                canvas.create_line( self.points[id][0],self.points[id][1] , x,y, fill="green") #for debug
                
            finalx = contractx
            finaly = contracty
            # On recalcule la valeur du nouveau point
            contractValue = f(contractx,contracty)
            # Si il est toujours le plus mauvais, on réduit le triangle sur le meilleur point = REDUCTION
            if contractValue > self.points[id][2] :
                reduction = True
                print("reduction !")
                # Avant de réduire, il faut réassigner le pount qui a bougé si la nouvelle valeurs est meilleur que l'ancienne
                if newValue < self.points[id][2]:
                    self.points[id][0] = newx
                    self.points[id][1] = newy 
                  
                # Puis on réduit, et recalcules les valeurs en chaque point
                for k in range(3):
                    self.points[k][0] = 0.5*(self.points[k][0] + self.points[bestID][0])
                    self.points[k][1] = 0.5*(self.points[k][1] + self.points[bestID][1])
                    self.points[id][2] = f( self.points[0][0] ,  self.points[0][1] )
                
                
                    
        # on réinitialise la liste d'index, les coordonnées du point et sa valeur
        self.indexTab = [0,1,2] 
        if not reduction :
            self.points[id][0] = finalx
            self.points[id][1] = finaly
            self.points[id][2] = f( self.points[0][0] ,  self.points[0][1] )
        
        canvas.create_line(self.points[0][0], self.points[0][1], self.points[1][0], self.points[1][1],fill="blue")
        canvas.create_line(self.points[0][0], self.points[0][1], self.points[2][0], self.points[2][1],fill="blue")
        canvas.create_line(self.points[1][0], self.points[1][1], self.points[2][0], self.points[2][1],fill="blue")
        
        return (x,y)

simplex = 0
i = 0 
# while( i<7 ):
#     i+=1
#     print("************  ",i,"   *****************")
#     wID = simplex.findWorst()
#     bID = simplex.findBest()
#     simplex.moveWorstPoint(wID, bID)

def key(event): # déplace le simplex
    global i    
    canvas.focus_set()
    print( "pressed :", i)
    i+=1
    wID = simplex.findWorst()
    bID = simplex.findBest()
    simplex.moveWorstPoint(wID, bID)
 
def callback(event): # créé le simplex
    global simplex
    canvas.focus_set()
    #print( "clicked at", event.x, event.y)
    simplex = Simplex(event.x, event.y)

canvas.bind("<Key>", key)
canvas.bind("<Button-1>", callback )
canvas.pack()

#tk.after(2000, task)
tk.mainloop()












