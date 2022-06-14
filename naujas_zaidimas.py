import pygame
import os
pygame.font.init()
pygame.mixer.init()

PLOTIS, AUKSTIS = 900, 500
LANGAS = pygame.display.set_mode((PLOTIS, AUKSTIS))
pygame.display.set_caption('Žaidimas')

BALTA = (255, 255, 255)
JUODA = (0, 0, 0)
RAUDONA = (255, 0, 0)
GELTONA = (255, 255, 0)

LINIJA = pygame.Rect(PLOTIS // 2 - 5, 0, 10, AUKSTIS)

KULKA_HIT_GARSAS = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
KULKA_FIRE_GARSAS = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

GYVYBIU_TEKSTAS = pygame.font.SysFont('comicsans', 40)
LAIMETOJO_TEKSTAS = pygame.font.SysFont('comicsans', 100)

ERDVELAIVIO_PLOTIS, ERDVELAIVIO_ILGIS = 55, 40

GELTONAS_PATAIKYTAS = pygame.USEREVENT + 1
RAUDONAS_PATAIKYTAS = pygame.USEREVENT + 2

FPS = 60
GREITIS = 5
KULKOS_GREITIS =  7
KULKU_SKAICIUS = 3

GELTONAS_ERDVELAIVIS_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
GELTONAS_ERDVELAIVIS = pygame.transform.rotate(pygame.transform.scale
                                           (GELTONAS_ERDVELAIVIS_IMAGE, (ERDVELAIVIO_PLOTIS, ERDVELAIVIO_ILGIS)), 90)
RAUDONAS_ERDVELAIVIS_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RAUDONAS_ERDVELAIVIS = pygame.transform.rotate(pygame.transform.scale(RAUDONAS_ERDVELAIVIS_IMAGE,
                                                                      (ERDVELAIVIO_PLOTIS, ERDVELAIVIO_ILGIS)), 270)

FONAS = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (PLOTIS, AUKSTIS))

def lango_parametrai(raudona, geltona, raudona_kulka, geltona_kulka, raudono_gyvybes, geltono_kulkos):
    LANGAS.blit(FONAS, (0, 0))
    pygame.draw.rect(LANGAS, JUODA, LINIJA)

    raudono_gyvybiu_tekstas = GYVYBIU_TEKSTAS.render('Gyvybės: ' + str(raudono_gyvybes), 1, BALTA)
    geltono_gyvybiu_tekstas = GYVYBIU_TEKSTAS.render('Gyvybės: ' + str(geltono_kulkos), 1, BALTA)
    LANGAS.blit(raudono_gyvybiu_tekstas, (PLOTIS - raudono_gyvybiu_tekstas.get_width() - 10, 10))
    LANGAS.blit(geltono_gyvybiu_tekstas, (10, 10))

    LANGAS.blit(GELTONAS_ERDVELAIVIS, (geltona.x, geltona.y))
    LANGAS.blit(RAUDONAS_ERDVELAIVIS, (raudona.x, raudona.y))

    for kulka in raudona_kulka:
        pygame.draw.rect(LANGAS, RAUDONA, kulka)

    for kulka in geltona_kulka:
        pygame.draw.rect(LANGAS, GELTONA, kulka)

    pygame.display.update()

def geltono_valdymas(paspaustas_mygtukas, geltona):
    if paspaustas_mygtukas[pygame.K_a] and geltona.x - GREITIS > 0:  # kaire
        geltona.x -= GREITIS
    if paspaustas_mygtukas[pygame.K_d] and geltona.x  + GREITIS + geltona.height < LINIJA.x:  # desine
        geltona.x += GREITIS
    if paspaustas_mygtukas[pygame.K_w] and geltona.y  - GREITIS > 0:  # virsus
        geltona.y -= GREITIS
    if paspaustas_mygtukas[pygame.K_s] and geltona.y  + GREITIS + geltona.width < AUKSTIS:  # apacia
        geltona.y += GREITIS

