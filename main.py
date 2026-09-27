from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()
Sky()

for x in range(16):
    for z in range(16):
        Entity(model='cube', color=color.lime,
               texture='white_cube',
               position=(x, 0, z), collider='box')

camera.position = (7.5, 30, -14)
camera.rotation_x = 55

jogador = FirstPersonController(position=(8, 1, 2))

cores = {
    '1': color.gray,
    '2': color.orange,
    '3': color.azure,
    '4': color.yellow
}
cor_atual = cores['1']
indice_atual = '1'

#interface itens em mão

slots_ui = []
tamanho_slot = 0.08
espacamento = 0.02
largura_total = (len(cores) * tamanho_slot) + ((len(cores) - 1) * espacamento)
inicio_x = -largura_total / 2 + tamanho_slot / 2

for i, (tecla, c) in enumerate(cores.items()):
    slot = Button(
        parent=camera.ui,
        model='quad',
        color=c,
        scale=(tamanho_slot, tamanho_slot),
        position=(inicio_x + (i * (tamanho_slot + espacamento)), -0.45),
        text=tecla,
        text_color=color.black,
        text_scale=0.7
    )
    slots_ui.append(slot)

#efeito visual item selecionado
def atualizar_hotbar():
    for i, tecla in enumerate(cores.keys()):
        if tecla == indice_atual:
            slots_ui[i].scale = (tamanho_slot * 1.2, tamanho_slot * 1.2)
        else:
            slots_ui[i].scale = (tamanho_slot, tamanho_slot)

atualizar_hotbar()

#menu pausa
pausado = False
fundo_pausa = Entity(parent=camera.ui, model='quad', scale=(2, 2), color=color.rgba(0, 0, 0, 150), enabled=False)
botao_sair = Button(parent=camera.ui, model='quad', color=color.red, scale=(0.3, 0.1), position=(0, 0), text='Sair', text_color=color.white, enabled=False, on_click=application.quit)

def alternar_pausa():
    global pausado
    pausado = not pausado

    if pausado:
        application.time_scale = 0
        jogador.enabled = False
        jogador.cursor.enabled = False
        mouse.locked = False
        fundo_pausa.enabled = True
        botao_sair.enabled = True
    else:
        application.time_scale = 1
        jogador.enabled = True
        jogador.cursor.enabled = True
        mouse.locked = True
        fundo_pausa.enabled = False
        botao_sair.enabled = False

#caso caia da plataforma, o jogador volta para a posição inicial
def update():
    if jogador.y < -5:
        jogador.position = (8, 5, 8)
        jogador.gravity = 0
        invoke(setattr, jogador, 'gravity', 1, delay=0.1)

def input(key):
    global cor_atual, indice_atual

    if key == 'escape':
        alternar_pausa()
        return

    if pausado:
        return

    if key in cores:
        cor_atual = cores[key]
        indice_atual = key
        atualizar_hotbar()
        print(f"Cor selecionada: {key}")
        return

    alvo = mouse.hovered_entity
    if not alvo:
        return

    if key == 'right mouse down':
        Entity(model='cube', color=cor_atual,
               texture='white_cube',
               position=alvo.position + mouse.normal,
               collider='box')

    if key == 'left mouse down':
        destroy(alvo)

app.run()