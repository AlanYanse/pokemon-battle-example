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

# Fuente personalizada
try:
    font = pygame.font.Font("Font/Perfect DOS VGA 437 Win.ttf", 24)  # Cambia el tamaño a lo que prefieras
except FileNotFoundError:
    print("Fuente personalizada no encontrada. Usando fuente predeterminada.")
    font = pygame.font.Font(None, 32)

# Clase para un Player
class Player:
    def __init__(self, name, hp, level):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.level = level

    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

    def is_fainted(self):
        return self.current_hp <= 0

# Clase para un NPC
class NPC:
    def __init__(self, name, hp, path_portrait, personality):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.portrait = pygame.image.load(path_portrait)
        self.portrait = pygame.transform.scale(self.portrait, (250, 250))  # Escala la imagen a 250x250
        self.personality = personality

    def take_damage(self, damage):
        self.current_hp = max(0, self.current_hp - damage)

    def is_fainted(self):
        return self.current_hp <= 0

# Instancia player
player = Player("player", 20, "trainer")

# Instancia NPC
sra_zafiro = NPC("Sra Zafiro", 10, "portraits/sra-zafiro-d.png", "Hostil")

# Función para dibujar texto
def draw_text(text, x, y, color=BLACK):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Función para wrappear el texto en ventana
def draw_wrapped_text(text, x, y, max_width, color=BLACK):
    """
    Dibuja texto ajustado a un ancho máximo.
    :param text: El texto a dibujar.
    :param x: Posición x en la pantalla.
    :param y: Posición y en la pantalla.
    :param max_width: Ancho máximo permitido para el texto.
    :param color: Color del texto.
    """
    words = text.split()  # Divide el texto en palabras
    lines = []  # Almacena las líneas ajustadas
    current_line = ""

    # Crea líneas ajustadas al ancho máximo
    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word

    # Agrega la última línea
    if current_line:
        lines.append(current_line)

    # Dibuja las líneas ajustadas
    for i, line in enumerate(lines):
        line_surface = font.render(line, True, color)
        screen.blit(line_surface, (x, y + i * font.get_linesize()))


# Estado del juego
battle_log = []
menu_state = "main_menu"  # Estados posibles: "main_menu", "resolver_menu"
turn = "player"  # Alterna entre "player" y "enemy"

# Bucle principal
running = True
while running:
    screen.fill(WHITE)

    # Dibujar el retrato del NPC
    screen.blit(sra_zafiro.portrait, (50, 50))  # Posición del retrato en la pantalla

    # Dibujar los elementos según el estado del menú
    if menu_state == "main_menu":
        draw_text(f"{sra_zafiro.name} - HP: {sra_zafiro.current_hp}/{sra_zafiro.max_hp}", 50, 10)
        draw_text(f"{sra_zafiro.name} dice: ", 330, 50)
        draw_wrapped_text("Dale que me anda para la M1#rd4 la computadora!", 330, 90, WIDTH - 340)
        draw_text("Elegir una opción :", 60, 320)
        draw_text("1> Resolver  2> Escapar", 60, 360)
    elif menu_state == "resolver_menu":
        draw_text(f"{sra_zafiro.name} - HP: {sra_zafiro.current_hp}/{sra_zafiro.max_hp}", 50, 10)
        draw_text(f"{sra_zafiro.name} dice: ", 330, 50)
        draw_text("Elegir una opción :", 60, 320)
        draw_text("1> Reiniciar la PC", 60, 360)

    # Dibujar registros de batalla
    log_pos_x = 60
    log_pos_y = 400
    for i, log in enumerate(battle_log[-3:]):  # Solo muestra los últimos 3 mensajes
        draw_text(log, log_pos_x, log_pos_y + i * 20)

    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if menu_state == "main_menu":
                if event.key == pygame.K_1:  # Resolver
                    menu_state = "resolver_menu"
                elif event.key == pygame.K_2:  # Escapar
                    battle_log.append("¡Has escapado!")
                    running = False
            elif menu_state == "resolver_menu":
                if event.key == pygame.K_1:  # Reiniciar la PC
                    battle_log.append("Reiniciar la PC fué efectivo...")
                elif event.key == pygame.K_2:  # Negociar
                    battle_log.append("Intentas negociar con el NPC...")
                elif event.key == pygame.K_3:  # Atacar
                    battle_log.append("Decides atacar al NPC...")
                    menu_state = "main_menu"  # Regresa al menú principal

    pygame.display.flip()

# Salir del juego
pygame.quit()
sys.exit()
