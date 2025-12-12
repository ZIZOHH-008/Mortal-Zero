import pygame, sys, carga_personajes

pygame.init()



## ================= RECURSOS =================
screen = pygame.display.set_mode((1280,720))
pygame.display.set_caption("Katana Zero")

ruta_fuente = "fuentes/Nightmare Codehack.ttf"


fondo_inicial = pygame.image.load("mapas/mirador.png")
fondo_inicial = pygame.transform.scale(fondo_inicial, (1280, 720))
fondo_pelea = pygame.image.load("mapas/acantilado.png")
fondo_pelea= pygame.transform.scale(fondo_pelea, (1280,720))
v_fail = carga_personajes.cargar_v_fail()
v_laugh = carga_personajes.cargar_v_laugh()
z_fail =carga_personajes.cargar_z_fail()
z_victory = carga_personajes.cargar_z_victory()







# ================ PONER LA FUENTE ================
def get_font(size):
    return pygame.font.Font("fuentes/Nightmare Codehack.ttf", size)






### ================ LA FUNCION DE PANTALLA FINAL ================
def again(ganador, pos_v, pos_z):
    if ganador == "V":
        anim_ganador = v_laugh
        anim_perdedor = z_fail   # si Zero no tiene animaciones, usamos v_fail como placeholder
    elif ganador == "Z" or ganador == "ZERO":
        anim_ganador = z_victory
        anim_perdedor = v_fail

    frame = 0
    timer_anim = 0
    clock = pygame.time.Clock()





    # ========== CUADRO QUE TENDRÁ GANADOR Y BOTONES ==========
    ancho = 600
    alto = 320
    popup = pygame.Surface((ancho, alto))
    popup.fill((30, 30, 30))
    popup_rect = popup.get_rect(center=(640, 360))

    fuente = get_font(80)
    fuente_btn = get_font(55)




    # ======= TAMAÑO BOTONES ======= 
    btn_ancho, btn_alto = 220, 70

    # BOTON AGAIN
    btn_again = pygame.Rect(0, 0, btn_ancho, btn_alto)
    btn_again.center = (popup_rect.centerx - 140, popup_rect.centery + 60)

    # Botón QUIT
    btn_quit = pygame.Rect(0, 0, btn_ancho, btn_alto)
    btn_quit.center = (popup_rect.centerx + 140, popup_rect.centery + 60)








    # ========== BUCLE ==========
    while True:
        mouse_pos = pygame.mouse.get_pos()

        dt = clock.tick(60)
        timer_anim += dt

        screen.blit(fondo_pelea, (0, 0))  #Primero dibujo el fondo



        # ======= CONDICIONAL DE GANADOR =======
        if ganador == "V":
            pos_gan = pos_v
            pos_per = pos_z
        else:
            pos_gan = pos_z
            pos_per = pos_v



        # ===== ANIMAR =====
        screen.blit(anim_ganador[frame % len(anim_ganador)], pos_gan)
        screen.blit(anim_perdedor[frame % len(anim_perdedor)], pos_per)

        # Avanzar frame
        frame += 1
        if frame >= max(len(anim_ganador), len(anim_perdedor)):
            frame = 0



        # ===== PINTAR CUADRO CON ELEMENTOS =====
        screen.blit(popup, popup_rect)


        # Texto ganador
        texto = fuente.render(f"¡{ganador} GANA!", True, (255, 220, 80))
        screen.blit(texto, texto.get_rect(center=(popup_rect.centerx, popup_rect.centery - 40)))


        # ===== BOTÓN AGAIN =====
        color_again = (200, 200, 200) if btn_again.collidepoint(mouse_pos) else (150, 150, 150)
        pygame.draw.rect(screen, color_again, btn_again, border_radius=15)
        texto_again = fuente_btn.render("AGAIN", True, (0, 0, 0))
        screen.blit(texto_again, texto_again.get_rect(center=btn_again.center))


        # ===== BOTÓN QUIT =====
        color_quit = (200, 200, 200) if btn_quit.collidepoint(mouse_pos) else (150, 150, 150)
        pygame.draw.rect(screen, color_quit, btn_quit, border_radius=15)
        texto_quit = fuente_btn.render("QUIT", True, (0, 0, 0))
        screen.blit(texto_quit, texto_quit.get_rect(center=btn_quit.center))


        # ===== EVENTOS =====
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_again.collidepoint(mouse_pos):
                    return  # vuelve al combate

                if btn_quit.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(12)  # velocidad de animación