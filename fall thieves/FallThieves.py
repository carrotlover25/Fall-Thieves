# main game
import sys
import pygame 
import random
import math
import time
from pygame.time import Clock
import pandas as pd

pygame.init() 
pygame.font.init()
pygame.mixer.init()
pygame.display.set_caption("Fall Thieves")
screen = pygame.display.set_mode((1200, 675))

# Initialize variables for button locations
sbLocation = None
mbLocation = None

# colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
PURPLE = (128, 0, 128)

# inicializar variables necesarias
htpbLocation = pygame.Rect(0, 0, 0, 0)  
gbbLocation = pygame.Rect(0, 0, 0, 0)  


# necesario para el juego de memoria
altura_boton = 50  # Ajuste del botón
medida_cuadro = 120  # Tamaño de cada cuadro para que encajen en 4x4 en 550x550
nombre_imagen_oculta = "assets/oculta.png"
imagen_oculta = pygame.image.load(nombre_imagen_oculta)
imagen_oculta = pygame.transform.scale(imagen_oculta, (medida_cuadro, medida_cuadro))
segundos_mostrar_pieza = 2  # Segundos para ocultar la pieza si no es la correcta

# clases


class Cuadro:
    def __init__(self, fuente_imagen):
        self.mostrar = True
        self.descubierto = False
        self.fuente_imagen = fuente_imagen
        self.imagen_real = pygame.image.load(fuente_imagen)
        self.imagen_real = pygame.transform.scale(self.imagen_real, (120, 120))
        
