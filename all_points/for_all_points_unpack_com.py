import xml.etree.ElementTree as ET
import copy
import csv
import os

csv_keys = ["tag", "engSH", "engSL", 
            "HH", "HI", "LO", "LL", 
            "enHH", "enHI", "enLO", "enLL",
            "Module", "Channel", 
            "Controller", "BlockType"]     # ключи csv файла

def csv_dict_reader(file_obj):
    """
    Читаем CSV файл с помощью csv.DictReader
    """
    reader = csv.DictReader(file_obj, delimiter=';')
    reader_list = []
    for line in reader:
        if line[csv_keys[14]] == block_type and line[csv_keys[13]] == controller:
        #print(line[csv_keys[14]])
            reader_list.append(
                {csv_keys[0]: line[csv_keys[0]],
                csv_keys[1]: line[csv_keys[1]], 
                csv_keys[2]: line[csv_keys[2]],
                csv_keys[3]: line[csv_keys[3]],
                csv_keys[4]: line[csv_keys[4]],
                csv_keys[5]: line[csv_keys[5]],
                csv_keys[6]: line[csv_keys[6]],
                csv_keys[7]: line[csv_keys[7]],
                csv_keys[8]: line[csv_keys[8]],
                csv_keys[9]: line[csv_keys[9]],
                csv_keys[10]: line[csv_keys[10]],
                csv_keys[11]: line[csv_keys[11]],
                csv_keys[12]: line[csv_keys[12]]})                       
    return reader_list


"""
<<<----Здесь задаются исходные данные---->>>
Новый gvl_X файл формируется из старого safety_gvl + новых сгенерированных тегов
Для удобства перед прокачой очередного типа сигналов можно брать сгенерированный 
gvl_X файл, подкладывать в корневую папку и переименовывать в safety_gvl.
"""

point_type = 'DO'

csv_file = 'All_points_reserve.csv'                 # Файл с тегами каналов, шкалами и уставками
# tags_file = 'AI_txt.txt'                  # Текстовый файл с тегами каналов
primary_file_name = f'UNPACK_{point_type}_COMMAND_TEST.xml'  # Исходный xml файл с шаблоном
replaced_tag = f'TEST'             # Заменяемый тег из шаблона
primary_gvl_file_name = 'safety_gvl.xml'    # Исходный safety_gvl файл
if not os.path.exists(f'{point_type}'):     # Создаем папку, если не существует
    os.mkdir(f'{point_type}')
block_type = f'E-{point_type} (RED)'        # Тип блока
controller = 'DMA_PAZ2'                    # Контроллер
new_file_path = f'{point_type}/{controller}_{primary_file_name}'      # Новый xml файл для загрузки в конфигурацию
new_gvl_file_path = f'{point_type}/{controller}_UNPACK_{point_type}_COMMAND_gvl.xml'   # Новый файл safety_gvl для загрузки в конфигурацию
reserve = 'reserve'                         # Название переменной резерва

with open(csv_file) as f_obj:
    csv_list = csv_dict_reader(f_obj)
    number = len(csv_list)
    tags_list = [tag['tag'] for tag in csv_list]

    module_list = sorted(list(set([m['Module'] for m in csv_list])))
    number2 = len(module_list)


print('<<<----Общее количество тегов в файле---->>>')
print(number)
print('<<<----Список тегов---->>>')
print(tags_list)
print('<<<----csv_list---->>>')
for line in csv_list:
    print(line)
print('<<<----module_list---->>>')
print(module_list)

tree = ET.parse(primary_file_name)      # Парсинг xml-шаблона
root = tree.getroot()                       # Дерево xml-шаблона

