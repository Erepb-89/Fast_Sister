import xml.etree.ElementTree as ET
from tkinter import *
import tkinter as tk
from tkinter.ttk import Combobox
import os
import copy
import csv
from tkinter import filedialog


csv_keys = ["tag", "SH", "SL", 
            "HH", "HI", "LO", "LL", 
            "enHH", "enHI", "enLO", "enLL",
            "Module", "Channel", 
            "Controller", "BlockType"]     # ключи csv файла


class ProsoftApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Прокачка сигналов Prosoft (ПАЗ)")
        self.geometry('355x200')

        self.lbl2 = Label(self, text='Заменяемая переменная', font=("Arial Bold", 10))
        self.combo_point = Combobox(self)
        self.combo_point['values'] = ['AI', 'DI', 'DO']
        self.combo_point.current(0)  # установите вариант по умолчанию 

        self.btn_open = Button(self, text="Открыть файл", command=self.open_file)

        self.lbl2.pack()
        self.combo_point.pack()
        self.btn_open.pack()


    def open_file(self):
        self.file = filedialog.askopenfilename(filetypes = (("CSV files","*.csv"),("all files","*.*")))

        with open('All_points.csv') as f_obj:
            self.ctrlr_list = self.csv_controller_list(f_obj)

        self.lbl = Label(self, text='Выбранный контроллер', font=("Arial Bold", 10))
        self.lbl.pack()

        self.combo_ctrlr = Combobox(self)
        self.combo_ctrlr['values'] = self.controller_list
        self.combo_ctrlr.current(0)  # установите вариант по умолчанию 
        self.combo_ctrlr.pack()

        self.btn_run = tk.Button(self, text="Старт", command=self.on_button)
        self.btn_run.pack()

        return self.file

    def csv_controller_list(self, file_obj):
        rdr = csv.DictReader(file_obj, delimiter=';')
        self.controller_list = (line[csv_keys[13]] for line in rdr if 'PAZ' in line[csv_keys[13]])
        self.controller_list = sorted(list(set(self.controller_list)))
        return self.controller_list


    def csv_dict_reader(self, file_obj):
        """
        Читаем CSV файл с помощью csv.DictReader
        """
        reader = csv.DictReader(file_obj, delimiter=';')

        self.reader_list = []
        for line in reader:
            if line[csv_keys[14]] == self.block_type and line[csv_keys[13]] == self.controller:

                self.reader_list.append(
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
                    csv_keys[13]: line[csv_keys[13]]})                       
        return self.reader_list


    def on_button(self):
        print(self.combo_ctrlr.get())

        point_type = self.combo_point.get()
        print(point_type)

        csv_file = self.file                        # Файл с тегами каналов, шкалами и уставками
        print(csv_file)
        primary_file_name = f'{point_type}_01.xml'  # Исходный xml файл с шаблоном
        replaced_tag = f'{point_type}1'             # Заменяемый тег из шаблона
        primary_gvl_file_name = 'safety_gvl.xml'    # Исходный safety_gvl файл

        try:
            if not os.path.exists(f'{point_type}'):     # Создаем папку, если не существует
                os.mkdir(f'{point_type}')
        except Exception as ex:
            print('Введите заменяемую переменную')
            print(ex)

        self.block_type = f'E-{point_type} (RED)'        # Тип блока
        self.controller = self.combo_ctrlr.get()               # Контроллер
        new_file_path = f'{point_type}/{self.controller}_{point_type}.xml'      # Новый xml файл для загрузки в конфигурацию
        new_gvl_file_path = f'{point_type}/{self.controller}_gvl.xml'   # Новый файл safety_gvl для загрузки в конфигурацию
        synchron = 'PAZ004SHU01_S_alarm'


        with open(csv_file) as f_obj:
            csv_list = self.csv_dict_reader(f_obj)
            number = len(csv_list)
            tags_list = [tag['tag'] for tag in csv_list]


        tree = ET.parse(primary_file_name)      # Парсинг xml-шаблона
        root = tree.getroot()                       # Дерево xml-шаблона

        safety_len = len(root[0][0][1][0][2][0][0])     # Кол-во переменных SafetyVariables
        print(safety_len)
        print('<<<----Кол-во Inputs---->>>')
        block_input_len = len(root[0][0][1][0][2][1][0][2][0][0])   # Кол-во Inputs
        print(block_input_len)
        print('<<<----Кол-во Outputs---->>>')
        block_output_len = len(root[0][0][1][0][2][1][0][2][0][1])  # Кол-во Outputs
        print(block_output_len)

        count = safety_len * number

        counter = int(root[0][0][1][0][2][1][0][2][1][0][2].text)
        print("<<<----Новое имя группы (чтобы не было конфликта при импорте)---->>>")
        root[0][0][1][0][1][2].text = f'{self.controller}_{point_type}'
        print(root[0][0][1][0][1][2].text)


        safety_var_list = [root[0][0][1][0][2][0][0][el][0].text for el in range(len(root[0][0][1][0][2][0][0]))]
        print('safety_var_list', safety_var_list)

        for i in range(number):

            new_block = copy.deepcopy(root[0][0][1][0][2][1][0])        # Создаем копию root[0][0][1][0][2][1][0]
            old_network_text = root[0][0][1][0][2][1][0][0].text        # Сохраняем старый текст в переменную
            chngd = tags_list[i]                                        # Берем из списка тегов следующий по порядку
            new_block[0].text = old_network_text.replace(replaced_tag, chngd)     # Имя Network

            old_counter = root[0][0][1][0][2][1][0][4].text             # Берем старший/наибольший ID из шаблона
            counter += 1                                        # Увеличиваем счетчик/номер ID для новой точки
            new_block[4].text = f'{counter}'                    # Преобразование обязательно, тип string не поддерживается
            counter += 1
            new_block[2][0][9].text = f'{counter}'

            for i2 in range(block_input_len):
                try:
                    old_block_input = root[0][0][1][0][2][1][0][2][0][0][i2][2][0].text

                    if old_block_input == 'TEST_SHU':
                        new_block[2][0][0][i2][2][0].text = synchron

                    else:
                        new_block[2][0][0][i2][2][0].text = old_block_input.replace(replaced_tag, chngd)  # Inputs < Input

                    counter += 1
                    new_block[2][0][0][i2][2][2].text = f'{counter}'

                except:
                    pass

            for i3 in range(block_output_len):
                try:
                    old_block_output = root[0][0][1][0][2][1][0][2][0][1][i3][2][0].text
                    new_block[2][0][1][i3][2][0].text = old_block_output.replace(replaced_tag, chngd) # Outputs < Input
                    counter += 1
                    new_block[2][0][1][i3][2][2].text = f'{counter}'

                except:
                    pass

            new_block[2][0][3].text = old_network_text.replace(replaced_tag, chngd)   # InstanceName < Input

            old_outputs_text = root[0][0][1][0][2][1][0][2][1][0][0].text
            new_block[2][1][0][0].text = old_outputs_text.replace(replaced_tag, chngd)   # Outputs < MainItem

            counter += 1
            new_block[2][2].text = f'{counter}'
            counter += 1
            new_block[2][1][0][2].text = f'{counter}'

            root[0][0][1][0][2][1].append(new_block)            # добавляем новые блоки к NetworkArray


            for safety_var in range(safety_len):            
                old_text = root[0][0][1][0][2][0][0][safety_var][0].text

                if old_text == 'InitAlarm':
                    pass

                else:
                    new_safety = copy.deepcopy(root[0][0][1][0][2][0][0][safety_var])
                    new_safety[0].text = old_text.replace(replaced_tag, chngd)
                    safety_key = new_safety[0].text.split('_')

                    if safety_key[-1] in csv_keys:
                        new_safety[3].text = csv_list[i][safety_key[-1]]

                    if new_safety[0].text in safety_var_list:
                        pass            # Пропускаем повторяющиеся переменные

                    else:    
                        root[0][0][1][0][2][0][0].append(new_safety)    # добавляем новые переменные к SafetyVariables

        try:
            tree_gvl = ET.parse(primary_gvl_file_name)      # Парсинг xml-шаблона
            root_gvl = tree_gvl.getroot()                   # Дерево xml-шаблона

            glv_names_list = [root_gvl[0][0][1][0][2][0][0][el][0].text for el in range(len(root_gvl[0][0][1][0][2][0][0]))]
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
            self.lb2 = Label(self, text=f'Файл {new_file_path} создан', font=("Arial Bold", 10))
            self.lb2.pack()

        try:
            with open(new_gvl_file_path, 'wb') as file:            # Сохраняем получившееся дерево в новый файл
                tree_gvl.write(file)
                self.lb3 = Label(self, text=f'Файл {new_gvl_file_path} создан', font=("Arial Bold", 10))
                self.lb3.pack()

        except:
            pass


app = ProsoftApp()
app.mainloop()