class JuegoMemoria:
    def __init__(self, screen):
        self.screen = screen
        self.altura_boton = 30  # Ajuste del botón
        self.medida_cuadro = 120  # Tamaño de cada cuadro para que encajen en 4x4 en 550x550
        self.nombre_imagen_oculta = "assets/oculta.png"
        self.imagen_oculta = pygame.image.load(self.nombre_imagen_oculta)
        self.imagen_oculta = pygame.transform.scale(self.imagen_oculta, (self.medida_cuadro, self.medida_cuadro))
        self.segundos_mostrar_pieza = 2  # Segundos para ocultar la pieza si no es la correcta
        self.completed = False

        self.Cuadro = Cuadro

        self.cuadros = [
            [Cuadro("assets/phishing_amarillo.png"), Cuadro("assets/phishing_amarillo.png"),
             Cuadro("assets/phishing_azul.png"), Cuadro("assets/phishing_azul.png")],
            [Cuadro("assets/phishing_blanca.png"), Cuadro("assets/phishing_blanca.png"),
             Cuadro("assets/phishing_pare.png"), Cuadro("assets/phishing_pare.png")],
            [Cuadro("assets/phishing_random.png"), Cuadro("assets/phishing_random.png"),
             Cuadro("assets/phishing_rojo.png"), Cuadro("assets/phishing_rojo.png")],
            [Cuadro("assets/phishing_sesion.png"), Cuadro("assets/phishing_sesion.png"),
             Cuadro("assets/phishing_negro.png"), Cuadro("assets/phishing_negro.png")]
        ]

        # Colores
        self.color_blanco = (255, 255, 255)
        self.color_negro = (0, 0, 0)
        self.color_gris = (206, 206, 206)
        self.color_azul = (30, 136, 229)

        # Sonidos
        self.sonido_fondo = pygame.mixer.Sound("assets/fondo.wav")
        self.sonido_clic = pygame.mixer.Sound("assets/clic.wav")
        self.sonido_exito = pygame.mixer.Sound("assets/ganador.wav")
        self.sonido_fracaso = pygame.mixer.Sound("assets/equivocado.wav")
        self.sonido_voltear = pygame.mixer.Sound("assets/voltear.wav")

        # Calculamos el tamaño de la pantalla
        self.anchura_pantalla = len(self.cuadros[0]) * self.medida_cuadro
        self.altura_pantalla = (len(self.cuadros) * self.medida_cuadro) + self.altura_boton
        self.anchura_boton = self.anchura_pantalla

        # Fuente del botón
        self.tamanio_fuente = 20
        self.fuente = pygame.font.SysFont("Arial", self.tamanio_fuente, bold=True)
        self.xFuente = int((self.anchura_boton / 2) - (self.tamanio_fuente * 3.5))
        self.yFuente = int(self.altura_pantalla - self.altura_boton / 2 - self.tamanio_fuente / 2)

        # Botón como un rectángulo
        self.boton = pygame.Rect(0, self.altura_pantalla - self.altura_boton, self.anchura_boton, self.altura_boton)

        # Banderas
        self.ultimos_segundos = None
        self.puede_jugar = True
        self.juego_iniciado = False
        self.x1 = None
        self.y1 = None
        self.x2 = None
        self.y2 = None

    def ocultar_todos_los_cuadros(self):
        for fila in self.cuadros:
            for cuadro in fila:
                cuadro.mostrar = False
                cuadro.descubierto = False

    def aleatorizar_cuadros(self):
        cantidad_filas = len(self.cuadros)
        self.screen.fill(self.color_negro)
        cantidad_columnas = len(self.cuadros[0])
        for y in range(cantidad_filas):
            for x in range(cantidad_columnas):
                x_aleatorio = random.randint(0, cantidad_columnas - 1)
                y_aleatorio = random.randint(0, cantidad_filas - 1)
                cuadro_temporal = self.cuadros[y][x]
                self.cuadros[y][x] = self.cuadros[y_aleatorio][x_aleatorio]
                self.cuadros[y_aleatorio][x_aleatorio] = cuadro_temporal

    def comprobar_si_gana(self):
        if self.gana():
            pygame.mixer.Sound.play(self.sonido_exito)
            self.reiniciar_juego()
            global memoryGame_completed
            memoryGame_completed = True

    def gana(self):
        for fila in self.cuadros:
            for cuadro in fila:
                if not cuadro.descubierto:
                    return False
        return True

    def reiniciar_juego(self):
        self.juego_iniciado = False

    def iniciar_juego(self):
        pygame.mixer.Sound.play(self.sonido_clic)
        for i in range(3):
            self.aleatorizar_cuadros()
        self.ocultar_todos_los_cuadros()
        self.juego_iniciado = True

    def manejar_click(self, pos):
        if not self.puede_jugar:
            return

        # Desplazamientos para ajustar la posición de las imágenes
        x_offset = 700  # Desplazamiento horizontal
        y_offset = 100  # Desplazamiento vertical

        if self.boton.collidepoint(pos):
            if not self.juego_iniciado:
                self.iniciar_juego()
        else:
            if not self.juego_iniciado:
                return
            
            # Ajustar la posición del clic restando los desplazamientos
            x = (pos[0] - x_offset) // self.medida_cuadro
            y = (pos[1] - y_offset) // self.medida_cuadro

            # Verificar si el clic está dentro de la cuadrícula
            if x < 0 or y < 0 or x >= len(self.cuadros[0]) or y >= len(self.cuadros):
                return  # Clic fuera de los límites de la cuadrícula

            cuadro = self.cuadros[y][x]
            if cuadro.mostrar or cuadro.descubierto:
                return
            
            if self.x1 is None and self.y1 is None:
                # Primer clic
                self.x1 = x
                self.y1 = y
                self.cuadros[self.y1][self.x1].mostrar = True
                pygame.mixer.Sound.play(self.sonido_voltear)
            else:
                # Segundo clic
                self.x2 = x
                self.y2 = y
                self.cuadros[self.y2][self.x2].mostrar = True
                cuadro1 = self.cuadros[self.y1][self.x1]
                cuadro2 = self.cuadros[self.y2][self.x2]
                if cuadro1.fuente_imagen == cuadro2.fuente_imagen:
                    # Encontró un par
                    cuadro1.descubierto = True
                    cuadro2.descubierto = True
                    self.x1 = None
                    self.y1 = None
                    self.x2 = None
                    self.y2 = None
                    pygame.mixer.Sound.play(self.sonido_clic)
                else:
                    # Fallo en el par
                    pygame.mixer.Sound.play(self.sonido_fracaso)
                    self.ultimos_segundos = int(time.time())
                    self.puede_jugar = False
            self.comprobar_si_gana()

    def mostrar_cuadros(self):
        ahora = int(time.time())
        if self.ultimos_segundos is not None and ahora - self.ultimos_segundos >= self.segundos_mostrar_pieza:
            self.cuadros[self.y1][self.x1].mostrar = False
            self.cuadros[self.y2][self.x2].mostrar = False
            self.x1 = None
            self.y1 = None
            self.x2 = None
            self.y2 = None
            self.ultimos_segundos = None
            self.puede_jugar = True

        # Desplazamiento de imágenes
        x_offset = 700  # Desplazamiento horizontal para las imágenes
        y_offset = 100  # Desplazamiento vertical solo para las imágenes

        x = 0
        y = 0
        for fila in self.cuadros:
            x = 0
            for cuadro in fila:
                if cuadro.descubierto or cuadro.mostrar:
                    self.screen.blit(cuadro.imagen_real, (x + x_offset, y + y_offset))
                else:
                    self.screen.blit(self.imagen_oculta, (x + x_offset, y + y_offset))
                x += self.medida_cuadro
            y += self.medida_cuadro

        # Ajustar la posición del botón justo debajo de las cartas
        boton_y = y + y_offset  # Justo debajo de la última fila de cartas
        self.boton = pygame.Rect(x_offset, boton_y, self.anchura_boton, self.altura_boton)

        # Dibujar el botón
        pygame.draw.rect(self.screen, self.color_negro, self.boton)
        self.screen.blit(self.fuente.render("Iniciar juego", True, self.color_blanco), 
                 (self.boton.centerx - self.tamanio_fuente * 3.5, boton_y + (self.altura_boton // 4)))
        (self.boton.centerx - self.tamanio_fuente * 3.5, boton_y + (self.altura_boton // 4))
            
        
    pygame.display.update()
        
class Puzzle:
    def __init__(self, image_file_name, image_size, puzzle_size, pos, show_scramble=False):
        self.loadedimage = pygame.image.load(image_file_name)
        self.loadedimage = pygame.transform.scale(self.loadedimage, image_size)
        
        self.pos = pos
        self.dim = image_size
        self.size = puzzle_size
        self.puzzle = self.create_puzzle()
        self.void = (puzzle_size[0] - 1, puzzle_size[1] - 1)
        self.puzzle[self.void[0]][self.void[1]] = (-1, -1)

        self.show_scramble = show_scramble
        self.scramble_moves = 0
        self.moves = [self.move_up, self.move_down, self.move_left, self.move_right]
        self.animating = None
        self.buffer = (0, 0)
        self.ANIMATION_SPEED = 0.1
        self.revealing = False
        self.revealing_animation = 0
        self.REVEALING_ANIMATION_SPEED = 10

    def create_puzzle(self):
        return [[(i, j) for j in range(self.size[1])] for i in range(self.size[0])]

    def render(self, screen):
        cell_width = self.dim[0] // self.size[0]
        cell_height = self.dim[1] // self.size[1]

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.animating == (i, j):
                    screen.blit(self.loadedimage, (self.pos[0] + i * cell_width + int(self.buffer[0] * cell_width),
                                                   self.pos[1] + j * cell_height + int(self.buffer[1] * cell_height)),
                                 (self.puzzle[i][j][0] * cell_width, self.puzzle[i][j][1] * cell_height, cell_width, cell_height))
                else:
                    screen.blit(self.loadedimage, (self.pos[0] + i * cell_width, self.pos[1] + j * cell_height),
                                 (self.puzzle[i][j][0] * cell_width, self.puzzle[i][j][1] * cell_height, cell_width, cell_height))

        self.draw_grid(screen, cell_width, cell_height)

    def draw_grid(self, screen, cell_width, cell_height):
        for i in range(self.size[0] + 1):
            pygame.draw.line(screen, [0] * 3, (self.pos[0] + i * cell_width, self.pos[1]),
                             (self.pos[0] + i * cell_width, self.pos[1] + self.size[1] * cell_height), 10)
        for j in range(self.size[1] + 1):
            pygame.draw.line(screen, [0] * 3, (self.pos[0], self.pos[1] + j * cell_height),
                                 (self.pos[0] + self.size[0] * cell_width, self.pos[1] + j * cell_height), 10)

    def reveal(self, screen):
        if not self.revealing:
            self.revealing = True
            self.revealing_animation = 255
        image = self.loadedimage.copy()
        image.set_alpha(255 - self.revealing_animation)
        screen.blit(image, self.pos)

    def __reduce_buffer(self):
        if self.buffer[0] > 0:
            self.buffer = (max(0, self.buffer[0] - self.ANIMATION_SPEED), self.buffer[1])
        if self.buffer[0] < 0:
            self.buffer = (min(0, self.buffer[0] + self.ANIMATION_SPEED), self.buffer[1])
        if self.buffer[1] > 0:
            self.buffer = (self.buffer[0], max(0, self.buffer[1] - self.ANIMATION_SPEED))
        if self.buffer[1] < 0:
            self.buffer = (self.buffer[0], min(0, self.buffer[1] + self.ANIMATION_SPEED))

    def move_up(self, animate=True, anim_time=1):
        if self.void[1] < self.size[1] - 1:
            self.swap_tiles(self.void[0], self.void[1], self.void[0], self.void[1] + 1)
            self.void = (self.void[0], self.void[1] + 1)
            if animate:
                self.animating = (self.void[0], self.void[1] - 1)
                self.buffer = (0, 1 * anim_time)

    def move_down(self, animate=True, anim_time=1):
        if self.void[1] > 0:
            self.swap_tiles(self.void[0], self.void[1], self.void[0], self.void[1] - 1)
            self.void = (self.void[0], self.void[1] - 1)
            if animate:
                self.animating = (self.void[0], self.void[1] + 1)
                self.buffer = (0, -1 * anim_time)

    def move_left(self, animate=True, anim_time=1):
        if self.void[0] < self.size[0] - 1:
            self.swap_tiles(self.void[0], self.void[1], self.void[0] + 1, self.void[1])
            self.void = (self.void[0] + 1, self.void[1])
            if animate:
                self.animating = (self.void[0] - 1, self.void[1])
                self.buffer = (1 * anim_time, 0)

    def move_right(self, animate=True, anim_time=1):
        if self.void[0] > 0:
            self.swap_tiles(self.void[0], self.void[1], self.void[0] - 1, self.void[1])
            self.void = (self.void[0] - 1, self.void[1])
            if animate:
                self.animating = (self.void[0] + 1, self.void[1])
                self.buffer = (-1 * anim_time, 0)

    def swap_tiles(self, x1, y1, x2, y2):
        self.puzzle[x1][y1], self.puzzle[x2][y2] = self.puzzle[x2][y2], self.puzzle[x1][y1]

    def is_solved(self):
        if self.scramble_moves > 0:
            return False
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.puzzle[i][j] != (-1, -1) and self.puzzle[i][j] != (i, j):
                    return False
        return True

    def update(self):
        if self.animating is not None:
            self.__reduce_buffer()
            if self.buffer == (0, 0):
                self.animating = None
        elif self.scramble_moves > 0:
            self.scramble()
        elif self.revealing and self.revealing_animation > 0:
            self.revealing_animation = max(0, self.revealing_animation - self.REVEALING_ANIMATION_SPEED)

    def moves_allowed(self):
        return self.scramble_moves == 0 and self.animating is None and not self.is_solved()

    def scramble(self):
        if self.scramble_moves == 0:
            self.scramble_moves = random.randint(self.size[0] * self.size[1] ** 2, self.size[0] * self.size[1] ** 3)
        
        if self.show_scramble:
            random.choice(self.moves)(True, 0.001)
            self.scramble_moves -= 1
        else:
            for _ in range(self.scramble_moves):
                random.choice(self.moves)(False)
            self.scramble_moves = 0
            
clock = Clock()

class Game:
    def __init__(self):
        self.puzzle = Puzzle("gameImages/PuzzleImage.jpg", (600, 600), (3, 3), (550, 30))
        self.puzzle.scramble()
        self.key_states = {pygame.K_w: False, pygame.K_a: False, pygame.K_s: False, pygame.K_d: False}
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.completed = False
        self.screen = screen

    def handle_events(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            self.update_key_state(event)

    def update_key_state(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.key_states:
                self.key_states[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in self.key_states:
                self.key_states[event.key] = False

        self.move_puzzle()

    def move_puzzle(self):
        if self.key_states[pygame.K_w]:
            self.puzzle.move_up()
        elif self.key_states[pygame.K_a]:
            self.puzzle.move_left()
        elif self.key_states[pygame.K_s]:
            self.puzzle.move_down()
        elif self.key_states[pygame.K_d]:
            self.puzzle.move_right()

    def update(self):
        self.puzzle.update()
        if self.puzzle.is_solved():
            self.completed = True

    def is_game_over(self):
        return self.completed

    def show_game_over(self):
        result_text = "You completed the puzzle!"
        game_over_message = self.font.render(result_text, True, WHITE)
        self.screen.blit(game_over_message, (50, 300))
        completed_message = self.font.render("You have completed the game!", True, GREEN)
        self.screen.blit(completed_message, (50, 350))

    def render(self, screen):
        self.puzzle.render(screen)
        if self.puzzle.is_solved():
            self.puzzle.reveal(screen)
            self.show_game_over()
        pygame.display.update()

    def run(self):
        while self.running:
            clock.tick(60)
            self.handle_events()
            self.update()
            self.render(screen)




class SecurityQuestions:
    def __init__(self, screen, font, data_file, background):
        self.screen = screen
        self.font = font
        self.data_file = data_file
        self.background = pygame.image.load(background)
        self.questions = []  # Aquí almacenaremos las preguntas y opciones randomizadas
        self.question_index = 0
        self.correct_answers = 0
        self.answer_buttons = []
        self.completed = False
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.PURPLE = (128, 0, 128)

        # Cargar preguntas y respuestas randomizadas
        self.load_questions()

    def load_questions(self):
        data = pd.read_excel(self.data_file)
        data = data.astype(str)
        randomized_questions = []

        for i in range(len(data)):
            options = [
                data['correct answer'][i],
                data['R1'][i],
                data['R2'][i]
            ]
            randomized_questions.append({
                "question": data['Questions'][i],
                "options": random.sample(options, len(options)),  
                "correct_answer": data['correct answer'][i]
            })

        self.questions = randomized_questions

    def show_question(self):
        """Muestra la pregunta y las opciones en pantalla."""
        if self.question_index >= len(self.questions):
            self.completed = True
            return False 

        question_data = self.questions[self.question_index]
        question_text = self.font.render(question_data['question'], True, self.WHITE)
        self.screen.blit(question_text, (50, 80))

        self.answer_buttons = []
        mouse_pos = pygame.mouse.get_pos()

        for i, option in enumerate(question_data['options']):
            button_rect = pygame.Rect(50, 150 + (i * 60), 700, 50)
            if button_rect.collidepoint(mouse_pos):
                inflated = button_rect.inflate(10, 10)
                button_color = self.PURPLE
            else:
                inflated = button_rect
                button_color = self.GREEN

            pygame.draw.rect(self.screen, button_color, inflated)
            button_text = self.font.render(option, True, self.BLACK)
            self.screen.blit(button_text, (inflated.x + 10, inflated.y + 10))
            self.answer_buttons.append((button_rect, option))

        return True

    def handle_answer(self, pos):
        for button_rect, option in self.answer_buttons:
            if button_rect.collidepoint(pos):
                question_data = self.questions[self.question_index]
                if option == question_data['correct_answer']:
                    self.correct_answers += 1
                self.question_index += 1
                return True
        return False

    def is_game_over(self):
        return self.completed

    def show_game_over(self):
        result_text = f"Game Over! You answered {self.correct_answers} out of {len(self.questions)} correctly."
        game_over_message = self.font.render(result_text, True, self.WHITE)
        self.screen.blit(game_over_message, (50, 300))
        completed_message = self.font.render("You have completed the game!", True, self.GREEN)
        self.screen.blit(completed_message, (50, 350))
            
# Primer frame 
def frame1():
    global sbLocation, mbLocation  # Allow access to these variables outside the function
    
    background = pygame.image.load("gameImages/MainBackground.png")

    # Start button
    startButton = pygame.image.load("gameImages/StartButton.png").convert_alpha()
    sbLocation = startButton.get_rect()
    sbLocation.x = 90
    sbLocation.y = 330

    # Menu button
    menuButton = pygame.image.load("gameImages/MenuButton.png").convert_alpha()
    mbLocation = menuButton.get_rect()
    mbLocation.x = 750
    mbLocation.y = 340
    
    # Pintar el frame
    screen.blit(background, (0,0))
    screen.blit(startButton, sbLocation)
    screen.blit(menuButton, mbLocation)
    
def frame2(): # opening del juego
    background = pygame.image.load("gameImages/openingScene.png")
    screen.blit(background, (0,0))
    
    #yes button
    font = pygame.font.Font(None, 30)
    yesButton = pygame.Rect(590, 400, 190, 50)
    yesButtonText = font.render("Yes", True, BLACK)
    yBmouse_pos = pygame.mouse.get_pos()
    
    if yesButton.collidepoint(yBmouse_pos):
        yesButton.inflate_ip(10, 10) 
        
    yesButtonColor = GREEN if yesButton.collidepoint(yBmouse_pos) else GRAY
    pygame.draw.rect(screen, yesButtonColor, yesButton)
    screen.blit(yesButtonText, (yesButton.x + 70, yesButton.y + 15))
    
    # no button
    font = pygame.font.Font(None, 30)
    noButton = pygame.Rect(800, 401, 190, 50)
    noButtonText = font.render("No", True, BLACK)
    nBmouse_pos = pygame.mouse.get_pos()
    
    if noButton.collidepoint(nBmouse_pos):
        noButton.inflate_ip(10,10)
    
    noButtonColor = RED if noButton.collidepoint(nBmouse_pos) else GRAY
    pygame.draw.rect(screen, noButtonColor, noButton)
    screen.blit(noButtonText, (noButton.x + 70, noButton.y + 15))
    
def frame3(): # frame del menu
    global htpbLocation, gbbLocation
    background = pygame.image.load("gameImages/OptionsScreen.png")
    
    # how to play button 
    howToPlayButton = pygame.image.load("gameImages/HowToPlayButton.png").convert_alpha()
    htpbLocation = howToPlayButton.get_rect()
    htpbLocation.x = 100
    htpbLocation.y = 100
    
    # go back button
    gobackButton = pygame.image.load("gameImages/GoBackButton.png").convert_alpha()
    gbbLocation = gobackButton.get_rect()
    gbbLocation.x = 100
    gbbLocation.y = 300
    
    # pintar el frame
    screen.blit(background, (0,0))
    screen.blit(howToPlayButton, htpbLocation)
    screen.blit(gobackButton, gbbLocation)
    
def frame4(): # aquí se muestra el how to play
    background = pygame.image.load("gameImages/HowToPlay.png").convert_alpha()
    
    # botón de continue :)
    font = pygame.font.Font(None, 30)
    continueButton = pygame.Rect(900, 600, 190, 50)
    continueButtonText = font.render("Continue", True, BLACK)
    cBmouse_pos = pygame.mouse.get_pos()
    
    if continueButton.collidepoint(cBmouse_pos):
        continueButton.inflate_ip(10,10)
        
    continueButtonColor = PURPLE if continueButton.collidepoint(cBmouse_pos) else GREEN
    
    # pintar el frame4
    screen.blit(background, (0,0))
    pygame.draw.rect(screen, continueButtonColor, continueButton)
    screen.blit(continueButtonText, (continueButton.x + 50, continueButton.y + 15))

def frame5(): #menu de los minijuegos
    global mgbLocation, qgbLocation, pgbLocation, questionsGame_completed
    background = pygame.image.load("gameImages/MenuMinigames.png").convert_alpha()
    
    
    # boton de juego de memoria
    memoryGameButton = pygame.image.load("gameImages/MemoryGameButton.png").convert_alpha()
    mgbLocation = memoryGameButton.get_rect()
    mgbLocation.x = 750
    mgbLocation.y = 200
    
    # boton del juego de preguntas de seguridad
    questionsGameButton = pygame.image.load("gameImages/QuestionsGameButton.png").convert_alpha()
    qgbLocation = questionsGameButton.get_rect()
    qgbLocation.x = 750
    qgbLocation.y = 290
    
    # boton del juego de puzzle
    puzzleGameButton = pygame.image.load("gameImages/PuzzleGameButton.png").convert_alpha()
    pgbLocation = puzzleGameButton.get_rect()
    pgbLocation.x = 750
    pgbLocation.y = 380
    
    # pintar el frame
    screen.blit(background, (0,0))
    screen.blit(memoryGameButton, mgbLocation)
    screen.blit(questionsGameButton, qgbLocation)
    screen.blit(puzzleGameButton, pgbLocation)

    

memoryGame_completed = False

def frame6(): # minijuego de memoria
    global memoryGame_completed, current  # Cambiar el estado de completado

    backgrounds = [
        pygame.image.load("gameImages/MemoryRules.png"),
        pygame.image.load("gameImages/MemoryBackground.png")
    ]
    current_background = 0

    # Configuración inicial
    font = pygame.font.Font(None, 30)
    button_width = 190
    button_height = 50
    continueButton = pygame.Rect(190, 400, button_width, button_height)
    continueButtonText = font.render("Continue", True, BLACK)

    # Botón para volver al menú de minijuegos (Go Back)
    goBackButton2 = pygame.Rect(200, 500, button_width, button_height)
    goBackButtonText = font.render("Go Back", True, BLACK)

    # Instancia del minijuego de memoria
    juego_memoria = JuegoMemoria(screen)

    def update_background():
        """Cambiar el fondo al siguiente estado."""
        nonlocal current_background
        current_background += 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Evento: Cambio de fondo al presionar Continue
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_background < len(backgrounds) - 1:  # No estamos en el último fondo
                    if continueButton.collidepoint(event.pos):
                        update_background()
                elif current_background == len(backgrounds) - 1:  # Ya estamos en el minijuego
                    juego_memoria.manejar_click(event.pos)  # Delegar eventos al juego

                # Evento: Volver al menú principal al presionar "Go Back"
                if goBackButton2.collidepoint(event.pos):
                    memoryGame_completed = True 
                    if memoryGame_completed and puzzleGame_completed and questionsGame_completed:
                        current = 8 # El juego de memoria no se ha completado
                    else:
                        current = 4  # Regresar al frame 5
                    return 

        # Dibujar la pantalla según el estado actual
        if current_background < len(backgrounds):  # Mostrar fondos de reglas o juego
            screen.blit(backgrounds[current_background], (0, 0))

        # Mostrar botón Continue en la pantalla de reglas
        if current_background == 0:
            cBmouse_pos = pygame.mouse.get_pos()
            if continueButton.collidepoint(cBmouse_pos):
                inflated = continueButton.inflate(10, 10)
                continueButtonColor = PURPLE
            else:
                continueButtonColor = GREEN
                inflated = continueButton

            pygame.draw.rect(screen, continueButtonColor, inflated)
            screen.blit(continueButtonText, (continueButton.x + 50, continueButton.y + 15))

        # Ejecutar el minijuego si estamos en la pantalla de juego
        if current_background == 1:
            juego_memoria.mostrar_cuadros()  # Dibujar el juego en pantalla

            # Verificar si el juego ha sido completado
            if juego_memoria.gana():  # Si el juego se ha completado
                memoryGame_completed = True  # El juego se ha completado

                # Mostrar el botón Go Back solo cuando el juego ha sido completado
                cBmouse_pos = pygame.mouse.get_pos()
                if goBackButton2.collidepoint(cBmouse_pos):
                    inflated = goBackButton2.inflate(10, 10)
                    goBackButtonColor = PURPLE
                else:
                    goBackButtonColor = GREEN
                    inflated = goBackButton2

                pygame.draw.rect(screen, goBackButtonColor, inflated)
                screen.blit(goBackButtonText, (goBackButton2.x + 50, goBackButton2.y + 15))

        pygame.display.flip()  # Actualizar la pantalla
        clock.tick(60)  # Controlar la tasa de fotogramas (FPS)
    
questionsGame_completed = False

def frame7(): # minijuego de security questions
    global gBBLocation, current, questionsGame_completed 
    
    
    font = pygame.font.Font(None, 30)
    backgrounds = ["gameImages/SQRules.png", "gameImages/QuestionsBackground.png"]
    current_background = 0
    continueButton = pygame.Rect(200, 400, 190, 50)
    continueButtonText = font.render("Continue", True, BLACK)

    # Instancia de SecurityQuestions
    data_file = "C:/Users/mfrey/OneDrive/Pictures/fall thieves/PREGUNTASYRESP.xlsx"
    security_questions = SecurityQuestions(screen, font, data_file, backgrounds[1])

    def update_background():
        nonlocal current_background
        current_background += 1

    # Botón para volver al menú de minijuegos
    goBackButton = pygame.image.load("gameImages/GoBackButton.png").convert_alpha()
    gBBLocation = goBackButton.get_rect()
    gBBLocation.x = 200
    gBBLocation.y = 500

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if current_background == 0 and continueButton.collidepoint(event.pos):
                    update_background()
                elif current_background == 1:
                    if security_questions.is_game_over():
                        if gBBLocation.collidepoint(event.pos):
                            questionsGame_completed = True
                            if memoryGame_completed and puzzleGame_completed and questionsGame_completed:
                                current = 8
                            else:
                                current = 4 # Regresa al menú de minijuegos
                                running = False
                            
                    else:
                        security_questions.handle_answer(event.pos)

        # Dibujar el fondo actual
        screen.blit(pygame.image.load(backgrounds[current_background]), (0, 0))

        if current_background == 0:  # Pantalla de Reglas
            cBmouse_pos = pygame.mouse.get_pos()
            if continueButton.collidepoint(cBmouse_pos):
                inflated = continueButton.inflate(10, 10)
                continueButtonColor = PURPLE
            else:
                continueButtonColor = GREEN
                inflated = continueButton

            pygame.draw.rect(screen, continueButtonColor, inflated)
            screen.blit(continueButtonText, (continueButton.x + 50, continueButton.y + 15))

        elif current_background == 1:  # Pantalla de Preguntas
            if security_questions.is_game_over():
                security_questions.show_game_over()
                screen.blit(goBackButton, gBBLocation)
            else:
                security_questions.show_question()

        pygame.display.flip()
        pygame.time.Clock().tick(60)
        
puzzleGame_completed = False
   
def frame8():      
    global gBBLocation1, puzzleGame_completed, current
    backgrounds = [
        pygame.image.load("gameImages/PuzzleRules.png"),
        pygame.image.load("gameImages/PuzzlePlayBackground.png")
    ]
    current_background = 0

    sw = True
    font = pygame.font.Font(None, 30)
    continueButton = pygame.Rect(200, 400, 190, 50)
    continueButtonText = font.render("Continue", True, BLACK)
    goBackButton = pygame.Rect(200, 400, 190, 50)
    goBackButtonText = font.render("Go Back", True, BLACK)
    
    game = Game()

    def update_background():
        nonlocal current_background
        current_background += 1

    while sw:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if current_background < len(backgrounds) - 1:
                if event.type == pygame.MOUSEBUTTONDOWN and continueButton.collidepoint(event.pos):
                    update_background()

            elif current_background == 1:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.is_game_over() and goBackButton.collidepoint(event.pos):
                        puzzleGame_completed = True  # Actualizar puzzleGame_completed
                        if memoryGame_completed and puzzleGame_completed and questionsGame_completed:
                            current = 8
                        else:
                            current = 4
                            sw = False
                    else:
                        game.handle_events(event)
                else:
                    game.handle_events(event)

        if current_background < len(backgrounds):
            screen.blit(backgrounds[current_background], (0, 0))

        if current_background < len(backgrounds) - 1:
            cBmouse_pos = pygame.mouse.get_pos()
            if continueButton.collidepoint(cBmouse_pos):
                inflated = continueButton.inflate(10, 10)
                continueButtonColor = PURPLE
            else:
                continueButtonColor = GREEN
                inflated = continueButton

            pygame.draw.rect(screen, continueButtonColor, inflated)
            screen.blit(continueButtonText, (continueButton.x + 50, continueButton.y + 15))

        if current_background == 1:
            game.update()
            game.render(screen)
            if game.is_game_over():
                game.show_game_over()
                gBmouse_pos = pygame.mouse.get_pos()
                if goBackButton.collidepoint(gBmouse_pos):
                    inflated = goBackButton.inflate(10, 10)
                    goBackButtonColor = PURPLE
                else:
                    goBackButtonColor = GREEN
                    inflated = goBackButton

                pygame.draw.rect(screen, goBackButtonColor, inflated)
                screen.blit(goBackButtonText, (goBackButton.x + 50, goBackButton.y + 15))
                
        pygame.display.flip()
        clock.tick(60)

def win():
    backgrounds = [
        pygame.image.load("gameImages/100PercentBack.png"),
        pygame.image.load("gameImages/GoodEnding.png")
    ]
    current_background = 0

    font = pygame.font.Font(None, 30)
    continueButton = pygame.Rect(590, 400, 190, 50)
    continueButtonText = font.render("Continue", True, BLACK)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop if the window is closed
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continueButton.collidepoint(event.pos):
                    running = False  # Exit the loop when the button is pressed

        # Mostrar el fondo de victoria
        screen.blit(backgrounds[current_background], (0, 0))

        # Mostrar el botón de continuar
        cBmouse_pos = pygame.mouse.get_pos()
        if continueButton.collidepoint(cBmouse_pos):
            inflated = continueButton.inflate(10, 10)
            continueButtonColor = PURPLE
        else:
            continueButtonColor = GREEN
            inflated = continueButton

        pygame.draw.rect(screen, continueButtonColor, inflated)
        screen.blit(continueButtonText, (continueButton.x + 50, continueButton.y + 15))

        pygame.display.flip()  # Actualizar la pantalla
        clock.tick(60)

def show_popup(screen, font, message):
    
    popup_rect = pygame.Rect(200, 400, 190, 50)
    button_rect = pygame.Rect(150, 170, 100, 40)
    
    # Fondo del popup
    pygame.draw.rect(screen, (0, 0, 0), popup_rect)
    pygame.draw.rect(screen, (255, 255, 255), popup_rect, 5)  

    # Mensaje en el popup
    text_surface = font.render(message, True, (255, 255, 255))
    screen.blit(text_surface, (popup_rect.x + 20, popup_rect.y + 30))

    # Botón para cerrar el popup
    pygame.draw.rect(screen, (255, 0, 0), button_rect)
    close_button_text = font.render("Cerrar", True, (255, 255, 255))
    screen.blit(close_button_text, (button_rect.x + 30, button_rect.y + 10))

    return button_rect


# Lista de frames
frames = [frame1, frame2, frame3, frame4, frame5, frame6, frame7, frame8, win]
current = 0
running = True

# El main
while running:
    # Handle events (like closing the window)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit the loop if the window is closed
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            if memoryGame_completed and puzzleGame_completed and questionsGame_completed:
                current = 8
            # frame1 (menu principal)
            if current == 0:
                if sbLocation and sbLocation.collidepoint(mouse_pos):
                    current = 1
                elif mbLocation and mbLocation.collidepoint(mouse_pos):
                    current = 2
            
            # frame2 (openingscene)
            elif current == 1:
                yesButton = pygame.Rect(590, 400, 190, 50)
                noButton = pygame.Rect(800, 401, 190, 50)
                if yesButton.collidepoint(mouse_pos):
                    current = 4
                elif noButton.collidepoint(mouse_pos):
                    current = 0
                    
            # frame3 (menu)
            elif current == 2:
                if htpbLocation and htpbLocation.collidepoint(event.pos):
                    current = 3
                elif gbbLocation and gbbLocation.collidepoint(event.pos):
                    current = 0
                    
            # frame4 (el how to play)
            elif current == 3:
                continueButton = pygame.Rect(900, 600, 190, 50)
                if continueButton.collidepoint(event.pos):
                    current = 1
                    
            # frame5 (menu de los minijuegos)
            elif current == 4:
                if mgbLocation and mgbLocation.collidepoint(event.pos):
                    # current = 5
                    if memoryGame_completed:
                        font = pygame.font.Font(None, 30)
                        button_rect = show_popup(screen, font, "Minigame already completed")
                        if button_rect.collidepoint(mouse_pos):
                            pass
                    else:
                        current = 5  
                elif qgbLocation and qgbLocation.collidepoint(event.pos):
                    if questionsGame_completed:
                        font = pygame.font.Font(None, 30)
                        button_rect = show_popup(screen, font, "Minigame already completed")
                        if button_rect.collidepoint(mouse_pos):
                            pass
                    else:
                        current = 6 
                elif pgbLocation and pgbLocation.collidepoint(event.pos):
                    if puzzleGame_completed:
                        font = pygame.font.Font(None, 30)
                        button_rect = show_popup(screen, font, "Minigame already completed")
                        if button_rect.collidepoint(mouse_pos):
                            pass
                    else:
                        current = 7
                    
            elif current == 5 and gBBLocation.collidepoint(event.pos):
                current = 4
                
                
               
                    
                
    frames[current]()

    pygame.display.flip() 
    
pygame.quit()
sys.exit()
