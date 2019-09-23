from tkinter import *
import random
import math
 
# глобальные переменные
# настройки окна
WIDTH = 900
HEIGHT = 600

#settings
MISSLES_DEFAULT = 1
BASIC_WIND_COUNTER = 60
BONUS_SIZE = 50
BASIC_BONUS_COUNTER = random.randint(200,300) #"перезарядка" бонуса
NORMAL_SPEED = 10 #стандартная скорость персонажа
BULLET_SPEED_X = -30
ARROW_SPEED_X = 15
MAX_WIND_SPEED = 5
MAX_WIND_CHANGE = 2
NORMAL_REACTION_TIME=4  #тиков сохраняется действие
DIFFICULTY=5   #дальность "замечаемых снарядов" в тиках
SHOOTING_COOLDOWN=3

#just global stuff
BULLETS_MAX = MISSLES_DEFAULT
ARROWS_MAX = MISSLES_DEFAULT
BONUS_EXISTS=False
INDEEC_UPGRADE=False
COWBOY_UPGRADE=False
COWBOY_SPEED = 0
INDEEC_SPEED = 0
BULLET_SPEED_Y = 0
ARROW_SPEED_Y = 0
WIND_SPEED_X = 0
WIND_SPEED_Y = 0
WIND_COUNTER=0
BONUS_COUNTER=0
REACTION_EVADING=0
REACTION_ATTACKING=0
COWBOY_WIN=False
INDEEC_WIN=False
EVADING=False
SHOOTING=False
COOLDOWN_BULLET=0
COOLDOWN_ARROW=0


root = Tk()
root.title("WILDWEST")
 
# область анимации
c = Canvas(root, width=WIDTH, height=HEIGHT, background="#8b734b")
c.pack()
 
# персонажи
cowboy_body=c.create_rectangle(
    WIDTH-40,HEIGHT/2-40,WIDTH,HEIGHT/2+40,fill='white',tag='cowboy')
cowboy_hat=c.create_oval(
    WIDTH-40,HEIGHT/2-20,WIDTH,HEIGHT/2+20,fill='brown',tag='cowboy')

indeec_body=c.create_rectangle(
    40,HEIGHT/2-40,0,HEIGHT/2+40,fill='red',tag='indeec')
indeec_hat=c.create_oval(
    40,HEIGHT/2-20,0,HEIGHT/2+20,fill='brown',tag='indeec')


arrow_wind=c.create_line(
                            WIDTH/2-WIND_SPEED_X,HEIGHT-20-WIND_SPEED_Y,
                            WIDTH/2+WIND_SPEED_X,HEIGHT-20+WIND_SPEED_Y,
                            width=5,arrow=LAST,arrowshape='10 20 10',fill='blue')

 
# функция движения персонажей
def move_players():
# двигаем ракетку с заданной скоростью
        c.move('cowboy', 0, COWBOY_SPEED)
        # если ракетка вылезает за игровое поле возвращаем ее на место
        if c.coords(cowboy_body)[1] < 0:
            c.move('cowboy', 0, -c.coords(cowboy_body)[1])
        elif c.coords(cowboy_body)[3] > HEIGHT:
            c.move('cowboy', 0, HEIGHT - c.coords(cowboy_body)[3])


        c.move('indeec', 0, INDEEC_SPEED)
        # если ракетка вылезает за игровое поле возвращаем ее на место
        if c.coords(indeec_body)[1] < 0:
            c.move('indeec', 0, -c.coords(indeec_body)[1])
        elif c.coords(indeec_body)[3] > HEIGHT:
            c.move('indeec', 0, HEIGHT - c.coords(indeec_body)[3])
 
