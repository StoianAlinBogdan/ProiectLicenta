import PySimpleGUI as sg
from Generators import QRNG
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg



if __name__ == "__main__":

    _VARS = {'window': False}
    sg.theme('LightGrey')
    sg.set_options(element_padding=(1, 1))

    AppFont = 'Any 16'

    menu_def = [['&Mode',  ['Simulated', 'Real']], ['&Help']]

    left_part = [ 
        sg.Listbox(values=['test1', 'test2', 'test3'], key='-LISTBOX-', size=(30,6), expand_y=True)
    ]
    right_part = [
        sg.Canvas(key='-CANVAS-')
    ]
    layout = [
        [sg.Menu(menu_def, tearoff=False, key='-MENU-', font=AppFont)],
        [sg.Column([left_part], expand_y=True), sg.VSeparator(), sg.Column([right_part])]
    ]


    qrngs = QRNG()
    nums = qrngs.run_Hadamard_1bit(10000)
    unique_nums = list(set(nums))
    my_counts1 = {x: nums.count(x) for x in unique_nums}
    fig = plt.figure()
    plt.bar(my_counts1.keys(), my_counts1.values(), width=1)

    _VARS['window'] = sg.Window(
                        'TheWindow',
                        layout,
                        finalize=True,
                        resizable=True,

    )
    draw_figure(_VARS['window']['-CANVAS-'].TKCanvas, fig)

    while True:
        event, values = _VARS['window'].read(timeout=200)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
    _VARS['window'].close()


