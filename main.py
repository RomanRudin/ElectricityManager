from pickle import ADDITEMS
from re import L
from tabnanny import check
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout, QRadioButton, QComboBox, QCheckBox
import time
import json
import os
from module import resulting, appliance, start
import localization as lang
#from module import method

d = 1
results_shown = False

data = {
    'test_configuration' : {
    }
}

#Функции
def writing():
    with open('data.json', 'a', encoding='utf-8') as file:
        json.dump(data, file, sort_keys=True, ensure_ascii=False)

def message(message):
    information_logs.addItem(f"[{str(time.ctime(time.time()))}]:       {message}")

def show_third():
    name = configurations_list.selectedItems()[0].text()
    appliance_list.clear()
    appliance_list.addItems(data[name])

def show_second_list():
    show_second(name=appliance_list.selectedItems()[0].text())

def show_results():
    layout_second.insertLayout(1, layout_result)
    layout_second.insertLayout(3, layout_result_selected)
    show_second(name=result_logs.selectedItems()[0].text())

def hide_results():
    if results_shown:
        layout_second.removeItem(layout_result)
        layout_second.removeItem(layout_result_selected)
        show_second(name=result_logs.selectedItems()[0].text())

def show_second(name):
    key = configurations_list.selectedItems()[0].text()
    appliance_type.clear()
    appliance_number.clear()
    appliance_power.clear()
    appliance_time.clear()
    appliance_efficiency.clear()
    appliance_time_flag.setCurrentText('Секунды')
    if appliance[name] != '':
        for i in appliance[name]:
            appliance_type.addItem(str(i))
        appliance_type.activated[str].connect(appliance_type_function) 
    if data[key][name]['data'][0] != 0:
        #data showing
        appliance_number.setText(str(data[key][name]['data'][0]))
        appliance_power.setText(str(data[key][name]['data'][1]))
        appliance_time.setText(str(data[key][name]['data'][2]))
        appliance_efficiency.setText(str(data[key][name]['data'][3]))
        appliance_model.setText(data[key][name]['data'][4])
        appliance_type.setCurrentText(str(data[key][name]['data'][5][0]))
        #result showing
        result_loss.setText('' + str(data[key][name]['result'][0]))
        result_money.setText('' + str(data[key][name]['result'][1]))
        result_all_loss.setText('Loss' + str(sum(data[key][key1]['result'][0] for key1 in data[key])))
        result_all_money.setText('Money' + str(sum(data[key][key1]['result'][1] for key1 in data[key])))

def create_configuration(): #Добавление заметки
    configuration_name, ok = QInputDialog.getText(main, lang.add_cofiguration, lang.name_of_cofiguration)
    if ok and configuration_name != '':
        hide_results()
        data[configuration_name] = {}
        configurations_list.addItem(configuration_name)
        writing()
    else:
        message(lang.name_unspecified)

def delete_configuration():
    if configurations_list.selectedItems():
        hide_results()
        key = configurations_list.selectedItems()[0].text()
        data.pop(key)
        configurations_list.clear()
        appliance_list.clear()
        configurations_list.addItems(data)
        writing()
    else:
        message(lang.configuration_unselected_deleting)

def save_appliance():
    if configurations_list.selectedItems() and appliance_list.selectedItems():
        if float_checking():
            if must_have_checker():
                global d
                key, key1 = configurations_list.selectedItems()[0].text(), appliance_list.selectedItems()[0].text()
                number, power, time = must_have_checker()
                if appliance_efficiency.text() != '':
                    n = float(appliance_efficiency.text())
                    data[key][key1]['data'] = [int(number), float(power), float(time), n, appliance_model.text(), data[key][key1]['data'][5]]
                    result(number, power, time * d, n)
                else:
                    data[key][key1]['data'] = [int(number), float(power), float(time), '', appliance_model.text(), data[key][key1]['data'][5]]
                    result(number, power, time * d)
    else:
        message(lang.configuration_unselected_saving)

