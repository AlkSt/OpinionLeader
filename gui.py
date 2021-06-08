import PySimpleGUI as sg
import tvk_parse
import os.path
import network_analitic
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import create_graph
import matplotlib.pyplot as plt
import webbrowser
import model3
import multiprocessing
import concurrent.futures

import time

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='none', expand=0)
    return figure_canvas_agg

def delete_figure_agg(figure_agg):
    figure_agg.get_tk_widget().forget()
    plt.close('all') 

def analitic(Gr, res):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        futures.append(executor.submit(network_analitic.degree_centralitys, G=Gr))                
        futures.append(executor.submit(network_analitic.page_rank, G=Gr))                
        futures.append(executor.submit(network_analitic.leader_rank, G=Gr))
        futures.append(executor.submit(network_analitic.cluster_runk, G=Gr))
        futures.append(executor.submit(network_analitic.stars_rank, G=Gr))
        for future in concurrent.futures.as_completed(futures):
            res.append(future.result())

sg.theme('Reddit')   # тема окна 

# содержимое 
left_frame= [[sg.Text('Получение структуры сообщества', font="TimesNewRoman")],
            [sg.Text('Идентификатор сообщества'),
             sg.InputText( key = "-INPUTID-", default_text="87359621", do_not_clear=True, focus = True),
             sg.Button('Ok')],
            [sg.Button(button_text= 'Построить граф', key="-GRAPHKEY-", disabled=True),
             sg.Button(button_text= 'Показать сообщество', key="-GROUPBUT-", disabled=True)],
            [sg.Canvas(size=(640,480),key='-CANVAS-', background_color='white')]]

right_frame = [[sg.Text('Выберите метод для анализа', font="TimesNewRoman 14" ) ],
                [sg.Combo(['Degree centrality', 'Leader rank', 'Cluster rank','RC measure'],
                            size=(50, 50), key = "-COMBOBAR-", enable_events= "some", disabled=True,
                            readonly = True)],
                [sg.Text('Топ лидеров мнений')],
                [sg.Listbox(values=[''],  key = '-RANKTEXT-',size=(50, None), background_color='white', highlight_background_color='dodgerblue', enable_events= True)],
                [sg.Text('Смоделировать распространение', font="TimesNewRoman 14", pad = (5, 25))],
                [sg.Text('Количество шагов', font="TimesNewRoman 14"), sg.Slider(range=(150,5000), orientation='h', size=(25,20), change_submits=True, key='-SLIDER-')],
                [sg.Checkbox('Degree centrality', key = '-DC-', checkbox_color='violet', default=True)],
                # [sg.Checkbox('Page Rank', key = '-PR-', default=True)],
                [sg.Checkbox('Leader rank', key = '-LR-', checkbox_color='green')],
                [sg.Checkbox('Cluster rank', key = '-CR-', checkbox_color= 'orange')],
                [sg.Checkbox('RC measure', key = '-SR-', checkbox_color='darkred')],
                [sg.Button(button_text= 'Моделировать распространение', key="-EXPERIMENT-", disabled=True), sg.Checkbox('Учитывать совпадения', key = '-DIF-')]
                ]           

columns = [[sg.Column(left_frame),
            sg.Column( right_frame, size =(400,550))] ]

layout = [[sg.Column(columns)], [sg.ProgressBar(100, orientation='h', size=(80, 20), key='-PROGRESS-')]] 