def raudono_valdymas(paspaustas_mygtukas, raudona):
    if paspaustas_mygtukas[pygame.K_LEFT] and raudona.x - GREITIS > LINIJA.x + LINIJA.width:  # kaire
        raudona.x -= GREITIS
    if paspaustas_mygtukas[pygame.K_RIGHT] and raudona.x  + GREITIS + raudona.height < PLOTIS:  # desine
        raudona.x += GREITIS
    if paspaustas_mygtukas[pygame.K_UP] and raudona.y  - GREITIS > 0:  # virsus
        raudona.y -= GREITIS
    if paspaustas_mygtukas[pygame.K_DOWN] and raudona.y  + GREITIS + raudona.width < AUKSTIS:  # apacia
        raudona.y += GREITIS

def kulku_parametrai(geltono_kulkos, raudono_kulkos, geltona, raudona):
    for kulka in geltono_kulkos:
        kulka.x += KULKOS_GREITIS
        if raudona.colliderect(kulka):
            pygame.event.post(pygame.event.Event(RAUDONAS_PATAIKYTAS))
            geltono_kulkos.remove(kulka)
        elif kulka.x > PLOTIS:
            geltono_kulkos.remove(kulka)

    for kulka in raudono_kulkos:
        kulka.x -= KULKOS_GREITIS
        if geltona.colliderect(kulka):
            pygame.event.post(pygame.event.Event(GELTONAS_PATAIKYTAS))
            raudono_kulkos.remove(kulka)
        elif kulka.x < 0:
            raudono_kulkos.remove(kulka)

def parodyti_laimetoja(text):
    tekstas = LAIMETOJO_TEKSTAS.render(text, 1, BALTA)
    LANGAS.blit(tekstas, (PLOTIS / 2 - tekstas.get_width() / 2, AUKSTIS / 2 - tekstas.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    raudonas = pygame.Rect(600, 300, ERDVELAIVIO_PLOTIS, ERDVELAIVIO_ILGIS)
    geltonas = pygame.Rect(100, 300, ERDVELAIVIO_PLOTIS, ERDVELAIVIO_ILGIS)

    raudono_kulkos = []
    geltono_kulkos = []

    raudono_gyvybes = 10
    geltono_gyvybes = 10

    laikas = pygame.time.Clock()
    run = True
    while run:
        laikas.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and len(geltono_kulkos) < KULKU_SKAICIUS:
                    bullet = pygame.Rect(geltonas.x + geltonas.width, geltonas.y + geltonas.height // 2 - 2, 10, 5)
                    geltono_kulkos.append(bullet)
                    KULKA_FIRE_GARSAS.play()

                if event.key == pygame.K_0 and len(raudono_kulkos) < KULKU_SKAICIUS:
                    bullet = pygame.Rect(raudonas.x, raudonas.y + raudonas.height // 2 - 2, 10, 5)
                    raudono_kulkos.append(bullet)
                    KULKA_FIRE_GARSAS.play()

            if event.type == RAUDONAS_PATAIKYTAS:
                raudono_gyvybes -= 1
                KULKA_HIT_GARSAS.play()

            if event.type == GELTONAS_PATAIKYTAS:
                geltono_gyvybes -= 1
                KULKA_HIT_GARSAS.play()

        laimetojo_tekstas = ""
        if raudono_gyvybes <= 0:
            laimetojo_tekstas = 'Geltonas laimėjo'

        if geltono_gyvybes <= 0:
            laimetojo_tekstas = 'Raudonas laimėjo'

        if laimetojo_tekstas != "":
            parodyti_laimetoja(laimetojo_tekstas)
            break

        keys_pressed = pygame.key.get_pressed()
        geltono_valdymas(keys_pressed, geltonas)
        raudono_valdymas(keys_pressed, raudonas)
        kulku_parametrai(geltono_kulkos, raudono_kulkos, geltonas, raudonas)
        lango_parametrai(raudonas, geltonas, raudono_kulkos, geltono_kulkos, raudono_gyvybes, geltono_gyvybes)
    main()


if __name__ == '__main__':
    main()