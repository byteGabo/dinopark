import turtle

#VENTANA
pan = turtle.Screen()
pan.title('PingPong')
pan.bgcolor('blue')
pan.setup(width=800,height=600)
pan.tracer(0)

#PUNTUACION
A = 0 
B = 0

#DIBUJAR JUGADOR 1 
J1 = turtle.Turtle()
J1.speed(0)
J1.shape('square')
J1.color('white')
J1.penup()
J1.goto(-350,0) 
J1.shapesize(stretch_wid=5,stretch_len=1)

#DIBUJAR JUGADOR 2 
J2 = turtle.Turtle()
J2.speed(0)
J2.shape('square')
J2.color('white')
J2.penup()
J2.goto(350,0)
J2.shapesize(stretch_wid=5,stretch_len=1)

#DIBUJAR PELOTA
P = turtle.Turtle()
P.speed(0)
P.shape('square')
P.color('white')
P.penup()
P.goto(0,0)

#LINEA
div = turtle.Turtle()
div.color("white")
div.goto(0,400)
div.goto(0,-400)

P.dx = 0.80
P.dy = 0.80



#FUNCIONES
def j1_up():
	y = J1.ycor()
	y += 20
	J1.sety(y)
 
def j1_down():
	y = J1.ycor()
	y -= 20
	J1.sety(y)

def j2_up():
	y = J2.ycor()
	y += 20
	J2.sety(y)

def j2_down():
	y = J2.ycor()
	y -= 20
	J2.sety(y)
 
#TECLAS DE JUGADORES
pan.listen()
pan.onkeypress(j1_up,'w')
pan.onkeypress(j1_down,'s')
pan.onkeypress(j2_up,'o')
pan.onkeypress(j2_down,'l')

#MAIN
while True:
    pan.update()
    
    #MOVER LA BOLA 
    P.setx(P.xcor() + P.dx)
    P.sety(P.ycor() + P.dy)
    
    #COLISIONES
    if P.ycor() > 290:
        P.dy *= -1     
    if P.ycor() < -290:
        P.dy *= -1
        A +=1
        print ('Jugador1: ' + str(A))
        
    if P.xcor() > 390:
        P.goto(0,0)
        P.dx *= -1    
    if P.xcor() < -390:
        P.goto(0,0)
        P.dx *= -1
        B +=1
        print ('Jugador2: ' + str(B))
        
        
        
    #COLISIONES DE JUGADORES     
    if((P.xcor() > 340 and P.xcor() < 350)
        and (P.ycor() < J2.ycor() + 50
        and P.ycor() > J2.ycor() - 50)):
        P.dx *= -1   
        
    if((P.xcor() < -340 and P.xcor() > -350)
        and (P.ycor() < J1.ycor() + 50
        and P.ycor() > J1.ycor() - 50)):
        P.dx *= -1 