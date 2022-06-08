from enum import unique
import PySimpleGUI as sg
import Generators as gen
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

_VARS = {
    'window': False,
    'fig_agg': False,
    'plt_fig': False
    }

function_map = {
    'Hadamard1Bit': 'run_Hadamard_1bit',
    'Hadamard8Bit': 'run_Hadamard_8bit',
    'RY1Bit': 'run_RY_1bit',
    'RY8Bit': 'run_RY_8bit',
    'Uniform1Bit': 'run_Uniform_1bit',
    'Uniform8Bit': 'run_Uniform_8bit'
}

def draw_figure(canvas, figure) -> None:
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=0)
    return figure_canvas_agg


def draw_chart(data: list) -> None:
    _VARS['plt_fig'] = plt.figure()
    unique_nums = list(set(data))
    counts = {x: data.count(x) for x in unique_nums}
    plt.bar(counts.keys(), counts.values(), width=1)
    plt.title('Distribution of the numbers')
    plt.xlabel('Number')
    plt.ylabel('Frequency of number')
    _VARS['fig_agg'] = draw_figure(_VARS['window']['-CANVAS-'].TKCanvas, _VARS['plt_fig'])


def update_chart(data: list) -> None:
    _VARS['fig_agg'].get_tk_widget().forget()
    plt.clf()
    unique_nums = list(set(data))
    counts = {x: data.count(x) for x in unique_nums}    
    plt.bar(counts.keys(), counts.values(), width=1)
    plt.title('Distribution of the numbers')
    plt.xlabel('Number')
    plt.ylabel('Frequency of number')
    _VARS['fig_agg'] = draw_figure(_VARS['window']['-CANVAS-'].TKCanvas, _VARS['plt_fig'])   
    


if __name__ == "__main__":
    sg.theme('LightGrey')
    sg.set_options(element_padding=(1, 1))

    AppFont = 'Any 16'

    qrngs = gen.QRNG()

    left_part = [
        [
            sg.Listbox(values=[x for x in qrngs.QRNGs.keys()], key='-LISTBOX-', size=(30,None), expand_x=True, expand_y=True, enable_events=True)
        ]
    ]
    right_part = [
        [
            sg.Canvas(key='-CANVAS-', size=(650,550))
        ],
        [
            sg.Text("Amount of numbers: "), sg.Input(key='-NUMS-'), sg.Button('Generate', disabled=False, key='-GENERATE_BUTTON-')
        ]
    ]

    menu_def = [['&Mode',  ['Simulated', 'Real']], ['&Help']]
    layout = [
        [sg.Menu(menu_def, tearoff=False, key='-MENU-', font=AppFont)],
        [sg.Column(left_part, expand_y=True), sg.VSeparator(), sg.Column(right_part, element_justification='center')]
    ]


    _VARS['window'] = sg.Window(
                        'TheWindow',
                        layout,
                        finalize=True,
                        resizable=True,

    )
    _VARS['window']['-LISTBOX-'].update(set_to_index=[0])
    generator_string = 'Hadamard1Bit'
    while True:
        event, values = _VARS['window'].read(timeout=500)
        if values['-NUMS-'] != '':
            _VARS['window']['-GENERATE_BUTTON-'].update(disabled=False)
        else:
            _VARS['window']['-GENERATE_BUTTON-'].update(disabled=True)         
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '-LISTBOX-':
            generator_string = values['-LISTBOX-'][0]
        if event == '-GENERATE_BUTTON-':
            RNG = getattr(qrngs, function_map[generator_string])
            nums = RNG(int(values['-NUMS-']))
            if _VARS['plt_fig'] == False:
                draw_chart(nums)
            else:
                update_chart(nums)


    _VARS['window'].close()