def result(number, power, time, n=0, l=0):
    key, key1 = configurations_list.selectedItems()[0].text(), appliance_list.selectedItems()[0].text()
    if key[0] != 0:
        result_logs.addItem(key1)
        data[key][key1]['result'] = resulting(key1, power, time, number, n, l)

def delete_appliance():
    if configurations_list.selectedItems() and appliance_list.selectedItems():
        hide_results()
        key, key1 = configurations_list.selectedItems()[0].text(), appliance_list.selectedItems()[0].text()
        data[key].pop([key1])
        appliance_list.clear()
        appliance_list.addItems(data[key])
        writing()
    else:
        message(lang.device_unselected)

def add_appliance(text):
    try:
        if text not in data[configurations_list.selectedItems()[0].text()]:
            if text != '':
                appliance_list.addItem(text)
                data[configurations_list.selectedItems()[0].text()][str(text)] = {'data': [0, 0, 0, 0, '', ['', 0]], 'result': [0, 0]}
                writing()
        else:
            message(lang.device_already_on_list)
    except IndexError:
        message(lang.configuration_unselected)

def appliance_type_function(text):
    key, key1 = configurations_list.selectedItems()[0].text(), appliance_list.selectedItems()[0].text()
    data[key][key1]['data'][5] = [str(text), appliance[appliance_list.selectedItems()[0].text()][text]]

def appliance_time_flag_function(text):
    global d
    if text == 'Часы':
        d = 3600
    elif text == 'Минуты':
        d = 60
    else:
        d = 1

def float_checking():
    checker = {'время работы': appliance_time.text(), 'мощность': appliance_power.text(), 
        'количество': appliance_number.text(), 'КПД': appliance_efficiency.text()}
    flag = True
    for key in checker:
        data = checker[key]
        if data != '':
            try:
                if key == 'количество':
                    data = int(data)
                else:
                    data = float(data)
            except ValueError:
                if key == 'количество':
                    message(lang.parameter + str(key) + lang.must_be_an_integer)
                else:
                    message((key) + 'должен содеражть число с плавающей точкой (',') или целое число')
                flag = False
    return flag

def must_have_checker():
    must_have = appliance_number.text(), appliance_power.text(), appliance_time.text()
    for data in must_have:
        if data == '':
            message(f'Параметр {data} обязателен для заполнения!')
            return False
    return int(appliance_number.text()), float(appliance_power.text()), float(appliance_time.text()) * d




