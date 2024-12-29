import pygame
import sys

# Inicializa Pygame
pygame.init()

# Tamaño de la ventana
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sistema de Combate RPG")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# **Fuente personalizada**
# Reemplaza 'my_font.ttf' con la ruta de tu archivo de fuente
try:
    font = pygame.font.Font("Font/Perfect DOS VGA 437 Win.ttf", 24)  # Cambia el tamaño a lo que prefieras
except FileNotFoundError:
    print("Fuente personalizada no encontrada. Usando fuente predeterminada.")
    font = pygame.font.Font(None, 32)  # Usa la fuente predeterminada de Pygame

# Fuentes
#font = pygame.font.Font(None, 32)

# Clase para un Pokémon
class Pokemon:
    def __init__(self, name, hp, level):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.level = level

    # Modifica el HP según el damage
    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

    # Devuelve True si el HP del NPC es menor o igual a 0
    def is_fainted(self):
        return self.current_hp <= 0


class NPC:
    def __init__(self, name, hp, path_portrait, personality):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.portrait = pygame.image.load(path_portrait)
        self.portrait = npc_portrait = pygame.transform.scale(self.portrait, (250, 250))  # Escala la imagen a 250x250
        self.personality = personality

    # Modifica el HP según el damage
    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

    # Devuelve True si el HP del NPC es menor o igual a 0
    def is_fainted(self):
        return self.current_hp <= 0


# Inicializa Pokémon
pikachu = Pokemon("Pikachu", 19, 5)
eevee = Pokemon("Eevee", 20, 5)

# Inicializa NPC
sra_zafiro = NPC("Sra Zafiro", 10, "portraits/sra-zafiro-d.png", "Hostil")

# Cargar imagen del NPC portrait
#npc_portrait = pygame.image.load("portraits/sra-zafiro-d.png")  # Asegúrate de que esta imagen exista
#npc_portrait = pygame.transform.scale(npc_portrait, (250, 250))  # Escala la imagen a 100x100

# Función para dibujar texto
def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Lógica de combate
def battle_turn(attacker, defender):
    damage = 5  # Daño fijo para este ejemplo
    defender.take_damage(damage)
    return f"{attacker.name} ataca causando {damage} de daño a {defender.name}!"

# Estado del juego
battle_log = []
turn = "player"  # Alterna entre "player" y "enemy"

# Bucle principal
running = True
while running:
    screen.fill(WHITE)

    # Dibujar la interfaz de combate
    pygame.draw.rect(screen, GRAY, (50, 300, 540, 150))  # Caja de texto

    # Dibujar el retrato del NPC
    screen.blit(sra_zafiro.portrait, (50, 50))  # Posición del retrato en la pantalla

    # Dibujar otros textos
    draw_text(f"{sra_zafiro.name} - HP: {sra_zafiro.current_hp}/{sra_zafiro.max_hp}", 50, 10)
    #draw_text(f"{eevee.name} - HP: {eevee.current_hp}/{eevee.max_hp}", 350, 170)
    draw_text(f"{sra_zafiro.name} dice: ", 330, 50)

    # Opciones de combate
    draw_text("Elegir una opción :", 60, 320)
    draw_text("1> Resolver  2> Escapar", 60, 360)

    # Posicion del log
    log_pos_x = 60
    log_pos_y = 400

    # Dibujar registros de batalla
    for i, log in enumerate(battle_log[-3:]):  # Solo muestra los últimos 3 mensajes
        draw_text(log, log_pos_x, log_pos_y + i * 20)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if turn == "player":
                if event.key == pygame.K_1:  # Lucha
                    log = battle_turn(sra_zafiro, eevee)
                    battle_log.append(log)
                    turn = "enemy"

            elif turn == "enemy":
                log = battle_turn(eevee, pikachu)
                battle_log.append(log)
                turn = "player"

    # Verifica si alguien ha perdido
    if pikachu.is_fainted() or eevee.is_fainted():
        winner = "Player" if not pikachu.is_fainted() else "Enemy"
        battle_log.append(f"¡{winner} gana!")
        running = False

    pygame.display.flip()

# Salir del juego
pygame.quit()
sys.exit()
