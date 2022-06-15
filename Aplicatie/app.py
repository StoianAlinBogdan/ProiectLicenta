import PySimpleGUI as sg
import Generators as gen
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import subprocess

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


def make_numbers_window():
    layout = [
        [sg.Text("Sample of your numbers: ")],
        [sg.Multiline(size=(30, 5), key='-NUMBERS_BOX-')],
        [sg.FileSaveAs("Save to file", key='-SAVE_FILE_BUTTON-', initial_folder='./', file_types=(('TXT', '.txt'),)),
         sg.Button("Copy to clipboard", key='-CLIPBOARD_COPY_BUTTON-')]
    ]
    return sg.Window('Numbers window', layout, finalize=True)
    


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
            sg.Text("Amount of numbers: "), sg.Input(key='-NUMS-'), sg.Button('Generate', disabled=True, key='-GENERATE_BUTTON-'),
            sg.Button('Get Numbers', disabled=True, key='-NUMBERS_BUTTON-')
        ]
    ]

    menu_def = [['&Mode',  ['Simulated', 'Real']], ['&Help']]
    layout_main = [
        [sg.Menu(menu_def, tearoff=False, key='-MENU-', font=AppFont)],
        [sg.Column(left_part, expand_y=True), sg.VSeparator(), sg.Column(right_part, element_justification='center')]
    ]
    tabbed_layout = [[sg.TabGroup([[sg.Tab('MainTab', layout_main)]])]]


    _VARS['window'] = sg.Window(
                        'TheWindow',
                        tabbed_layout,
                        finalize=True,
                        resizable=True)
    _VARS['numbers_window'] = None
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
            _VARS['window']['-NUMBERS_BUTTON-'].update(disabled=False)
            RNG = getattr(qrngs, function_map[generator_string])
            nums = RNG(int(values['-NUMS-']))
            if _VARS['plt_fig'] == False:
                draw_chart(nums)
            else:
                update_chart(nums)
        if event == '-NUMBERS_BUTTON-':
            _VARS['numbers_window'] = make_numbers_window()
            _VARS['numbers_window']['-NUMBERS_BOX-'].print(nums[0:len(nums)//100])
            wrote = False
            disabled_button = False
            while True:
                event, values = _VARS['numbers_window'].read(timeout=500)
                if event == sg.WIN_CLOSED:
                    break
                if len(nums) > 1000 and disabled_button == False:
                    _VARS['numbers_window']['-CLIPBOARD_COPY_BUTTON-'].update(disabled=True)
                    _VARS['numbers_window'].Element('-CLIPBOARD_COPY_BUTTON-').SetTooltip("Disabled because of\ntoo many numbers!")
                    disabled_button = True
                if values['-SAVE_FILE_BUTTON-'] != '' and wrote == False:
                    with open(values['-SAVE_FILE_BUTTON-'], 'w') as f:
                        f.write(str(nums))
                    values['-SAVE_FILE_BUTTON-'] = ''
                    wrote = True
                if event == '-CLIPBOARD_COPY_BUTTON-':
                    subprocess.check_call('echo ' + str(nums).strip() + '|clip', shell=True)
                    
                    
    _VARS['window'].close()


