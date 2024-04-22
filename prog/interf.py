import PySimpleGUI as sg
from pars import *

file_states='C:/Users/ПК-870/Desktop/ДИПЛОМ/prog/states_predicates.txt'
file_trans='C:/Users/ПК-870/Desktop/ДИПЛОМ/prog/trans.txt'
file_loop='C:/Users/ПК-870/Desktop/ДИПЛОМ/prog/loop.txt'



state_pred=read_file(file_states)#считали состояния и их предикаты
trans=read_file(file_trans)#считали переходы
pred_only=get_pred_only(state_pred)#предикаты
pred_true=get_pred_true(state_pred)


layout = [  [sg.Text('Выберете модель для генерации')],
          [sg.Button('Модель с имитацией реального времени')],
            [sg.Button('Временная модель')],
             [sg.Button('Выход')] 
            ]

# Create the Window
window = sg.Window('Генерация smv-файла', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Выход': # if user closes window or clicks cancel
        break
    elif event=='Модель с имитацией реального времени':
        result='No'
        while result=='No':
            folder = sg.popup_get_folder('Выберете папку для генерации файла с кодом')
            result=sg.popup_yes_no(f'Вы действительно хотите создать файл в папке \n {folder} ?')
            if result=='Yes':
                file_name=folder+'/'+'code.smv'
                make_code_rasp(file_name, state_pred, trans, pred_only, pred_true)
                sg.popup_auto_close('Код успешно сгенерирован!', auto_close_duration=2)
    elif event=='Временная модель':
        result='No'

        while result=='No':
            folder = sg.popup_get_folder('Выберете папку для генерации файла с кодом')
            result=sg.popup_yes_no(f'Вы действительно хотите создать файл в папке \n {folder} ?')
            sg.popup_auto_close('Необходимо ввести параметры расписания в командной строке проекта!', auto_close_duration=10)
            if result=='Yes':
                D_ts=int(input('Введите значение длительности временного интервала\n'))
                K=int(input('Введите размер окна ожидания метки времени / 2\n'))
                N_ts=int(input('Введите количество временных интервалов в эпохе\n'))
                
                
                pred_true_without_loop=change_data_for_timed_kripke(D_ts, K, N_ts)
                file_name=folder+'/'+'timed_kripke.smv'
                make_code_rasp(file_name, state_pred, trans, pred_only, pred_true_without_loop)
                sg.popup_auto_close('Код успешно сгенерирован!', auto_close_duration=2)
                


            