# функция движения снарядов и их специальные условия
def move_missles():
        global COWBOY_WIN
        global INDEEC_WIN
        global BONUS_EXISTS
        global COWBOY_UPGRADE
        global INDEEC_UPGRADE

        if BONUS_EXISTS:
                bonus_left, bonus_top, bonus_right, bonus_bot = c.coords('bonus')
                                        
        for bullet in bullets:
                bullet_left, bullet_top, bullet_right, bullet_bot = c.coords(bullet)
                bullet_center_x=bullet_left+20
                bullet_center_y=bullet_bot-10 #BULLET WIDTH HALVED
                indeec_left, indeec_top, indeec_right, indeec_bot = c.coords(indeec_body)
                try:
                        #специальные условия пуль
                        if bullet_left<0 or bullet_top<0 or bullet_right>WIDTH or bullet_bot>HEIGHT:
                                c.delete(bullet)
                                bullets.remove(bullet)
                                continue
                        elif bullet_left<indeec_right and indeec_top<bullet_center_y<indeec_bot:
                                COWBOY_WIN=True
                                break
                        elif bonus_left<bullet_center_x<bonus_right and bonus_bot>bullet_center_y>bonus_top:
                                COWBOY_UPGRADE=True
                except Exception:
                        continue
                                        
        c.move('bullet',BULLET_SPEED_X+WIND_SPEED_X,BULLET_SPEED_Y+WIND_SPEED_Y)

        for arrow in arrows:
                arrow_left, arrow_top, arrow_right, arrow_bot = c.coords(arrow)
                arrow_center_x=c.coords(arrow)[0]+20
                arrow_center_y=c.coords(arrow)[1] #arrow WIDTH HALVED
                cowboy_left, cowboy_bot, cowboy_right, cowboy_top = c.coords(cowboy_body)
                try:
                        #специальные условия стрел
                        if arrow_left<0 or arrow_top-10<0 or arrow_right>WIDTH or arrow_bot+10>HEIGHT:
                                c.delete(arrow)
                                arrows.remove(arrow)
                                continue
                        elif arrow_right>cowboy_left and cowboy_bot<arrow_center_y<cowboy_top:
                                INDEEC_WIN=True
                                break
                        elif bonus_right>arrow_center_x>bonus_left and bonus_top<arrow_center_y<bonus_bot:
                                INDEEC_UPGRADE=True
                except Exception:
                        continue
                
        c.move('arrow',ARROW_SPEED_X+WIND_SPEED_X,ARROW_SPEED_Y+WIND_SPEED_Y)


# фокус на Canvas чтобы он реагировал на нажатия клавиш
c.focus_set()

bullets=[]
arrows=[]

# функция обработки нажатия клавиш
def movement_handler(event):
    global COWBOY_SPEED,INDEEC_SPEED
    if event.keysym == "Up":
        COWBOY_SPEED = -NORMAL_SPEED
    elif event.keysym == "Down":
        COWBOY_SPEED = NORMAL_SPEED
    if event.keysym == "w":
        INDEEC_SPEED = -NORMAL_SPEED
    elif event.keysym == "s":
        INDEEC_SPEED = NORMAL_SPEED
    if event.keysym == "r":
        spawn_bullet()
    if event.keysym == "0":
            spawn_arrow()    
                 
c.bind("<KeyPress>", movement_handler)

# функция реагирования на отпускание клавиши
def stop_pad(event):
    global COWBOY_SPEED,INDEEC_SPEED
    if event.keysym in ("Up", "Down"):
        COWBOY_SPEED = 0
    if event.keysym in ("w", "s"):
        INDEEC_SPEED = 0
 
c.bind("<KeyRelease>", stop_pad)

# создание пули
def spawn_bullet():
        global COOLDOWN_BULLET
        
        if COOLDOWN_BULLET==0:
                if not (COWBOY_WIN or INDEEC_WIN):
                        if len(bullets)<BULLETS_MAX:
                                COOLDOWN_BULLET=SHOOTING_COOLDOWN
                                bullets.append(c.create_rectangle(
                                                                    c.coords(cowboy_body)[0],c.coords(cowboy_body)[1]+30,
                                                                    c.coords(cowboy_body)[2],c.coords(cowboy_body)[3]-30,
                                                                    fill='orange',tag='bullet'))
        
# создание стрелы        
def spawn_arrow():
        global COOLDOWN_ARROW
        
        if COOLDOWN_ARROW==0:
                if not (COWBOY_WIN or INDEEC_WIN):
                        if len(arrows)<ARROWS_MAX:
                                COOLDOWN_ARROW=SHOOTING_COOLDOWN
                                arrows.append(c.create_line(
                                    c.coords(indeec_body)[0],c.coords(indeec_body)[1]+40,
                                    c.coords(indeec_body)[2],c.coords(indeec_body)[3]-40,
                                    width=5,arrow=LAST,arrowshape='10 20 10',fill='red',tag='arrow'))