print('<<<----Дерево:---->>>')
print(root[0][0][0].attrib)                 # Profile
print(root[0][0][1].attrib)                 # EntryList
print(root[0][0][1][0].attrib)              # 6198ad31-4b98-445c-927f-3258a0e82fe3
print(root[0][0][1][0][1].attrib)           # MetaObject
print(root[0][0][1][0][1][2].text)          # Имя группы
print(root[0][0][1][0][2].attrib)           # Object
print(root[0][0][1][0][2][0][0].attrib)     # SafetyVariables
#print(root[0][0][1][0][2][0][0][11][0].text)     # InitAlarm for AI only
print(root[0][0][1][0][2][1].attrib)        # NetworkArray
print(root[0][0][1][0][2][1][0].attrib)     # Блок с привязками 67368ee6...
print(root[0][0][1][0][2][1][0][0].text)    # Имя Network
print(root[0][0][1][0][2][1][0][2].attrib)          # MainItem
print(root[0][0][1][0][2][1][0][2][0].attrib)          # Input < MainItem
print(root[0][0][1][0][2][1][0][2][0][0].attrib)          # Inputs < Input
print(root[0][0][1][0][2][1][0][2][0][0][0][0].attrib)      # PinInfo < Inputs
print(root[0][0][1][0][2][1][0][2][0][0][0][1].attrib)      # PinFlags < Inputs
print(root[0][0][1][0][2][1][0][2][0][0][0][2].attrib)      # Item < Inputs
print(root[0][0][1][0][2][1][0][2][0][1].attrib)          # Outputs < Input
print(root[0][0][1][0][2][1][0][2][0][1][0][0].attrib)      # PinInfo < Outputs
print(root[0][0][1][0][2][1][0][2][0][1][0][1].attrib)      # PinFlags < Outputs
print(root[0][0][1][0][2][1][0][2][0][1][0][2].attrib)      # Item < Outputs
print(root[0][0][1][0][2][1][0][2][0][3].attrib)          # InstanceName < Input
print(root[0][0][1][0][2][1][0][2][1].attrib)          # Outputs < MainItem
print(root[0][0][1][0][2][1][0][2][0][9].attrib)          # Inputs < Input
print()

print(f'<<<-ID Input in MainItem: {root[0][0][1][0][2][1][0][2][0][9].text}')     # ID Input
print(f'<<<-ID Outputs: {root[0][0][1][0][2][1][0][2][1][0][2].text}')           # ID < Outputs
print(f'<<<-ID MainItem: {root[0][0][1][0][2][1][0][2][2].text}')            # ID < MainItem
print(f'<<<-ID Network: {root[0][0][1][0][2][1][0][4].text}')          # ID < Network
print(f'<<<-1st Input: {root[0][0][1][0][2][1][0][2][0][0][0][2][2].text}')     # 1st Input
print()

print('<<<----Кол-во SafetyVariables---->>>')
safety_len = len(root[0][0][1][0][2][0][0])     # Кол-во переменных SafetyVariables
print(safety_len)
print('<<<----Кол-во Inputs---->>>')
block_input_len = len(root[0][0][1][0][2][1][0][2][0][0])   # Кол-во Inputs
print(block_input_len)
print('<<<----Кол-во Outputs---->>>')
block_output_len = len(root[0][0][1][0][2][1][0][2][0][1])  # Кол-во Outputs
if block_output_len > 28:
    block_output_len = 28
print(block_output_len)

count = safety_len * number

counter = int(root[0][0][1][0][2][1][0][2][1][0][2].text)
print('<<<----Максимальное значение счетчика шаблона---->>>')
print(counter)
#print("<<<----Новое имя группы (чтобы не было конфликта при импорте)---->>>")
#root[0][0][1][0][1][2].text = f'{controller}_{point_type}'
print(root[0][0][1][0][1][2].text)

safety_var_list = [root[0][0][1][0][2][0][0][el][0].text for el in range(len(root[0][0][1][0][2][0][0]))]
print('<<<----safety_var_list---->>>')
print(safety_var_list)


