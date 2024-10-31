import flet as ft

#define temas com diferentes combinações de cores para fonte e fundo
temas = [
    [ #tema 1
        {'fonte': '#2e292e', 'fundo': '#ff7c70'},
        {'fonte': '#2e292e', 'fundo': '#b7c9a9'},
        {'fonte': '#f2dfb1', 'fundo': '#674d69'}
    ],
    [ #tema 2
        {'fonte': '#013750', 'fundo': '#00988d'},
        {'fonte': '#fef5c8', 'fundo': '#2c6b74'},
        {'fonte': '#fef5c8', 'fundo': '#013750'}
    ],
    [ #tema 3
        {'fonte': '#013750', 'fundo': '#d0ecea'},
        {'fonte': '#013750', 'fundo': '#91eced'},
        {'fonte': '#d8f5d1', 'fundo': '#586ea7'}
    ],
    [ #tema 4
        {'fonte': '#565164', 'fundo': '#9ddbca'},
        {'fonte': '#565164', 'fundo': '#92b395'},
        {'fonte': '#d8f5d1', 'fundo': '#565164'}
    ]
]

#define os botões da calculadora com seu símbolo e tema de cor
botoes = [
    {'operador': 'AC', 'tema': 0},
    {'operador': '±', 'tema': 0},
    {'operador': '%', 'tema': 0},
    {'operador': '÷', 'tema': 1},
    {'operador': '7', 'tema': 2},
    {'operador': '8', 'tema': 2},
    {'operador': '9', 'tema': 2},
    {'operador': 'x', 'tema': 1},
    {'operador': '4', 'tema': 2},
    {'operador': '5', 'tema': 2},
    {'operador': '6', 'tema': 2},
    {'operador': '-', 'tema': 1},
    {'operador': '1', 'tema': 2},
    {'operador': '2', 'tema': 2},
    {'operador': '3', 'tema': 2},
    {'operador': '+', 'tema': 1},
    {'operador': '⚙️', 'tema': 2},
    {'operador': '0', 'tema': 2},
    {'operador': '.', 'tema': 2},
    {'operador': '=', 'tema': 1},
]

#variável para definir qual tema está ativo, começa com o tema 0
tema_atual = 0

#função principal para configurar a interface da calculadora
def main(page: ft.Page):
    global result, tema_atual

    #configurações da janela da calculadora
    page.bgcolor = '#2e292e'
    page.window.resizable = False
    page.window.width = 287
    page.window.height = 410
    page.title = 'Calculadora'
    page.window.always_on_top = True

    #inicializa o display de resultado da calculadora com valor "0"
    result = ft.Text(value='0', color='white', size=20)

    #função para calcular o resultado da expressão na calculadora
    def calculate(value_at):
        try:
            #substitui 'x' por '*' e '÷' por '/' para realizar a operação
            value_at = value_at.replace('x', '*').replace('÷', '/')
            return eval(value_at)  #avalia a expressão e retorna o resultado
        except Exception as e:
            return 'Erro'  #retorna "Erro" se algo der errado

    #função para controlar o que acontece ao clicar em cada botão
    def select(e):
        global tema_atual
        value = result.value
        operador = e.control.content.value

        #verifica se é um número ou ponto para atualizar o display
        if operador.isdigit() or operador == '.':
            if value == '0':
                result.value = operador
            else:
                result.value += operador
        #verifica se o operador é AC para resetar o display para "0"
        elif operador == 'AC':
            result.value = '0'
        #verifica se é operador de cálculo e o adiciona ao display
        elif operador in ('+', '-', 'x', '÷'):
            if value[-1] in ('+', '-', 'x', '÷'):
                result.value = value[:-1] + operador  #substitui o operador
            else:
                result.value += operador  #adiciona o operador
        #verifica se o operador é "=" para calcular o resultado
        elif operador == '=':
            result.value = str(calculate(value))
        #verifica se o operador é "±" para trocar o sinal
        elif operador == '±':
            if value.startswith('-'):
                result.value = value[1:]
            else:
                result.value = '-' + value
        #verifica se o operador é "%" para calcular porcentagem
        elif operador == '%':
            result.value = str(float(value) / 100)
        #verifica se o operador é "⚙️" para trocar o tema
        elif operador == '⚙️':
            tema_atual = (tema_atual + 1) % len(temas)  #avança o tema
            atualizar_tema()

        result.update()  #atualiza o display com o valor modificado

    #função para atualizar o tema dos botões e do display
    def atualizar_tema():
        for i, btn in enumerate(keyboard.controls):
            tema = temas[tema_atual][botoes[i]['tema']]
            btn.content.color = tema['fonte']
            btn.bgcolor = tema['fundo']
            btn.update()
        result.color = temas[tema_atual][2]['fonte']  #atualiza cor do display
        result.update()

    #cria o display da calculadora
    display = ft.Row(
        width=300,
        controls=[result],
        alignment='end'
    )

    #cria os botões da calculadora e define a aparência com base no tema atual
    btn = [ft.Container(
        content=ft.Text(value=btn['operador'], color=temas[tema_atual][btn['tema']]['fonte']),
        width=55,
        height=55,
        bgcolor=temas[tema_atual][btn['tema']]['fundo'],
        border_radius=100,
        alignment=ft.alignment.center,
        on_click=select  #atribui a função de clique ao botão
    ) for btn in botoes]

    #cria o teclado da calculadora com todos os botões
    keyboard = ft.Row(
        width=250,
        wrap=True,
        controls=btn,
        alignment='end'
    )

    #adiciona o display e o teclado à página da calculadora
    page.add(display, keyboard)

#inicia a aplicação com a função main
ft.app(target=main)