def main():
    DC=dict()
    PR = dict()
    LR = dict()
    CR = dict()
    SR = dict()
    # создание окна
    window = sg.Window('Лидер', layout,font="Helvitica 10", location=(10,10))
    figure_agg = None

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
            break
        
        #получение списка смежности для сообщества   
        if event == 'Ok':
            
            window['-GRAPHKEY-'].update(disabled = True)
            window['-GROUPBUT-'].update(disabled = True)
            window['-COMBOBAR-'].update(disabled = True)
            window['-EXPERIMENT-'].update(disabled = True)
            if(figure_agg != None): delete_figure_agg(figure_agg)
            window['-RANKTEXT-'].update([])
            window['-COMBOBAR-'].update('')

            input_id = values["-INPUTID-"]
            print('You entered ', input_id)
            file_name = input_id+'adj.txt'
            if(not os.path.exists(file_name)):
                group_cap = tvk_parse.get_count(input_id)
                status = multiprocessing.Value('i')
                process = multiprocessing.Process(target=tvk_parse.get_info_about_group, args=(status,input_id))
                process.start()

                while process.is_alive():
                    window['-PROGRESS-'].UpdateBar(100*status.value/(2*group_cap))
                    print(status.value)                
            else: print(1)
                    
            window['-PROGRESS-'].UpdateBar(50)

            G = create_graph.get_graph(file_name)
            results = [{},{},{},{}]
            funcs = [network_analitic.degree_centralitys,network_analitic.cluster_runk, network_analitic.stars_rank, network_analitic.leader_rank]
            procs =[]
                # создаем объект блокировки
            lock = multiprocessing.Lock()
            # создаем очередь
            queue = multiprocessing.Queue()
            for i in range(len(funcs)):
                proc = multiprocessing.Process(target=funcs[i], args=(lock, queue, G))
                procs.append(proc)
                proc.start()

                while proc.is_alive():
                    window['-PROGRESS-'].UpdateBar(i*12.5+50)
                while not queue.empty():
                    results[i] = (queue.get())
            # ждем результатов
            for proc in procs: proc.join()             
            # освобождаем ресурсы
            for proc in procs: proc.close() 
            DC, CR, SR, LR = results

            
            # arr = multiprocessing.Array('i', 100000)
            # funcs = [network_analitic.degree_centralitys, network_analitic.leader_rank,network_analitic.cluster_runk, network_analitic.stars_rank]
            # procs = [{},{},{},{}]
            # for i in range(len(funcs)):
            #     pool = multiprocessing.Pool(processes=3)
            #     result = pool.apply_async(funcs[i], (G,))
                
            #     procs[i] = (result.get())
            #     print()
                # proc = multiprocessing.Process(target=func, args=(G, arr))
                # procs.append(proc)
                # proc.start()
            
            # window['-PROGRESS-'].UpdateBar(50)
            # # Ждем результатов
            # [proc.join() for proc in procs]            
            # print('Вывод результатов:')
            # print([i for i in arr if i != 0])
            # # очищаем используемые ресурсы
            # [proc.close() for proc in procs]

            # start_time = time.time()       
            # DC = network_analitic.degree_centralitys(G)
            # print(time.time() - start_time)

            # start_time = time.time()  
            # CR = network_analitic.cluster_runk(G)
            # print(time.time() - start_time)

            # start_time = time.time()  
            # SR = network_analitic.stars_rank(G)
            # print(time.time() - start_time)

            # start_time = time.time()  
            # LR = network_analitic.leader_rank (G)
            # print(time.time() - start_time)

            # обновление полей
            window['-PROGRESS-'].UpdateBar(100)
            window['-GRAPHKEY-'].update(disabled = False)
            window['-GROUPBUT-'].update(disabled = False)
            window['-COMBOBAR-'].update(disabled = False)
            window['-EXPERIMENT-'].update(disabled = False)

        # рисование графа сообщества
        if event == '-GRAPHKEY-':
            # fig= create_graph.load(file_name)
            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     futures = []
            #     futures.append(executor.submit(create_graph.load, file_name=file_name))
            #     for future in concurrent.futures.as_completed(futures):
            #        figure = future.result()
            #        window['-PROGRESS-'].UpdateBar(100)
            #        figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, figure)
                   
            if(figure_agg != None): delete_figure_agg(figure_agg)   
            figure = create_graph.load(file_name)
            figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, figure)
        # рассчет рановых значений выбранным методом
        if event == "-COMBOBAR-":
            method = values["-COMBOBAR-"]
            G = create_graph.get_graph(file_name)
            ranking_dict = list()
            leader_rows = list()
            if (method == "Degree centrality"):
                ranking_dict = DC #list(network_analitic.degree_centralitys(G).items())
            elif (method == "Leader rank"):
                ranking_dict = LR #list(network_analitic.leader_rank(G).items())
            elif (method == "Cluster rank"):
                ranking_dict = CR#list(network_analitic.cluster_runk(G).items()) 
            elif (method == "RC measure"):
                ranking_dict = SR   
            # отображение первых десяти из списка 
            out_line = 10 if 10< len(ranking_dict) else len(ranking_dict)
            for item in list(ranking_dict.items()):#[:out_line]:
                leader_rows.append('Rank: ' + str(round(float(item[1]),4))+ '    ID: ' + str(item[0]))   
            window['-RANKTEXT-'].update(  leader_rows )

        if event == "-GROUPBUT-":
            webbrowser.open('https://vk.com/club'+input_id)

        if event == '-RANKTEXT-':
            id_text = values['-RANKTEXT-'][0].split('D: ')[1]
            webbrowser.open('https://vk.com/id'+ id_text)
        if event == '-SLIDER-':
            sz_slider_step = int(values['-SLIDER-'])
        if event == '-EXPERIMENT-':
            sz_slider_step = int(values['-SLIDER-'])

            sDC = DC if values['-DC-'] else {}
            sLR = LR if values['-LR-'] else {}
            sCR = CR if values['-CR-'] else {}
            sSR = SR if values['-SR-'] else {}
            if(figure_agg != None): delete_figure_agg(figure_agg)
            if values['-DIF-']:
                figure = model3.dif_modeling_experiment(sDC,sLR,sCR,sSR,sz_slider_step,file_name)
            else: figure = model3.get_modeling_experiment(sDC,sLR,sCR,sSR,sz_slider_step,file_name)
            figure_agg = draw_figure(window['-CANVAS-'].TKCanvas, figure)


    window.close()

if __name__ == "__main__":
    main()