for i in range(number2):
    new_block = copy.deepcopy(root[0][0][1][0][2][1][0])        # Создаем копию root[0][0][1][0][2][1][0]
    old_network_text = root[0][0][1][0][2][1][0][0].text        # Сохраняем старый текст в переменную
    old_block_text = root[0][0][1][0][2][1][0][2][0][3].text    # Сохраняем старое название блока в переменную
    splitted_module = module_list[i].split('_')
    print(splitted_module)
    chngd2 = f'{splitted_module[2]}_{splitted_module[3]}{splitted_module[4][:2]}'   # Берем из списка модулей следующий по порядку
    new_block[0].text = old_network_text.replace(replaced_tag, chngd2)     # Имя Network

    if tags_list[block_output_len * i] == '':
        chngd3 = reserve                              # Outputs < MainItem
    else:
        chngd3 = tags_list[block_output_len * i]        # Outputs < MainItem
    print(chngd3)

    old_counter = root[0][0][1][0][2][1][0][4].text             # Берем старший/наибольший ID из шаблона
    counter += 1                                        # Увеличиваем счетчик/номер ID для новой точки
    new_block[4].text = f'{counter}'                    # Преобразование обязательно, тип string не поддерживается
    counter += 1
    new_block[2][0][9].text = f'{counter}'

    for i2 in range(block_input_len):
        try:
            old_block_input = root[0][0][1][0][2][1][0][2][0][0][i2][2][0].text
            new_block[2][0][0][i2][2][0].text = old_block_input.replace(replaced_tag, chngd2)  # Inputs < Input
            #print(new_block[2][0][0][i2][2][0].text)
            counter += 1
            new_block[2][0][0][i2][2][2].text = f'{counter}'
        except:
            pass
            #print('Данный элемент не имеет вложенностей и будет пропущен') 
            #print(f'len(root[0][0][1][0][2][1][0][2][0][0][i2][2]) = {len(root[0][0][1][0][2][1][0][2][0][0][i2][2])}')

        #for safety_var in range(safety_len):
        old_text = root[0][0][1][0][2][0][0][1][0].text
        new_safety = copy.deepcopy(root[0][0][1][0][2][0][0][1])
        new_safety[0].text = old_text.replace(replaced_tag, chngd2)
        root[0][0][1][0][2][0][0].append(new_safety)    # добавляем новые переменные к SafetyVariables


    for i3 in range(1, block_output_len):
        if tags_list[i3 + block_output_len * i] == '':
            chngd = reserve                                               # Outputs < Input
        else:
            chngd = tags_list[i3 + block_output_len * i]                  # Берем из списка тегов следующий по порядку   Outputs < Input
        try:
            old_block_output = root[0][0][1][0][2][1][0][2][0][1][i3][2][0].text
            if chngd != reserve:
                new_block[2][0][1][i3][2][0].text = old_block_output.replace(replaced_tag, chngd) # Outputs < Input
            else:
                new_block[2][0][1][i3][2][0].text = chngd
            counter += 1
            new_block[2][0][1][i3][2][2].text = f'{counter}'
        except:
            pass
            #print(f'Данный элемент не имеет вложенностей и будет пропущен')
            #print(f'len(root[0][0][1][0][2][1][0][2][0][1][i3][2]) = {len(root[0][0][1][0][2][1][0][2][0][1][i3][2])}')
        old_text = root[0][0][1][0][2][0][0][2][0].text
        new_safety = copy.deepcopy(root[0][0][1][0][2][0][0][2])
        if chngd != reserve:
            new_safety[0].text = old_text.replace(replaced_tag, chngd)
        else:
            new_safety[0].text = chngd

        if new_safety[0].text not in safety_var_list:
            root[0][0][1][0][2][0][0].append(new_safety)    # добавляем новые переменные к SafetyVariables
        else:
            pass
        safety_var_list.append(new_safety[0].text)

    new_block[2][0][3].text = old_block_text.replace(replaced_tag, chngd2)   # InstanceName < Input

    old_outputs_text = root[0][0][1][0][2][1][0][2][1][0][0].text
    if chngd3 != reserve:
        new_block[2][1][0][0].text = old_outputs_text.replace(replaced_tag, chngd3)   # Outputs < MainItem

        new_safety = copy.deepcopy(root[0][0][1][0][2][0][0][2])
        new_safety[0].text = old_outputs_text.replace(replaced_tag, chngd3)
        root[0][0][1][0][2][0][0].append(new_safety)    # добавляем новые переменные к SafetyVariables
        safety_var_list.append(new_safety[0].text)
    else:
        new_block[2][1][0][0].text = chngd3   # Outputs < MainItem

    counter += 1
    new_block[2][2].text = f'{counter}'
    counter += 1
    new_block[2][1][0][2].text = f'{counter}'

    root[0][0][1][0][2][1].append(new_block)            # добавляем новые блоки к NetworkArray


try:
    tree_gvl = ET.parse(primary_gvl_file_name)      # Парсинг xml-шаблона
    root_gvl = tree_gvl.getroot()                   # Дерево xml-шаблона

    #print(root_gvl[0][0][1][0][2][0][0].attrib)     # SafetyVariables

    glv_names_list = [root_gvl[0][0][1][0][2][0][0][el][0].text for el in range(len(root_gvl[0][0][1][0][2][0][0]))]
    #print(glv_names_list)
    print('<<<----Поля, добавленные в новый файл gvl---->>>')

    for elem in range(len(root[0][0][1][0][2][0][0])):
        if root[0][0][1][0][2][0][0][elem][0].text in glv_names_list:
            pass
        else:
            if root[0][0][1][0][2][0][0][elem][2].text == 'VAR_EXTERNAL':
                new_safety_gvl = copy.deepcopy(root[0][0][1][0][2][0][0][elem])
                new_safety_gvl[2].text = 'VAR_GLOBAL'
                root_gvl[0][0][1][0][2][0][0].append(new_safety_gvl)
                print(root[0][0][1][0][2][0][0][elem][0].text)
except:
    pass


with open(new_file_path, 'wb') as file:            # Сохраняем получившееся дерево в новый файл
    tree.write(file)

try:
    with open(new_gvl_file_path, 'wb') as file:            # Сохраняем получившееся дерево в новый файл
        tree_gvl.write(file)
except:
    pass
