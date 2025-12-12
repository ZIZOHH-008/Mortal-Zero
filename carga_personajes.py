import pygame

pygame.init()


## =================Personajes=================
# Personaje 1 - V

def cargar_v_quieto():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/v_quieto/{i}.png'), (100, 100))
        for i in range(1, 5)
    ]


def cargar_v_run():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/v_run/{i}.png'), (100, 100))
        for i in range(1, 6)
    ]


def cargar_v_fail():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/v_fail/{i}.png'), (90, 90))
        for i in range(1, 8)
    ]


def cargar_v_laugh():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/v_laugh/{i}.png'), (100, 100))
        for i in range(1, 5)
    ]


def cargar_v_motorcycle():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/v_motorcycle/{i}.png'), (140, 120))
        for i in range(1, 4)
    ]



def cargar_v_shoot():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/v_shoot/{i}.png'), (125, 100))
        for i in range(1, 16)
    ]


def bala():
    return pygame.transform.scale(pygame.image.load(f'assets/bala.png'), (30, 20))





# Personaje 2 - Zero

def cargar_z_run():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/z_run/{i}.png'), (110, 100))
        for i in range(1, 6)
    ]


def cargar_z_quieto():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/z_quieto/{i}.png'), (100, 100))
        for i in range(1, 6)
    ]


def cargar_z_jump():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/z_jump/{i}.png'), (100, 100))
        for i in range(1, 5)
    ]


def cargar_z_attack():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/z_attack/{i}.png'), (130, 100))
        for i in range(1, 5)
    ]


def cargar_z_dash():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/z_dash/{i}.png'), (105, 90))
        for i in range(1, 8)
    ]


def cargar_z_fail():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/z_fail/{i}.png'), (120, 80))
        for i in range(1, 6)
    ]



def cargar_z_motorcycle():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/z_motorcycle/{i}.png'), (140, 120))
        for i in range(1, 5)
    ]


def cargar_z_victory():
    return [
        pygame.transform.scale(pygame.image.load(f'personajes/z_victory/{i}.png'), (100, 100))
        for i in range(1, 12)
    ]

