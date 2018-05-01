# Written by: Yanlin Duan (yd2380@columbia.edu)
from tkinter import *
from tkinter import simpledialog
from PIL import ImageTk, Image
import os
import random

####################################
# Model
####################################

def init(data,rows,cols):
    # set initial game information
    
    data.rows = rows
    data.cols = cols
    data.margin = 20
    data.timerDelay = 1000
    data.time = -1
    data.mines = 0
    data.gameOver= False
    data.paused= False
    data.win= False  
    data.info = []
    
    print(data.rows)
    print(data.cols)    
    
       #Initiliaze a row by col board
    tempList = []
    for i in range(0,data.rows):
        for j in range(0,data.cols):
            tempList.append([None,False])
        data.info.append(tempList)
        tempList = []
    
    return

def buryMines(data):
    #randomly select spots in the grid to place one or two mines per row
    
    row = 0
    while(row < len(data.info)):
        amtMines = random.randint(1,data.rows//5)
        for i in range(0,amtMines):
             col = random.randint(0,data.cols-1)
             
             #to avoid placing a mine on the same space
             if(not(data.info[row][col][0] == -1)):
                 data.info[row][col][0] = -1  
                 data.mines += 1
        row += 1
    return data.info

def recursiveShow(row,col,data):

    #if this space is a flag, do not recurse
    if(data.info[row][col][1]):
        return
    #if you touch mine, you LOSER
    if(data.info[row][col][0] == -1):
        data.gameOver= True
        return
        
    #if you touch anything thats not blank, stop recursing
    if(data.info[row][col][0] != None):
        return
        
    #if you touch a space that has mines around it, reaveal how  many mines are around it
    if(countAround(row,col,data) > 0):
        data.info[row][col][0] = countAround(row,col,data)
        return
        
    #if you touch a blank space, reveal all spaces around it
    else:
        data.info[row][col][0] = 10
        #Top Left
        if(row >= 1 and col >= 1):
            recursiveShow(row-1,col-1,data)  
        #Top
        if(row >= 1):
            recursiveShow(row-1,col,data)
        #Top Right
        if(row >= 1 and col < data.cols-1):
            recursiveShow(row-1,col+1,data)
        #Left
        if(col >= 1):
            recursiveShow(row,col-1,data)
        #Right
        if(col < data.cols-1):
            recursiveShow(row,col+1,data)
        #Bottom Left
        if(row < data.rows-1 and col >= 1):
            recursiveShow(row+1,col-1,data)
        #Bottom
        if(row < data.rows-1):
            recursiveShow(row+1,col,data)
        #Bottom Right
        if(row < data.rows-1 and col < data.cols-1):
            recursiveShow(row+1,col+1,data)

    return
        
def countAround(row,col,data):
    # count the number of mines around the cell at (row, col), 
    # return integer value 
    amtMines = 0
    #Top Left
    if(row >= 1 and col >= 1):
        if(data.info[row-1][col-1][0] == -1):
            amtMines += 1
    #Top
    if(row >= 1):
        if(data.info[row-1][col][0] == -1):
            amtMines += 1  
    #Top Right
    if(row >= 1 and col < data.cols-1):
        if(data.info[row-1][col+1][0] == -1):
            amtMines += 1
    #Left
    if(col >= 1):
        if(data.info[row][col-1][0] == -1):
            amtMines += 1
    #Right
    if(col < data.cols-1):
        if(data.info[row][col+1][0] == -1):
            amtMines += 1    
    #Bottom Left
    if(row < data.rows-1 and col >= 1):
        if(data.info[row+1][col-1][0] == -1):
            amtMines += 1
    #Bottom
    if(row < data.rows-1):
        if(data.info[row+1][col][0] == -1):
            amtMines += 1
    #Bottom Right
    if(row < data.rows-1 and col < data.cols-1):
        if(data.info[row+1][col+1][0] == -1):
            amtMines += 1

    return amtMines

####################################
# Controller
####################################

def leftMousePressed(event, data):
    # recognize left click, if the cell clicked is not a mine, check all the c
    # cells around it, if it is a mine, game over
    #if(not(data.gameOver)):
    
    #if game is not over, and game is not paused, and game is not won, click a space
    if(not(data.gameOver) and not(data.paused) and not(data.win)):    
        recursiveShow((event.y-5)//50,(event.x-5)//50,data)

    xmid = data.width//2
   
    #if a game is over and you click in the "Play Again" box, restart game
    if((data.gameOver or data.win) and event.x > xmid-97 and event.x < xmid+103 \
    and event.y > data.height-56 and event.y < data.height):      
        start()    
    return
    


def rightMousePressed(event,data,canvas):

    #if game is not over, and game is not paused, and game is not won...
    if(not(data.gameOver) and not(data.paused) and not(data.win)):
        
        #if tile is not touched...
        if(data.info[event.y//50][event.x//50][0] == None):
            
            #if tile does not have a flag, add a flag
            if(not(data.info[event.y//50][event.x//50][1])):
                data.info[event.y//50][event.x//50][1] = True
                data.mines -= 1
                
            #if tile does has a flag, remove the flag    
            else:
                data.info[event.y//50][event.x//50][1] = False
                data.mines += 1
                
        #if tile is a mine...        
        elif(not(data.info[event.y//50][event.x//50][0] > 0)): 
            
            #if tile does not have a flag, add a flag
            if(not(data.info[event.y//50][event.x//50][1])):
                data.info[event.y//50][event.x//50][1] = True
                data.mines -= 1
                
            #if tile does has a flag, remove the flag                
            else:
                data.info[event.y//50][event.x//50][1] = False
                data.mines += 1
    return

def keyPressed(event, data):
    #recognize pressed key, if it is "p" pause the game  \

    #if key 'p' is pressed, pause the game
    if(event.keysym.lower() == 'p'):
        data.paused = not(data.paused)

    return

def timerFired(data):
    # check if the user has visited all the non-mine cells
    # if so, user wins the game

    #check all spaces, if all spaces that are not mines are pressed, you win the game
    if(not(data.gameOver) and not(data.paused) and not(data.win)):
        data.time += 1    
    for row in data.info:
        for col in row:
            if col[0] == None:
                return
    data.win = True
    return

####################################
# View
####################################

def drawBoard(canvas, data):
    # draw individual cells on the board. Mine, non-mine, visited, 
    # and unvisited cells should all look difference

    #White is not clicked
    #Gray is clicked

           
    #iterate through board
    for i in range(0,data.rows):
        for j in range(0,data.cols):
            
            #create the board
            canvas.create_rectangle(j*50+5,i*50+5,(j+1)*50+5,(i+1)*50+5)
            
            clikcolor = '#99e6ff'
            unclikcolor = '#e6ffff'           
            
            #if this space is a flag, create a flag
            if(data.info[i][j][1]):
                canvas.create_rectangle(j*50+5,i*50+5,(j+1)*50+5,(i+1)*50+5,fill=unclikcolor)
                canvas.create_text(j*50+30,i*50+30,text="F", font=("Arial",26,"bold"))
                #image1 = "flag.png"
                #photo1 = PhotoImage(file=image1)                
                #canvas.create_image(j*50+30,i*50+30, image=photo1)
                
            #if this space is not touched, make it white
            elif(data.info[i][j][0] == None):
                canvas.create_rectangle(j*50+5,i*50+5,(j+1)*50+5,(i+1)*50+5,fill=unclikcolor)
                
            #if this space is a mine, make it white
            elif(data.info[i][j][0] == -1):
                canvas.create_rectangle(j*50+5,i*50+5,(j+1)*50+5,(i+1)*50+5,fill=unclikcolor)
                
            #if this space was clicked, make it gray
            elif(data.info[i][j][0] == 10):
                canvas.create_rectangle(j*50+5,i*50+5,(j+1)*50+5,(i+1)*50+5,fill=clikcolor)
                
            #if this space was clicked, show many mines are around it
            else:
                colors = ['#3385ff','#33cc33','#ff3300','#6600cc','#804000','#00b8e6','#ffa31a','#e6e600']
                val = data.info[i][j][0]
                canvas.create_rectangle(j*50+5,i*50+5,(j+1)*50+5,(i+1)*50+5,fill=clikcolor)
                canvas.create_text(j*50+30,i*50+30,text = str(val),fill=colors[val-1],font=("Arial",14,"bold"))
                
    #if you win...         
    if(data.win):
        drawWin(canvas,data)
                
    #if you paused the game...
    if(data.paused and not(data.gameOver) and not(data.win)):
        drawPaused(canvas,data)
        

        
    #if the game is over...   
    if(data.gameOver):
        drawGameOver(canvas, data)

    
    #if you are playing the game...
    if(not(data.gameOver) and not(data.paused) and not(data.win)):
        drawBottom(canvas,data)
        
    #debugging stuff
    for rows in data.info:
        print(rows)
    print()
    return
    


def drawBottom(canvas,data):
    
    #colors
    textcolor = "#621ccc"
    textbkgrd = '#ff9beb'   
    
    #Timer box        
    canvas.create_rectangle(data.width-100,data.height-56,data.width,data.height, fill = textbkgrd)
    canvas.create_text(data.width-50,data.height-41,text = "Timer", fill = textcolor, font=("Arial",14))
    canvas.create_text(data.width-50,data.height-16,text = str(data.time), fill = textcolor, font=("Arial",26,"bold"))
    
    #Mines box
    canvas.create_rectangle(5,data.height-56,105,data.height, fill = textbkgrd)
    canvas.create_text(55,data.height-41,text = "Mines", fill = textcolor, font=("Arial",14))
    canvas.create_text(55,data.height-16,text = str(data.mines), fill = textcolor, font=("Arial",26,"bold"))

def drawPlayAgain(canvas,data):
    #colors
    playcolor = '#ffd260'
    playbkgrd = '#60c2ff'
    
    xmid = data.width//2
        
    #Play Again button
    canvas.create_rectangle(xmid-97,data.height-56,xmid+103,data.height, fill=playbkgrd)
    canvas.create_text(xmid+3,data.height-28,text="Play Again?", fill=playcolor, font=("Arial",26,"bold"))
       
def drawPaused(canvas,data):
    # show text in the center of the board that tells the user the game
    # is paused if data.paused is True

    #Pause message
    canvas.create_text(data.width//2,(data.height-56)//2,text="YOU PAUSED",fill="#00cc00",font=("Arial",26,"bold"))
            
    drawBottom(canvas,data)

    return

def drawGameOver(canvas, data):
    # show text in the center of the board that tells the user the game
    # is over if data.gameOver is True. Show different messages for winning
    # and losing
    
    #iterate through the board and reveal all mines
    for i in range(0,data.rows):
        for j in range(0,data.cols):
            if(data.info[i][j][0] == -1):
                canvas.create_oval(j*50+15,i*50+15,(j+1)*50-5,(i+1)*50-5,fill="red")
             
    #Lose message          
    canvas.create_text(data.width//2,(data.height-56)//2,text="YOU LOSED!",fill="#990000", font=("Arial",26,"bold"))
        
    drawBottom(canvas,data)
    
    #Play Again button
    drawPlayAgain(canvas,data)    
    
    return
    
def drawWin(canvas,data):
    #Win message
    canvas.create_text(data.width//2,(data.height-56)//2,text="YOU WINNNED!", fill="#ffdb4d",font=("Arial",26,"bold"))
    
    drawBottom(canvas,data)

    #Play Again button
    drawPlayAgain(canvas,data)

def redrawAll(canvas, data):
    drawBoard(canvas, data)

####################################
# Use the run function as-is
####################################

def start():
    root = Tk()
    num = simpledialog.askinteger("Welcome!", "Thank you for playing our color-sweeper\n\
    Please enter a number between 5 and 20 for your board size", parent=root)
    if(num < 5):
        num = 5
    elif(num > 20):
        num = 20
    ROWS = COLS = num
    root.destroy()
    run(ROWS*50+6, COLS*50+66,ROWS,COLS)
    

def run(width,height,rows,cols):
    # Run function adapted from David Kosbie's 
    # snake-demo.py for 15-112 (CarpeDiem!)

    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def leftMousePressedWrapper(event, canvas, data):
        leftMousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def rightMousePressedWrapper(event, canvas, data):
        rightMousePressed(event, data, canvas)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    
    # Set up data and call init
    class Struct(object): pass
    
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    init(data,rows,cols)                
                
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    
    
      
      
     
        
    buryMines(data)

    
    # set up events
    root.bind("<Button-1>", lambda event:
                            leftMousePressedWrapper(event, canvas, data))
    root.bind("<Button-3>", lambda event:
                            rightMousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    
start()