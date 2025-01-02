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
BLUE = (0, 0, 255)

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


# Opciones del menú
menu_options = ["Resolver", "Escapar"]
selected_option = 0  # Índice de la opción seleccionada

# Función para dibujar el menú con opciones resaltadas
def draw_menu(options, selected_index, x, y, color=BLACK, selected_color=WHITE, rect_color=BLUE):
    """
    Dibuja un menú con opciones y resalta la opción seleccionada con un rectángulo.
    :param options: Lista de opciones.
    :param selected_index: Índice de la opción seleccionada.
    :param x: Posición x del menú.
    :param y: Posición y del menú.
    :param color: Color del texto no seleccionado.
    :param selected_color: Color del texto seleccionado.
    :param rect_color: Color del rectángulo de selección.
    """
    for i, option in enumerate(options):
        option_text = f"> {option}" if i == selected_index else option
        text_surface = font.render(option_text, True, selected_color if i == selected_index else color)
        text_width, text_height = text_surface.get_size()

        # Dibuja el rectángulo si es la opción seleccionada
        if i == selected_index:
            pygame.draw.rect(screen, rect_color, (x - 10, y + i * 40 - 5, text_width + 20, text_height + 10))

        # Dibuja el texto
        screen.blit(text_surface, (x, y + i * 40))


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
menu_state = "main_menu"  # Estados posibles: "main_menu", "resolver_menu", "reward_screen"
turn = "player"  # Alterna entre "player" y "enemy"
sra_zafiro_text = "Dale que me anda para la M1#rd4 la computadora!"  # Texto inicial de Sra Zafiro

# Bucle principal
running = True
while running:
    screen.fill(WHITE)

    # Dibujar los elementos según el estado del menú
    if menu_state == "main_menu":
        screen.blit(sra_zafiro.portrait, (50, 50))  # Posición del retrato en la pantalla
        draw_text(f"{sra_zafiro.name} - HP: {sra_zafiro.current_hp}/{sra_zafiro.max_hp}", 50, 10)
        draw_text(f"{sra_zafiro.name} dice: ", 330, 50)
        draw_wrapped_text(sra_zafiro_text, 330, 90, WIDTH - 340)
        draw_text("Elegir una opción :", 60, 320)
        #draw_text("1> Resolver  2> Escapar", 60, 360)
        draw_menu(menu_options, selected_option, 60, 360)  # Dibuja el menú con opciones
    elif menu_state == "resolver_menu":
        menu_options = ["Reiniciar la PC"]
        screen.blit(sra_zafiro.portrait, (50, 50))  # Posición del retrato en la pantalla
        draw_text(f"{sra_zafiro.name} - HP: {sra_zafiro.current_hp}/{sra_zafiro.max_hp}", 50, 10)
        draw_text(f"{sra_zafiro.name} dice: ", 330, 50)
        draw_wrapped_text(sra_zafiro_text, 330, 90, WIDTH - 340)  # Asegurarse de que el texto se actualice aquí también.
        draw_text("Elegir una opción :", 60, 320)
        #draw_text("1> Reiniciar la PC", 60, 360)
        draw_menu(menu_options, selected_option, 60, 360)  # Dibuja el menú con opciones
    elif menu_state == "reward_screen":
        draw_text("Bien hecho!", 60, 60)
        draw_text("Recompensas:", 60, 100)
        draw_text("Has ganado 100 de experiencia", 60, 140)
        draw_text("Ahora eres un Junior", 60, 180)
        draw_text("Has ganado 1000 pe", 60, 220)
        draw_text("Has destrabado gpupdate", 60, 260)
        draw_text("Presiona enter para continuar.", 120, 320)
        draw_text("...Fin...", 60, 420)

    # Dibujar registros de batalla solo si no estamos en la pantalla de recompensas
    if menu_state != "reward_screen":
        log_pos_x = 60
        log_pos_y = 400
        for i, log in enumerate(battle_log[-3:]):  # Solo muestra los últimos 3 mensajes
            draw_text(log, log_pos_x, log_pos_y + i * 20)

    # Manejo de eventos
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if menu_state == "main_menu":
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)  # Mover hacia arriba
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)  # Mover hacia abajo
                elif event.key == pygame.K_RETURN:  # Seleccionar opción
                    if selected_option == 0:  # Resolver
                        menu_state = "resolver_menu"
                    elif selected_option == 1:  # Escapar
                        battle_log.append("¡Has escapado!")
                        running = False
            elif menu_state == "resolver_menu":
                if event.key == pygame.K_RETURN and sra_zafiro_text != "chau":  # Reiniciar la PC
                    battle_log.append("Reiniciar la PC fue efectivo...")
                    sra_zafiro.take_damage(10)
                    sra_zafiro_text = "chau"  # Actualiza el texto de Sra Zafiro
                    battle_log.append("Presiona enter para continuar...")
                elif event.key == pygame.K_RETURN and sra_zafiro_text == "chau":  # Presionar Enter después de "chau"
                    menu_state = "reward_screen"
            elif menu_state == "reward_screen":
                if event.key == pygame.K_RETURN:  # Presionar Enter en la pantalla de recompensas
                    running = False  # O puedes cambiar a otro estado o acción

    pygame.display.flip()

# Salir del juego
pygame.quit()
sys.exit()
