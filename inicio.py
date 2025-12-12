import pygame, sys
from button import Button
from game import batalla
from carga_personajes import cargar_v_motorcycle, cargar_z_motorcycle


pygame.init()




## ================= RECURSOS GENERALES =================
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Mortal Zero")

ruta_fuente = "fuentes/Nightmare Codehack.ttf"
sound_inicio = pygame.mixer.Sound('musica/You Can Always Come Home.mp3')


fondo_inicial = pygame.image.load("mapas/mirador.png")
fondo_inicial = pygame.transform.scale(fondo_inicial, (1280, 720))




# ============== RECURSOS PARA LAS MOTOS =================
# === POSICIONES INICIALES DE LAS MOTOS ===
pos_v_moto_x = -300
pos_z_moto_x = -450
vel_motos = 5

# ==== ANIMACIONESS =====
v_moto = cargar_v_motorcycle()
z_moto = cargar_z_motorcycle()
frame_moto = 0







# ================ PONER LA FUENTE ================
def get_font(size): 
    return pygame.font.Font("fuentes/Nightmare Codehack.ttf", size)






# ================ PANTALLA DE INICIO ================
def main_menu():
    sound_inicio.play()

    frame_moto = 0
    frame_timer = 0      #velocidad de animación
    vel_frames = 5       #Velocidad del cambio de frame

    pos_v_moto = -200
    pos_z_moto = -350
    vel_moto = 7         #velocidad a la derecha

    


    # ======== FONDO Y BOTONES ========
    while True:
        screen.blit(fondo_inicial, (0, 0)) # Pone el fondo_inicial

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 300), 
                            text_input="PLAY", font=get_font(75), base_color="#ffffff", hovering_color="#ecb511")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 500), 
                            text_input="QUIT", font=get_font(75), base_color="#ffffff", hovering_color="#ecb511")

        screen.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)




        # ============= ANIMAR MOTOS================
        global pos_v_moto_x, pos_z_moto_x

        # Avanzar frame
        frame_timer += 1
        if frame_timer >= vel_frames:    # cada vez que frame_timer llegue al límite
            frame_timer = 0
            frame_moto += 1              # avanza 1 frame de animación

        if frame_moto >= len(v_moto):
            frame_moto = 0


        # Mover hacia la derecha
        pos_v_moto += vel_moto
        pos_z_moto += vel_moto




        # ======== POSICIONES MOTOS ========
        screen.blit(z_moto[frame_moto], (pos_z_moto, 500))
        screen.blit(v_moto[frame_moto], (pos_v_moto, 520))


        # Cuando salgan completamente, que NO se sigan dibujando nunca más
        if pos_v_moto_x < 1400:   # límite derecho
            screen.blit(v_moto[frame_moto], (pos_v_moto_x, 400))

        if pos_z_moto_x < 1400:
            screen.blit(z_moto[frame_moto], (pos_z_moto_x, 420))  # un poquito más abajo

        
        


        # ================ LO QUE PASA SI PRESIONO ALGÚN BOTÓN ================
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    sound_inicio.stop()
                    pos_v_moto_x = 2000
                    pos_z_moto_x = 2000
                    batalla()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()