import PySimpleGUI as sg
import asyncio
import gcreater
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

def init_grf(file_name):
    figure = gcreater.load(file_name)
    return figure

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='none', expand=0)
    return figure_canvas_agg

layout = [[sg.Button(button_text= 'Построить граф', key="-GRAPHKEY-", visible = True), 
           sg.Button(button_text= '1 граф', key="-GRAPH1-", visible = True)],
          [sg.Canvas(size=(650,500),key='-CANVAS-', background_color='white')]] 
    # создание окна
window = sg.Window('Лидер', layout,font="Helvitica 10")

async def main():
    # цикл
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        # рисование графа сообщества
        if event == '-GRAPHKEY-':
            # fig= create_graph.load(file_name)
            # figure_agg = await draw_figure(window['-CANVAS-'].TKCanvas, '152573807adj.txt')
            pool = ThreadPoolExecutor(max_workers=multiprocessing.cpu_count())
            #loop = asyncio.get_event_loop()
            fig = await loop.run_in_executor(pool, init_grf, '24243817adj1.txt')
            figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, fig)

        if event == '-GRAPH1-':
            print(1)    

loop = asyncio.get_event_loop()
loop.run_until_complete(main())