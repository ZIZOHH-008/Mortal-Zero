import pygame
import carga_personajes
import final

pygame.init()






# ================================= VENTANA Y FPS =================================
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
FPS = 30
ruta_fuente = "fuentes/Nightmare Codehack.ttf"
last_time = 1200





### ================================= ZONA DE CARGA DE ARCHIVOS =================================
## ================= Música =================
sound_inicio = pygame.mixer.Sound('musica/You Can Always Come Home.mp3')
sound_mapas = pygame.mixer.Sound('musica/Loonboon.mp3')
sound_batalla = pygame.mixer.Sound('musica/mantis.mp3')
sound_final = pygame.mixer.Sound('musica/Ghost Fight.mp3')
sound_shoot = pygame.mixer.Sound('musica/gun_attack.mp3')
sound_katana = pygame.mixer.Sound('musica/katana_attack.mp3')

## ================= Fondos =================
fondo_pelea = pygame.image.load("mapas/acantilado.png")
fondo_pelea= pygame.transform.scale(fondo_pelea, (1280,720))

## =================Personajes=================
# Personaje 1 - V
v_run = carga_personajes.cargar_v_run()
v_quieto = carga_personajes.cargar_v_quieto()
v_shoot = carga_personajes.cargar_v_shoot()
bala_png = carga_personajes.bala()
v_fail = carga_personajes.cargar_v_fail()
v_laugh = carga_personajes.cargar_v_laugh()
v_motorcycle = carga_personajes.cargar_v_motorcycle()



# Personaje 2 - Zero
z_run = carga_personajes.cargar_z_run()
z_quieto = carga_personajes.cargar_z_quieto()
z_attack = carga_personajes.cargar_z_attack()
z_jump = carga_personajes.cargar_z_jump()
z_dash = carga_personajes.cargar_z_dash()
z_fail =carga_personajes.cargar_z_fail()
z_motorcycle = carga_personajes.cargar_z_motorcycle()
z_victory = carga_personajes.cargar_z_victory()














####=============================== LA BATALLA =================================