# функция выбора позиции для атаки
def attacking():
        global INDEEC_SPEED
        global REACTION_ATTACKING #задержка в виде "времени реакции" после выбора направления уворота

        cowboy_center_y=c.coords(cowboy_body)[1]+40
        indeec_center_y=c.coords(indeec_body)[1]+40
        diff=c.coords(indeec_body)[1]-c.coords(cowboy_body)[1]
        gunpoint=cowboy_center_y-abs(WIDTH//(ARROW_SPEED_X+WIND_SPEED_X))*WIND_SPEED_Y
        if REACTION_ATTACKING>0:
                REACTION_ATTACKING-=1
        else:        
                #if diff>0:
                if indeec_center_y>gunpoint+20:
                        INDEEC_SPEED=-NORMAL_SPEED
                        REACTION_ATTACKING=NORMAL_REACTION_TIME
                #elif diff<0:
                elif indeec_center_y<gunpoint-20:
                        INDEEC_SPEED=NORMAL_SPEED
                        REACTION_ATTACKING=NORMAL_REACTION_TIME
                else:
                        INDEEC_SPEED=0
                        REACTION_ATTACKING=NORMAL_REACTION_TIME

# функция уворотов
def evading(DIRECTION):
        global WIND_SPEED_Y
        global INDEEC_SPEED
        global NORMAL_SPEED
                
        if DIRECTION=='up':
                INDEEC_SPEED=-NORMAL_SPEED
        elif DIRECTION=='down':
                INDEEC_SPEED=NORMAL_SPEED
        
                        

def bonus_hunting():
        advr 
        #not realised yet

#функция выбора действия "ИИ"
def check_ai():
        global DIFFICULTY
        global BULLET_SPEED_X
        global WIND_SPEED_X
        global WIND_SPEED_Y
        global INDEEC_SPEED
        global NORMAL_SPEED
        global EVADING
        global SHOOTING
        global DIRECTION
        global REACTION_EVADING
        
        indeec_center_y=c.coords(indeec_body)[1]+40
        cowboy_center_y=c.coords(cowboy_body)[1]+40

        if REACTION_EVADING>0:
                REACTION_EVADING-=1

        if len(bullets)>0:        
                for bullet in reversed(bullets):   #проверка на уворот
                        bullet_center_x=c.coords(bullet)[0]+20
                        bullet_center_y=c.coords(bullet)[3]-10
                        proximity = bullet_center_x//abs((BULLET_SPEED_X+WIND_SPEED_X))
                        if proximity<=DIFFICULTY:
                                if indeec_center_y+60>bullet_center_y+WIND_SPEED_Y*proximity>indeec_center_y-60:
                                        EVADING=True
                                        REACTION_EVADING=NORMAL_REACTION_TIME
                                        if bullet_center_y+proximity*WIND_SPEED_Y>indeec_center_y: #исправить ?
                                                DIRECTION='up'
                                        elif bullet_center_y+proximity*WIND_SPEED_Y=indeec_center_y:
                                                DIRECTION=random.choice('up','down')
                                        else:
                                                DIRECTION='down'
                                else:
                                        EVADING=False
                        else:
                                EVADING=False
        else:
                EVADING=False

        flight_rounds=WIDTH//(ARROW_SPEED_X+WIND_SPEED_X) #проверка на выстрел
        if cowboy_center_y+20>indeec_center_y+WIND_SPEED_Y*flight_rounds>cowboy_center_y-20:
                SHOOTING=True          

#исполнение функции ИИ
def proceed_ai():
        global EVADING
        global SHOOTING
        

        if SHOOTING:
                spawn_arrow()
                SHOOTING=False
        if EVADING or REACTION_EVADING>0:
                print('evading')
                evading(DIRECTION)
        else:
                print('attacking')
                attacking()


#функция изменения ветра и отрисовки флюгера
def check_wind():
    global WIND_COUNTER
    global BASIC_WIND_COUNTER
    global MAX_WIND_SPEED
    global MAX_WIND_CHANGE
    global WIND_SPEED_X
    global WIND_SPEED_Y
    global arrow_wind
    global arrow_bott
    
    WIND_COUNTER+=1
    c.delete(arrow_wind)
    if WIND_COUNTER == BASIC_WIND_COUNTER:
        WIND_COUNTER=0
        wind_dif_x = random.randint(-MAX_WIND_CHANGE,MAX_WIND_CHANGE)
        wind_dif_y = random.randint(-MAX_WIND_CHANGE,MAX_WIND_CHANGE)
        WIND_SPEED_X+=wind_dif_x
        if abs(WIND_SPEED_X)>MAX_WIND_SPEED:
             WIND_SPEED_X+=-wind_dif_x
        WIND_SPEED_Y+=wind_dif_y
        if abs(WIND_SPEED_Y)>MAX_WIND_SPEED:
             WIND_SPEED_Y+=-wind_dif_y

    arrow_wind=c.create_line(
                            WIDTH/2-WIND_SPEED_X*4,HEIGHT-20-WIND_SPEED_Y*4,
                            WIDTH/2+WIND_SPEED_X*4,HEIGHT-20+WIND_SPEED_Y*4,
                            width=5,arrow=LAST,arrowshape='5 10 5',fill='blue')

# реализация бонусов
def check_bonuses():
        global BONUS_COUNTER
        global BASIC_BONUS_COUNTER
        global COWBOY_UPGRADE
        global INDEEC_UPGRADE
        global BULLETS_MAX
        global ARROWS_MAX
        global BONUS_EXISTS
        global BONUS_COUNTER

        if not BONUS_EXISTS:
                BONUS_COUNTER+=1
                if BONUS_COUNTER==BASIC_BONUS_COUNTER:
                        BONUS_COUNTER=0
                        create_bonus()
                        BONUS_EXISTS=True
                        BASIC_BONUS_COUNTER=random.randint(100,150)

        if COWBOY_UPGRADE:
                c.delete('bonus')
                BONUS_EXISTS=False
                BULLETS_MAX+=1
                COWBOY_UPGRADE=False
        if INDEEC_UPGRADE:
                c.delete('bonus')
                BONUS_EXISTS=False
                ARROWS_MAX+=1
                INDEEC_UPGRADE=False
# создание иконки бонуса
def create_bonus():
        global BONUS_SIZE
        x_init=random.randint(100,WIDTH-100-BONUS_SIZE)
        y_init=random.randint(100,HEIGHT-100-BONUS_SIZE)
        bonus=c.create_rectangle(x_init,y_init,
                           x_init+BONUS_SIZE,y_init+BONUS_SIZE,
                           fill='yellow',tag='bonus')


def game_restart(event):
        global COWBOY_WIN
        global INDEEC_WIN
        global WIND_SPEED
        global bullets
        global arrows
        global BULLETS_MAX
        global ARROWS_MAX
        global BONUS_EXISTS
        c.delete('rect')
        c.delete('play_again')
        c.delete('end_text')
        c.delete('arrow')
        c.delete('bullet')
        c.delete('bonus')
        BONUS_EXISTS = False
        BULLETS_MAX = MISSLES_DEFAULT 
        ARROWS_MAX = MISSLES_DEFAULT 
        arrows=[]
        bullets=[]
        c.coords(cowboy_body,WIDTH-40,HEIGHT/2-40,WIDTH,HEIGHT/2+40)
        c.coords(cowboy_hat,WIDTH-40,HEIGHT/2-20,WIDTH,HEIGHT/2+20)
        c.coords(indeec_body,40,HEIGHT/2-40,0,HEIGHT/2+40)
        c.coords(indeec_hat,40,HEIGHT/2-20,0,HEIGHT/2+20)
        COWBOY_WIN=False
        INDEEC_WIN=False
        WIND_SPEED=0
        root.after(30, main)

def main():
    global COWBOY_WIN
    global INDEEC_WIN
    global COOLDOWN_BULLET
    global COOLDOWN_ARROW
    
    if not (COWBOY_WIN or INDEEC_WIN):
        if COOLDOWN_BULLET>0:
                COOLDOWN_BULLET-=1
        if COOLDOWN_ARROW>0:
                COOLDOWN_ARROW-=1
        move_missles()
        check_ai()
        proceed_ai()
        move_players()
        check_wind()
        check_bonuses()

        root.after(15, main)                   # вызов самой себя каждые 15 миллисекунд
    else:                                      #окончание игры и отрисовка меню
        if COWBOY_WIN and not INDEEC_WIN:
                
                c.create_text(WIDTH/2, HEIGHT/2-50,
                                      tag='end_text',
                                      text="COWBOY WIN!",
                                      font="Arial 20",
                                      fill="#ff0000")
        elif not COWBOY_WIN and INDEEC_WIN:
                
                end_text=c.create_text(WIDTH/2, HEIGHT/2-50,
                                      tag='end_text',
                                      text="INDEEC WIN!",
                                      font="Arial 20",
                                      fill="#ff0000")
        else:
                end_text=c.create_text(WIDTH/2, HEIGHT/2-50,
                                      tag='end_text',
                                      text="DRAW!",
                                      font="Arial 20",
                                      fill="#ff0000")
        c.create_rectangle(WIDTH/2-60, HEIGHT/2-30, WIDTH/2+60, HEIGHT/2+30, fill='lightgreen',tag='rect')
        c.create_text(WIDTH/2, HEIGHT/2,
                                      tag='play_again',
                                      text="PLAY AGAIN?",
                                      font="Arial 10",
                                      fill="#ff0000")
        c.tag_bind('rect', '<Button-1>', game_restart)
        c.tag_bind('play_again', '<Button-1>', game_restart)


            
 
# запуск движения
main() 
# запуск работы окна
root.mainloop()
