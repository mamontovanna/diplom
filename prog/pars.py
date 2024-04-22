import random
def get_pred_only(dict_state_pred): #получаем только предикаты для их норм инициализации. при чем тут множества, поэтому только уникальные
    res=set()
    for key, value in dict_state_pred.items():
        for v in value:
            res.add(v)
    return res

def get_pred_true(dict_state_pred):#решаем проблему повторения предикатов: проверяем, если ли в только что созданном словаре ключ-предикат. 
    #если нет, то создаем его и его значение - это состояние, в котором он истенен. таким обрахом, если мы снова встречаем такой предикат, потом просто в список значений добавляем состояние
    pred_true=dict()
    for key, value in dict_state_pred.items():
        for pred in value:
            if pred in pred_true:
                pred_true[pred].append(key)
            else:
                pred_true[pred]=[key]
    return pred_true

def read_file(file_name):#   {состояние :[предикат1, предикат2], ...}
    dat=dict()
    with open(file_name, 'r') as file:
        data=file.readlines()#получили список data, где каждый элемент - строка файла
        #print(*data)

        for line in data:
            parts=line.split()
            key=parts[0]
            values=parts[1].split(',')
            dat[key]=values
        return dat

def get_loop_state(file_loop):#считываем из файла состояния с петлями
    with open(file_loop, 'r') as file:
        loop_state=file.read().split('\n')#список состояний с петлей
    return loop_state

def change_data_for_timed_kripke(D_ts, K, N_ts):
    loop_state=get_loop_state(file_loop)#считываем из файла состояния с петлей
    new_trans=dict()
    for el in loop_state:
        pred=state_pred[el]
        instead_of_loop=list()
        trans_el=list()#обяз сост
        #определяем сколько раз будут повторяться (условно) одни и те же состояния
        if 'II_1' in pred or 'II_2' in pred:
            cnt=D_ts*K
        elif 'III' in pred:
            cnt=(N_ts-2*K)*D_ts
        elif 'stop' in pred:
            random.seed()
            cnt=random.randint(D_ts,N_ts*D_ts+1)
        #добавляем в словарь новые состояния
        for i in range(cnt-1):#т.к. одно состояние из этого общего количества уже есть 
            state_pred[el+'_'+str(i)]=pred
            instead_of_loop.append(el+'_'+str(i))#тут все доп состояния вместо перехода
         

    #редактируем словарь с переходами
        trans_el=trans[el].copy()#базовые переходы
        trans[el].remove(el)
        trans_el.remove(el)
        for i in range(len(instead_of_loop)-1):
            trans[instead_of_loop[i]]=trans_el.copy()#обязательные переходы
            trans[instead_of_loop[i]].append(instead_of_loop[i+1])#переход в след состояние, которое вместо петли
            #print(instead_of_loop[i], trans[instead_of_loop[i]])
            if i==0:
                trans[el].append(instead_of_loop[i])
        trans[instead_of_loop[-1]]=trans_el.copy()  
        #print(trans[el])
        trans_el.clear()
    pred_true_without_loop=get_pred_true(state_pred)#словарь, где ключ - предикат(уникальный),
#а значение - состояние, в котором этот предикат истенен
    #print(pred_true_without_loop)
    return pred_true_without_loop
    

def make_code_rasp(file_name, dict_states, dict_trans, set_only_pred, dict_pred_true):
   check=True
   with open(file_name, 'w') as file:
    file.write('MODULE main\nVAR\n\tstate_ : {')
    #состояния
    k=1
    for key in dict_states:
        if k==len(dict_states):
           file.write(f'{key}')
        else:
           file.write(f'{key},')
        k+=1
    file.write('};\n')#
    #предикаты
    for pred in set_only_pred:#не знаю зачем я это сделала, если есть pred_true, где и так уникальные предикаты
        file.write(f'\t{pred} : boolean;\n')
    #переходы
    file.write('ASSIGN\n\tinit(state_) :=S0;\n\tnext(state_) :=case\n\t\t\t\t\t\t')
    
    for key, value in dict_trans.items():
        if len(value)>1:
            file.write(f'(state_ = {key}) : '+'{')
            for pred in value:
                file.write(pred)
                if value.index(pred)<len(value)-1:
                    file.write(', ')
                else:
                    file.write('};\n\t\t\t\t\t\t')
        else:
            file.write(f'(state_ = {key}) : ')
            for pred in value:
                file.write(f'{pred};\n\t\t\t\t\t\t')
    file.write('TRUE: state_;\n\t\t\t\t\t')
    file.write('esac;\n')
    file.write('------------------------------------------------------')

    #значение предикатов
    for key, value in dict_pred_true.items():
            file.write(f'\n\t{key}:= case (')
            for state in value:
                file.write(f'(state_ = {state})')
                if value.index(state)<len(value)-1:
                    file.write(' | ')
            file.write(') : TRUE;\n\t\t\t\t\tTRUE: FALSE;\n\t\t\tesac;')
    print('DONE')

##################################################




#print(pred_true)




##################################################MAIN##############################################
file_states='C:/Users/ПК-870/Desktop/ДИПЛОМ/prog/states_predicates.txt'
file_trans='C:/Users/ПК-870/Desktop/ДИПЛОМ/prog/trans.txt'
file_loop='C:/Users/ПК-870/Desktop/ДИПЛОМ/prog/loop.txt'


#smv-файлы
file_code='C:/Users/ПК-870/Desktop/ДИПЛОМ/nuxmv/nuXmv-2.0.0-win64/bin/code.smv'
file_timed_kripke='C:/Users/ПК-870/Desktop/ДИПЛОМ/nuxmv/nuXmv-2.0.0-win64/bin/timed_kripke.smv'

state_pred=read_file(file_states)#считали состояния и их предикаты
trans=read_file(file_trans)#считали переходы

pred_only=get_pred_only(state_pred)#предикаты

pred_true=get_pred_true(state_pred)#словарь, где ключ - предикат(уникальный),
#а значение - состояние, в котором этот предикат истенен
ch=1
#while ch!=0:
#    print('Выберете опцию автоматической генерация smv-файла с описанием модели Крипке:\n1 - с имитацией реального времени(с петлями)\n2 - временная модель\n0 - выход')
#    ch=int(input())
#    
#    if ch==1:
#        #print(trans)
#        make_code_rasp(file_code, state_pred, trans, pred_only, pred_true)
#        #print(pred_true)
#    if ch==2:
#        D_ts=int(input('Введите значение длительности временного интервала\n'))
#        K=int(input('Введите размер окна ожидания метки времени / 2\n'))
#        N_ts=int(input('Введите количество временных интервалов в эпохе\n'))
#        pred_true_without_loop=change_data_for_timed_kripke(D_ts, K, N_ts)
#        make_code_rasp(file_timed_kripke, state_pred, trans, pred_only, pred_true_without_loop)
        
        
         



            
                
            
                
        



            
            
        
                






    














   



