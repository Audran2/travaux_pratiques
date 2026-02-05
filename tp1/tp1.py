import turtle

from word2number import w2n

from turtle_animate import animate_entry

# --------- CONFIG ------------
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800

FORMES_DISPO = ["cercle", "carre", "triangle", "banane"]

COULEURS = {
    "rouge": "#FF0000", "bleu": "#0000FF", "vert": "#00FF00",
    "jaune": "#FFFF00", "noir": "#000000", "violet": "#FF00FF",
    "orange": "#FFA500", "rose": "#FFC0CB", "cyan": "#00FFFF"
}

POSITIONS = {
    "centre": (0, 0),
    "hautGauche": (-300, 200),
    "hautDroite": (300, 200),
    "basGauche": (-300, -200),
    "basDroite": (300, -200),
}
# --------------------------

def draw_square(t, size):
    for _ in range(4):
        t.forward(size)
        t.left(90)

def draw_triangle(t, size):
    for _ in range(3):
        t.forward(size)
        t.left(120)

def draw_circle(t, size):
    t.circle(size/2)

def draw_banana(t, size):
    t.setheading(-45)
    t.circle(size, 90)
    t.left(90)
    t.circle(size, 90)
    t.setheading(0)


def draw_shape_dispatch(t, forme, size, fill_c, border_c):
    t.color(border_c, fill_c)
    t.pensize(3)

    t.begin_fill()
    if forme == 'carre':
        draw_square(t, size)
    elif forme == 'cercle':
        draw_circle(t, size)
    elif forme == 'triangle':
        draw_triangle(t, size)
    elif forme == 'banane':
        draw_banana(t, size)
    t.end_fill()


def parse_input(text_input):
    parts = text_input.split()
    if len(parts) != 5:
        raise ValueError("Il faut 5 éléments (Nb Forme Remplissage Contour Position)")

    try:
        nb = w2n.word_to_num(parts[0])
    except ValueError:
        nb = int(parts[0])

    raw_forme = parts[1].lower().replace('é', 'e')
    if raw_forme not in FORMES_DISPO:
        raise ValueError(f"Forme inconnue. Dispo: {FORMES_DISPO}")
    forme = raw_forme

    c_fill = COULEURS.get(parts[2].lower())
    c_border = COULEURS.get(parts[3].lower())
    if not c_fill or not c_border:
        raise ValueError(f"Couleur inconnue. Utilisez: {list(COULEURS.keys())}")

    pos_key = parts[4]
    pos_found = next((v for k, v in POSITIONS.items() if k.lower() == pos_key.lower()), None)

    if pos_found is None:
        raise ValueError(f"Position inconnue. Dispo: {list(POSITIONS.keys())}")

    return nb, forme, c_fill, c_border, pos_found


def process_command(screen, turtle_obj, user_input):
    try:
        nb, forme, c_fill, c_border, (start_x, start_y) = parse_input(user_input)

        taille_forme = 50
        espacement = 70

        largeur_totale = (nb * taille_forme) + ((nb - 1) * (espacement - taille_forme))
        current_x = start_x - (largeur_totale / 2)

        print(f"Dessin de {nb} {forme}(s)")

        for i in range(nb):
            if abs(current_x) > (SCREEN_WIDTH / 2) - 50:
                print(f"Forme {i + 1} hors limite, ignorée.")
                current_x += espacement
                continue

            animate_entry(turtle_obj, current_x, start_y)
            draw_shape_dispatch(turtle_obj, forme, taille_forme, c_fill, c_border)

            current_x += espacement

    except Exception as e:
        print(f"Erreur : {e}")


def main():
    screen = turtle.Screen()
    screen.setup(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
    screen.title("Générateur de Formes - Animation Originale")

    t = turtle.Turtle()
    t.hideturtle()

    running = True
    while running:
        user_input = screen.textinput(
            "Commande",
            "Format: Nb Forme CouleurRemplissage CouleurBordure Position\n"
            "(ex: 3 banane jaune noir centre)"
        )

        if user_input is None or user_input.lower() == 'quitter':
            running = False
            break

        t.clear()

        commandes = user_input.split(',')
        for cmd in commandes:
            process_command(screen, t, cmd.strip())

    screen.bye()


if __name__ == "__main__":
    main()
