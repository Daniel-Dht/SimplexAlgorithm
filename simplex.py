# -*- coding: utf-8 -*-
"""
Created on Mon Mar 27 10:36:14 2017

@author: Daniel.D
"""

from tkinter import *
import time

WIDTH = 800
HEIGHT = 500
SIZE = 50
tk = Tk()
canvas = Canvas(tk, width=WIDTH, height=HEIGHT, bg="grey")
canvas.pack()
color = 'black'

xmin = -5
xmax =  5
ymin = -5
ymax =  5

    
def xPixel2Domain(x):
    return x/WIDTH*(xmax-xmin) + xmin;
    
def yPixel2Domain(y):
    return y/HEIGHT*(ymax-ymin) + ymin;
    
def f(x,y):
    x = xPixel2Domain(x)
    y = yPixel2Domain(y)
    return x**2+y**2
  
class Simplex:
    def __init__(self):
        self.points = [[150,200,0],[200,150,0],[300,200,0]] 
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
            if self.points[k][2] > bestValue :
                bestValue = self.points[k][2] 
                bestIndex = k
        return bestIndex

    def findWorst(self):
        worstValue = self.points[0][2]
        worstIndex = 0
        for k in range(3):
            if self.points[k][2] > worstValue :
                worstValue = self.points[k][2] 
                worstIndex = k
        self.indexTab.remove(worstIndex)        
        x1 = self.points[worstIndex][0]-10
        x2 = self.points[worstIndex][0]+10
        canvas.create_oval( x1,  self.points[worstIndex][1]-10 , x2, self.points[worstIndex][1]+10) #for debug
        print("plus grande valeur ", worstValue)
        return worstIndex
        
    def moveWorstPoint(self,id,bestID): # On cherche le barycentre (x,y) des points restant
        reduction = False
        valA = self.points[self.indexTab[0]][2]
        valB = self.points[self.indexTab[1]][2]
        x = ( valA*self.points[self.indexTab[1]][0] + valB*self.points[self.indexTab[0]][0] ) / (valA+valB)
        y = ( valA*self.points[self.indexTab[1]][1] + valB*self.points[self.indexTab[0]][1] ) / (valA+valB)
        newx = 2*x - self.points[id][0]     
        newy = 2*y - self.points[id][1]
        newValue = f(newx,newy)
        finalx = newx
        finaly = newy
        # on regarde si on va vers la bonne direction == EXPANSION
        if newValue < self.points[self.indexTab[0]][2] and newValue < self.points[self.indexTab[1]][2]:
            newx = 2*newx - x
            newy = 2*newy - y
            finalx = newx
            finaly = newy
        # on check pour contraction si la nouvelle valeurs est la pluse mauvaise des 3 = CONTRACTION
        elif newValue > self.points[self.indexTab[0]][2] and newValue > self.points[self.indexTab[1]][2]:
            # si elle est meilleur que l'ancienne :
            if newValue < self.points[id][2]:
                contractx = 0.5*newx - 0.5 * x
                contracty = 0.5*newy - 0.5 * y
            else :
                contractx = 0.5*self.points[id][0] - 0.5 * x
                contracty = 0.5*self.points[id][1] - 0.5 * y 
            finalx = contractx
            finaly = contracty
            # On recalcule la valeur du nouveau point
            contractValue = f(contractx,contracty)
            # Si il est toujours le plus mauvais, on réduit le triangle sur le meilleur point = REDUCTION
            if contractValue > self.points[id][2]:
                reduction = True
                # Reduction avec les 3 anciennes valeurs si la nouvelle est plus mauvaise
                if newValue > self.points[id][2]:
                    for k in range(3):
                        self.points[k][0] = 0.5*(self.points[k][0] + self.points[bestID][0])
                        self.points[k][1] = 0.5*(self.points[k][1] + self.points[bestID][1])
                # Reduction avec les 2 anciennes valeurs et la nouvelle
                else :
                    # il faut réassigner le pount qui a bougé
                    self.points[id][0] = newx
                    self.points[id][1] = newy 
                    for k in range(3): # puis on modifis les valeurs
                        self.points[k][0] = 0.5*(self.points[k][0] + self.points[bestID][0])
                        self.points[k][1] = 0.5*(self.points[k][1] + self.points[bestID][1])
                    

                    
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
    
        
simplex = Simplex()
i = 0 
while( i<20 ):
    i+=1
    wID = simplex.findWorst()
    bID = simplex.findBest()
    simplex.moveWorstPoint(wID, bID)

tk.mainloop()

##
    
      if(x > a[0]) {
        a[0] += 2*abs(a[0]-x); 
      } else {
        a[0] -= 2*abs(a[0]-x); 
      }
      if(y > a[1]) {
        a[1] += 2*abs(a[1]-y); 
      } else {
        a[1] -= 2*abs(a[1]-y); 
      }      
    













