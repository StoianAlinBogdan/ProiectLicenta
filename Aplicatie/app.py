import PySimpleGUI as sg
from Generators import QRNG
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=0)
    return figure_canvas_agg



if __name__ == "__main__":

    _VARS = {'window': False}
    sg.theme('LightGrey')
    sg.set_options(element_padding=(1, 1))

    AppFont = 'Any 16'

    qrngs = QRNG()

    left_part = [
        [
            sg.Listbox(values=[x for x in qrngs.QRNGs.keys()], key='-LISTBOX-', size=(30,None), expand_y=True, enable_events=True)
        ]
    ]
    right_part = [
        [
            sg.Canvas(key='-CANVAS-')
        ],
        [
            sg.Button('Generate', )
        ]
    ]

    menu_def = [['&Mode',  ['Simulated', 'Real']], ['&Help']]
    layout = [
        [sg.Menu(menu_def, tearoff=False, key='-MENU-', font=AppFont)],
        [sg.Column(left_part, expand_y=True), sg.VSeparator(), sg.Column(right_part, element_justification='center')]
    ]

    '''

    '''
    fig = plt.figure()

    _VARS['window'] = sg.Window(
                        'TheWindow',
                        layout,
                        finalize=True,
                        resizable=True,

    )
    draw_figure(_VARS['window']['-CANVAS-'].TKCanvas, fig)
    _VARS['window']['-LISTBOX-'].update(set_to_index=[0])
    while True:
        event, values = _VARS['window'].read(timeout=500)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == '-LISTBOX-':
            generator_string = values['-LISTBOX-'][0]
            sg.eprint(generator_string)
        if event == 'Generate':
            if values['-LISTBOX-'][0] == 'Hadamard1Bit':
                nums = qrngs.run_Hadamard_1bit(10000)
                unique_nums = list(set(nums))
                my_counts1 = {x: nums.count(x) for x in unique_nums}
                plt.close(fig)
                fig = plt.figure()
                plt.bar(my_counts1.keys(), my_counts1.values(), width=1) 
                draw_figure(_VARS['window']['-CANVAS-'].TKCanvas, fig)


    _VARS['window'].close()