def batalla():
    global clock, FPS, last_time, sound_mapas, sound_batalla, sound_final, sound_shoot, sound_katana, fondo_pelea
    global v_run, v_quieto , v_shoot, z_run, z_quieto, z_attack, x, y, speed, rect_v_run, frame_v, frame_speed_v 
    global animacion_v_inicial, vel_ataque_v, rect_z_run, vel_ataque_z, frame_z, frame_speed_z, animacion_z_inicial
    global vel_correr, vida_v, vida_z, cooldown_golpe_z, ultimo_golpe_z





    ## ================ ATRIBUTOS DEL PERSONAJE ===============

    # ================== Personaje 1 - V ==================
    x, y = 150, 620                     #Posición en la pantalla
    speed = 10                                       #Velocidad
    rect_v_run = v_run[0].get_rect(center=(x, y))  #Rectangulo del personaje (para mover)

    frame_v = 0                                       #Inicia en la foto 1
    frame_speed_v = 0.2                               #Que tan rápido cambia el frame
    animacion_v_inicial= v_quieto                    #La animación inicial es V_quieto
    vel_ataque_v = 0.5 
    vida_v = 5
    jumping_v = False

    last_jump_v = 0      # tiempo del último salto de V
    jump_cooldown_v = 600  # 0.5 segundos de espera
    jump_key_down_v = False
    v_vel_y = 0



    # ================== Personaje 2 - Zero ==================
    x, y = 150, 620                     #Posición en la pantalla                                
    rect_z_run = z_run[0].get_rect(center=(x+900, y))
    vel_ataque_z = 0.20
    vida_z = 5
    cooldown_golpe_z = 2000   # milisegundos de espera entre golpes
    ultimo_golpe_z = 0   

    frame_z = 0                                       #Inicia en la foto 1
    frame_speed_z = 0.2                               #Que tan rápido cambia el frame
    animacion_z_inicial = z_quieto
    vel_correr = 0.18
    jumping_z = False
    last_jump_z = 0      # tiempo del último salto de Zero
    jump_cooldown_z = 1000  # milisegundos de espera entre saltos
    jump_key_down_z = False
    z_vel_y = -30
    


    # ================== General ==================
    balas = []
    jump_speed = -18   # velocidad inicial del salto
    gravity = 1        # gravedad
    is_dashing = False
    dash_index = 0
    dash_distance_total = 100  # píxeles que se mueve en un dash
    dash_distance_done = 0
    dash_speed = 10
    dash_cooldown_z = 1000
    last_dash_z = 0
        
  


    # ========= Pausar la que había y poner nueva ============
    sound_final.stop()
    sound_batalla.play()

    running = True
    while running:

        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sound_final.stop()
                sound_inicio.play()
                running = False



        ### =========================== PRESIONAR TECLAS ============================
        current_time = pygame.time.get_ticks()

        keys = pygame.key.get_pressed()
        moving_v = False               #La posicion inicial es NO moverse
        moving_v_shoot= False

        moving_z = False
        moving_z_attack = False



        ## ======== V ========
        if keys[pygame.K_a]:
            rect_v_run.x -= speed
            moving_v = True
        if keys[pygame.K_d]:
            rect_v_run.x += speed
            moving_v = True
        if keys[pygame.K_f]:
            moving_v_shoot = True
            if current_time - last_time >= 1500:
                bala_img = carga_personajes.bala()
                bala_rect = bala_img.get_rect(center=(rect_v_run.centerx + 50, rect_v_run.centery-27))
                balas.append([bala_img, bala_rect])

                last_time = current_time
                sound_shoot.play()

        ## ==== Salto V ====
        ground_v = 620

        if keys[pygame.K_w]:
            if not jump_key_down_v and not jumping_v and pygame.time.get_ticks() - last_jump_v >= jump_cooldown_v:
                jumping_v = True
                v_vel_y = jump_speed
                animacion_v_inicial = v_quieto  # solo se levanta
                frame_v = 0
                last_jump_v = pygame.time.get_ticks()
            jump_key_down_v = True
        else:
            jump_key_down_v = False

        # ===== Física del salto de V ======
        if jumping_v:
            v_vel_y += gravity
            rect_v_run.y += v_vel_y
            if rect_v_run.centery >= ground_v:
                rect_v_run.centery = ground_v
                jumping_v = False
                v_vel_y = 0
                animacion_v_inicial = v_quieto
                frame_v = 0
                        # reinicia el frame




        ## ## ======== ZERO ========
        if keys[pygame.K_LEFT]:
            rect_z_run.x -= speed
            moving_z = True
        if keys[pygame.K_RIGHT]:
            rect_z_run.x += speed
            moving_z = True
        if keys[pygame.K_p]:
            moving_z_attack = True
            if current_time - last_time >= 700:
                last_time = current_time
                sound_katana.play()
        if keys[pygame.K_RSHIFT]:
            if not is_dashing and pygame.time.get_ticks() - last_dash_z >= dash_cooldown_z:
                is_dashing = True
                dash_index = 0
                dash_distance_done = 0
                last_dash_z = pygame.time.get_ticks()
        
        ## ===== Salto ZERO ======
        ground_z = 620

        if keys[pygame.K_UP]:
            if not jump_key_down_z and not jumping_z and pygame.time.get_ticks() - last_jump_z >= jump_cooldown_z:
                jumping_z = True
                z_vel_y = jump_speed
                animacion_z_inicial = z_jump
                frame_z = 0
                last_jump_z = pygame.time.get_ticks()
            jump_key_down_z = True
        else:
            jump_key_down_z = False

        # Física del salto
        if jumping_z:
            z_vel_y += gravity
            rect_z_run.y += z_vel_y
            if rect_z_run.centery >= ground_z:
                rect_z_run.centery = ground_z
                jumping_z = False
                z_vel_y = 0
                animacion_z_inicial = z_quieto
                frame_z = 0


    # ================== LIMITES DE PANTALLA ==================
        # Limite para V
        if rect_v_run.left < 0:
            rect_v_run.left = 0
        if rect_v_run.right > 1280:
            rect_v_run.right = 1280

        # Limite para Zero
        if rect_z_run.left < 0:
            rect_z_run.left = 0
        if rect_z_run.right > 1280:
            rect_z_run.right = 1280




        ### ========= ANIMACIONES AL MOVERSE ==========
        ## ===== V =====

        if moving_v_shoot:
            if animacion_v_inicial!= v_shoot:
                frame_v = 0                   #Pone el frame en la primer imagen
            animacion_v_inicial = v_shoot       #Corre desde el frame 1 (por lo anterior)
            frame_speed_v = vel_ataque_v
        elif moving_v:
            animacion_v_inicial = v_run
            frame_speed_v = 0.25
        else:
            if animacion_v_inicial!= v_quieto:
                frame_v = 0
            animacion_v_inicial = v_quieto

        frame_v += frame_speed_v              # controla qué tan rápido cambia la imagen
        if frame_v >= len(animacion_v_inicial): 
            frame_v = 0                         # Si el índice supera la cantidad de imágenes reinicia la animación para que vuelva al primer frame
        animacion_v_actual = animacion_v_inicial[int(frame_v)]   # Selecciona la imagen actual usando el frame convertido a entero

    

        ## ===== ZERO =====
        if moving_z_attack:
            if animacion_z_inicial != z_attack:
                frame_z = 0                   #Pone el frame en la primer imagen
            animacion_z_inicial = z_attack       #Corre desde el frame 1 (por lo anterior)
            frame_speed_z = vel_ataque_z
        elif is_dashing:
            animacion_z_inicial = z_dash
            frame_speed_z = 0.5
            rect_z_run.x -= dash_speed   # mueve el personaje
            dash_distance_done += dash_speed
            frame_z += frame_speed_z
            if frame_z >= len(animacion_z_inicial):
                frame_z = 0
            animacion_z_actual = animacion_z_inicial[int(frame_z)]
            
            if dash_distance_done >= dash_distance_total:
                is_dashing = False  # termina el dash
                animacion_z_inicial = z_quieto
                frame_z = 0  
        elif moving_z:
            animacion_z_inicial = z_run
            frame_speed_z = vel_correr 
        else:
            if animacion_z_inicial!= z_quieto:
                frame_z = 0
            animacion_z_inicial = z_quieto

        frame_z += frame_speed_z              # controla qué tan rápido cambia la imagen
        if frame_z >= len(animacion_z_inicial): 
            frame_z = 0                         # Si el índice supera la cantidad de imágenes reinicia la animación para que vuelva al primer frame
        animacion_z_actual = animacion_z_inicial[int(frame_z)]  





    # =============== DAÑO DE PERSONAJES ===================
        # ==== De V a Zero =====
        for bala in balas[:]:  # [:] para poder eliminar dentro del bucle
            bala[1].x += 20  # velocidad de la bala

            # Colisión con Z
            if bala[1].colliderect(rect_z_run):
                vida_z -= 1
                balas.remove(bala)  # eliminar bala que impactó

            # Eliminar balas que salgan de la pantalla
            elif bala[1].right > screen.get_width():
                balas.remove(bala)


        # ====== De Zero a V ======
        current_time = pygame.time.get_ticks()

        if rect_z_run.colliderect(rect_v_run) and animacion_z_inicial == z_attack:
            if current_time - ultimo_golpe_z >= cooldown_golpe_z:
                vida_v -= 1
                ultimo_golpe_z = current_time

    



    #======= ELEGIR GANADOR Y PERDEDOR=======
        pos_v_muerte = None
        pos_z_muerte = None

        if vida_v <= 0:
            pos_v_muerte = rect_v_run.topleft     # Guarda la ultima posición
            pos_z_muerte = rect_z_run.topleft

            sound_batalla.stop()
            sound_final.play()
            final.again("ZERO", pos_v_muerte, pos_z_muerte)
            return batalla()

        
        elif vida_z <= 0:
            pos_v_muerte = rect_v_run.topleft     # Guarda la ultima posición
            pos_z_muerte = rect_z_run.topleft

            sound_batalla.stop()
            sound_final.play()
            final.again("V", pos_v_muerte, pos_z_muerte)
            return batalla()
        



    #=================== AQUÍ DIBUJO COSAS (IMPERATIVAMENTE) ===================
        screen.blit(fondo_pelea, (0, 0))   
        screen.blit(animacion_v_actual, rect_v_run)
        screen.blit(animacion_z_actual, rect_z_run)

        for bala in balas:
            screen.blit(bala[0], bala[1])






    # ====================== MOSTRAR VIDA POR CUADRITOS ============================
        fuente_name = pygame.font.Font(ruta_fuente, 50)

        # ====== V =======
        nombre_v = fuente_name.render("V", True, (236, 181, 17))  # Color #ecb511
        screen.blit(nombre_v, (50, 50))

        # Dibujar rectángulos por cada vida de V
        for i in range(vida_v):
            rect = pygame.Rect(120 + i*40, 50, 35, 50)  # 40 = separación
            pygame.draw.rect(screen, (158, 3, 3), rect)



        # ====== ZERO =======
        nombre_z = fuente_name.render("Zero", True, (0, 26, 64))
        screen.blit(nombre_z, (50, 120))

        # Dibujar rectángulos por cada vida de Zero
        for i in range(vida_z):
            rect = pygame.Rect(170 + i*40, 120, 35, 50)
            pygame.draw.rect(screen, (158, 3, 3), rect)



        pygame.display.update()

    sound_batalla.stop()