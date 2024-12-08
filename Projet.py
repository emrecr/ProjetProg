import pygame
import random

elements = {
    2: "H", 4: "He", 8: "Be", 16: "C", 32: "O",
    64: "Ne", 128: "Mg", 256: "Si", 512: "S", 1024: "Cl", 2048: "Ar"
}

def init_grille(taille):
    grille = [[0] * taille for _ in range(taille)]
    for _ in range(random.randint(4, 6)):
        ajouter_tuile_aleatoire(grille)
    return grille

def ajouter_tuile_aleatoire(grille):
    taille = len(grille)
    valeur = random.choice([2, 4])
    case_vide = [(i, j) for i in range(taille) for j in range(taille) if grille[i][j] == 0]
    if case_vide:
        i, j = random.choice(case_vide)
        grille[i][j] = valeur

def deplacer_a_gauche(ligne, score):
    taille = len(ligne)
    nouvelle_ligne = [0] * taille
    position_libre = 0
    for i in range(taille):
        if ligne[i] != 0:
            if nouvelle_ligne[position_libre] == 0:
                nouvelle_ligne[position_libre] = ligne[i]
            elif nouvelle_ligne[position_libre] == ligne[i]:
                nouvelle_ligne[position_libre] *= 2
                score += nouvelle_ligne[position_libre]
                position_libre += 1
            else:
                position_libre += 1
                nouvelle_ligne[position_libre] = ligne[i]
    return nouvelle_ligne, score

def deplacer_grille_gauche(grille, score):
    taille = len(grille)
    for i in range(taille):
        grille[i], score = deplacer_a_gauche(grille[i], score)
    return score

def inverser_ligne(ligne):
    return ligne[::-1]

def deplacer_grille_droite(grille, score):
    taille = len(grille)
    for i in range(taille):
        reversed_line, score = deplacer_a_gauche(inverser_ligne(grille[i]), score)
        grille[i] = inverser_ligne(reversed_line)
    return score

def transposer_grille(grille):
    taille = len(grille)
    return [[grille[j][i] for j in range(taille)] for i in range(taille)]

def deplacer_grille_haut(grille, score):
    grille_transposee = transposer_grille(grille)
    score = deplacer_grille_gauche(grille_transposee, score)
    for i in range(len(grille_transposee)):
        for j in range(len(grille_transposee)):
            grille[j][i] = grille_transposee[i][j]
    return score

def deplacer_grille_bas(grille, score):
    grille_transposee = transposer_grille(grille)
    score = deplacer_grille_droite(grille_transposee, score)
    for i in range(len(grille_transposee)):
        for j in range(len(grille_transposee)):
            grille[j][i] = grille_transposee[i][j]
    return score

def jeu_gagnant(grille):
    for ligne in grille:
        if any(cell >= 2048 for cell in ligne):
            return True
    return False

def mouvements_possibles(grille):
    taille = len(grille)
    for i in range(taille):
        for j in range(taille):
            if grille[i][j] == 0:
                return True
    for i in range(taille):
        for j in range(taille - 1):
            if grille[i][j] == grille[i][j + 1]:
                return True
    for i in range(taille - 1):
        for j in range(taille):
            if grille[i][j] == grille[i + 1][j]:
                return True
    return False

def jouer_pygame():
    mode = input("Choisissez un mode : 'normal' (chiffres) ou 'chimique' (éléments) : ").lower()
    if mode not in ["normal", "chimique"]:
        print("Mode invalide. Par défaut, mode 'normal' sélectionné.")
        mode = "normal"

    taille_grille = int(input("Entrez la taille de la grille (ex: 4 pour 4x4) : ") or "4")

    taille_case = 100
    largeur = hauteur = taille_case * taille_grille
    marge = 10
    police = None

    pygame.init()
    fenetre = pygame.display.set_mode((largeur, hauteur))
    pygame.display.set_caption(f"2048 - Mode {mode} - Grille {taille_grille}x{taille_grille}")
    clock = pygame.time.Clock()
    police = pygame.font.Font(None, 40)

    couleurs = {
        0: (200, 200, 200), 2: (240, 240, 240), 4: (220, 220, 220), 8: (200, 180, 200),
        16: (180, 150, 240), 32: (150, 100, 240), 64: (120, 50, 220), 128: (100, 50, 180),
        256: (80, 50, 150), 512: (50, 30, 120), 1024: (30, 20, 80), 2048: (10, 10, 50)
    }

    grille = init_grille(taille_grille)
    score = 0

    def dessiner_grille():
        fenetre.fill((0, 0, 0))
        for i in range(taille_grille):
            for j in range(taille_grille):
                valeur = grille[i][j]
                couleur = couleurs.get(valeur, (50, 50, 50))
                x, y = j * taille_case, i * taille_case
                pygame.draw.rect(fenetre, couleur, (x + marge, y + marge, taille_case - marge, taille_case - marge))
                texte = str(valeur) if mode == "normal" else elements.get(valeur, "")
                if valeur > 0:
                    surface_texte = police.render(texte, True, (0, 0, 0))
                    fenetre.blit(surface_texte, (x + taille_case // 2 - surface_texte.get_width() // 2,
                                                 y + taille_case // 2 - surface_texte.get_height() // 2))

    def deplacer(direction):
        nonlocal score
        if direction == "left":
            score = deplacer_grille_gauche(grille, score)
        elif direction == "right":
            score = deplacer_grille_droite(grille, score)
        elif direction == "up":
            score = deplacer_grille_haut(grille, score)
        elif direction == "down":
            score = deplacer_grille_bas(grille, score)
        ajouter_tuile_aleatoire(grille)

    running = True
    while running:
        dessiner_grille()
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    deplacer("left")
                elif event.key == pygame.K_RIGHT:
                    deplacer("right")
                elif event.key == pygame.K_UP:
                    deplacer("up")
                elif event.key == pygame.K_DOWN:
                    deplacer("down")

        if jeu_gagnant(grille):
            print("Vous avez gagné ! Bravo !")
            running = False
        if not mouvements_possibles(grille):
            print("Game Over ! Plus de mouvements possibles.")
            running = False

        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    jouer_pygame()