if __name__ == '__main__':
    lang.choose_lang(0)
    start()
    #Виджеты
    app = QApplication([])

    main = QWidget()
    main.setWindowTitle('')
    main.resize(1900, 1000)

    #левая треть
    configurations_list_label = QLabel('Выберите конфигурацию из уже существующих или добавьте новую:')
    configurations_list = QListWidget()

    configurations_create = QPushButton('Создать')
    configurations_delete = QPushButton('Удалить')


    #центральная треть
    result_label = QLabel("Результаты вычислений:")
    result_all_loss = QLabel("")
    result_all_money = QLabel("")
    result_logs = QListWidget()
    result_loss = QLabel("")
    result_money = QLabel("")
    appliance_information_label = QLabel('Введите данные. Обязательные для ввода поля помечены *')
    appliance_type_label = QLabel('Выберите тип электроприбора *')
    appliance_type = QComboBox()
    appliance_model = QLineEdit()
    appliance_model.setPlaceholderText('Модель / марка прибора')
    appliance_number = QLineEdit()
    appliance_number.setPlaceholderText('Количество приборов *')
    appliance_power = QLineEdit()
    appliance_power.setPlaceholderText('Мощность приборов *')
    appliance_time = QLineEdit()
    appliance_time.setPlaceholderText('Время работы в сутки *')
    appliance_time_label = QLabel('Выберите указанную единицу измерения *')
    appliance_time_flag = QComboBox()

    appliance_time_flag.addItem('Часы')
    appliance_time_flag.addItem('Минуты')
    appliance_time_flag.addItem('Секунды')
    appliance_time_flag.activated[str].connect(appliance_time_flag_function)

    appliance_efficiency = QLineEdit()
    appliance_efficiency.setPlaceholderText('КПД прибора')
    appliance_space = QLabel()
    appliance_save = QPushButton('Сохранить')

    information_logs = QListWidget()


    #правая треть
    appliance_list_label = QLabel('Выберите электроприбор:')
    appliance_list = QListWidget()

    appliance_delete = QPushButton('Удалить')

    appliance_add_box = QComboBox()
    appliance_add_box.addItem('')
    for key in appliance:
        appliance_add_box.addItem(str(key))
    appliance_add_box.activated[str].connect(add_appliance)   



    #Лэйауты
    main_layout = QHBoxLayout()
    layout_first = QVBoxLayout()
    layout_second = QVBoxLayout()
    layout_third = QVBoxLayout()
    layout_c_buttons = QVBoxLayout()
    layout_c_buttons1 = QHBoxLayout()
    layout_a_buttons = QVBoxLayout()
    layout_device = QVBoxLayout()
    layout_add_appliance = QHBoxLayout()
    layout_result = QVBoxLayout() #? dynamic layout
    layout_result_selected = QHBoxLayout() #? dynamic layout

    layout_result_selected.addWidget(result_money)
    layout_result_selected.addWidget(result_loss)

    layout_result.addWidget(result_all_money)
    layout_result.addWidget(result_all_loss)

    layout_add_appliance.addWidget(appliance_add_box)

    layout_c_buttons1.addWidget(configurations_create)
    layout_c_buttons1.addWidget(configurations_delete)

    layout_c_buttons.addLayout(layout_c_buttons1)

    layout_device.addWidget(appliance_information_label, stretch=1)
    layout_device.addWidget(appliance_type_label, stretch=1)
    layout_device.addWidget(appliance_type, stretch=1)
    layout_device.addWidget(appliance_model, stretch=1)
    layout_device.addWidget(appliance_number, stretch=1)
    layout_device.addWidget(appliance_power, stretch=1)
    layout_device.addWidget(appliance_time, stretch=1)
    layout_device.addWidget(appliance_time_label, stretch=1)
    layout_device.addWidget(appliance_time_flag, stretch=1)
    layout_device.addWidget(appliance_efficiency, stretch=1)
    layout_device.addWidget(appliance_save, stretch=1)

    layout_a_buttons.addWidget(appliance_delete)
    layout_a_buttons.addLayout(layout_add_appliance)

    layout_first.addWidget(configurations_list_label, stretch=1) #изменить
    layout_first.addWidget(configurations_list, stretch=32)
    layout_first.addLayout(layout_c_buttons, stretch=24)

    layout_second.addWidget(result_label, stretch=1)
    layout_second.addWidget(result_logs, stretch=1)
    layout_second.addLayout(layout_device, stretch=3)
    layout_second.addWidget(information_logs, stretch=1)

    layout_third.addWidget(appliance_list_label, stretch=1)
    layout_third.addWidget(appliance_list, stretch=15)

    layout_third.addLayout(layout_a_buttons, stretch=5)

    main_layout.addLayout(layout_first, stretch=4)
    main_layout.addLayout(layout_second, stretch=7)
    main_layout.addLayout(layout_third, stretch=5)


    main.setLayout(main_layout)

    #Обработка событий
    configurations_list.itemClicked.connect(show_third)
    configurations_create.clicked.connect(create_configuration)
    configurations_delete.clicked.connect(delete_configuration)
    appliance_list.itemClicked.connect(show_second_list)
    result_logs.itemClicked.connect(show_results)
    appliance_delete.clicked.connect(delete_appliance)
    appliance_save.clicked.connect(save_appliance)

    message('Старт программы')

    try:
        import module as mod
    except ImportError:
        message('Файлы программы повреждены (module.py не найден). Обратитесь к разработчику.')


    #Запуск
    main.show()

    with open('D:\Учёба\Проект\data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    configurations_list.addItems(data)
    app.exec_()


    #setsize()
    #resize()