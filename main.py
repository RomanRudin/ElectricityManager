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


class Window(QWidget):
    def __init__(self):
        super().__init__()
        #левая треть
        configurations_list_label = QLabel('Выберите конфигурацию из уже существующих или добавьте новую:')
        self.configurations_list = QListWidget()

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
        appliance_time_flag.activated[str].connect(self.appliance_time_flag_function)

        appliance_efficiency = QLineEdit()
        appliance_efficiency.setPlaceholderText('КПД прибора')
        appliance_save = QPushButton('Сохранить')

        self.information_logs = QListWidget()


        #правая треть
        appliance_list_label = QLabel('Выберите электроприбор:')
        appliance_list = QListWidget()

        appliance_delete = QPushButton('Удалить')

        appliance_add_box = QComboBox()
        appliance_add_box.addItem('')
        for key in appliance:
            appliance_add_box.addItem(str(key))
        appliance_add_box.activated[str].connect(self.add_appliance)   



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
        layout_device.addWidget(appliance_type, stretch=2)
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
        layout_first.addWidget(self.configurations_list, stretch=32)
        layout_first.addLayout(layout_c_buttons, stretch=24)

        layout_second.addWidget(result_label, stretch=1)
        layout_second.addWidget(result_logs, stretch=1)
        layout_second.addLayout(layout_device, stretch=3)
        layout_second.addWidget(self.information_logs, stretch=1)

        layout_third.addWidget(appliance_list_label, stretch=1)
        layout_third.addWidget(appliance_list, stretch=15)

        layout_third.addLayout(layout_a_buttons, stretch=5)

        main_layout.addLayout(layout_first, stretch=4)
        main_layout.addLayout(layout_second, stretch=7)
        main_layout.addLayout(layout_third, stretch=5)

        #Обработка событий
        self.configurations_list.itemClicked.connect(self.show_third)
        configurations_create.clicked.connect(self.create_configuration)
        configurations_delete.clicked.connect(self.delete_configuration)
        appliance_list.itemClicked.connect(self.show_second_list)
        result_logs.itemClicked.connect(self.show_results)
        appliance_delete.clicked.connect(self.delete_appliance)
        appliance_save.clicked.connect(self.save_appliance)

        self.setLayout(main_layout)

    #Функции
    def writing(self):
        with open('data.json', 'a', encoding='utf-8') as file:
            json.dump(data, file, sort_keys=True, ensure_ascii=False)

    def message(self, message):
        self.information_logs.addItem(f"[{str(time.ctime(time.time()))}]:       {message}")

    def show_third(self):
        name = self.configurations_list.selectedItems()[0].text()
        self.appliance_list.clear()
        self.appliance_list.addItems(data[name])

    def show_second_list(self):
        self.show_second(name=self.appliance_list.selectedItems()[0].text())

    def show_results(self):
        self.layout_second.insertLayout(1, self.layout_result)
        self.layout_second.insertLayout(3, self.layout_result_selected)
        self.show_second(name=self.result_logs.selectedItems()[0].text())

    def hide_results(self):
        if results_shown:
            self.layout_second.removeItem(self.layout_result)
            self.layout_second.removeItem(self.layout_result_selected)
            self.show_second(name=self.result_logs.selectedItems()[0].text())

    def show_second(self, name):
        key = self.configurations_list.selectedItems()[0].text()
        self.appliance_type.clear()
        self.appliance_number.clear()
        self.appliance_power.clear()
        self.appliance_time.clear()
        self.appliance_efficiency.clear()
        self.appliance_time_flag.setCurrentText('Секунды')
        if appliance[name] != '':
            for i in appliance[name]:
                self.appliance_type.addItem(str(i))
            self.appliance_type.activated[str].connect(self.appliance_type_function) 
        if data[key][name]['data'][0] != 0:
            #data showing
            self.appliance_number.setText(str(data[key][name]['data'][0]))
            self.appliance_power.setText(str(data[key][name]['data'][1]))
            self.appliance_time.setText(str(data[key][name]['data'][2]))
            self.appliance_efficiency.setText(str(data[key][name]['data'][3]))
            self.appliance_model.setText(data[key][name]['data'][4])
            self.appliance_type.setCurrentText(str(data[key][name]['data'][5][0]))
            #result showing
            self.result_loss.setText('' + str(data[key][name]['result'][0]))
            self.result_money.setText('' + str(data[key][name]['result'][1]))
            self.result_all_loss.setText('Loss' + str(sum(data[key][key1]['result'][0] for key1 in data[key])))
            self.result_all_money.setText('Money' + str(sum(data[key][key1]['result'][1] for key1 in data[key])))

    def create_configuration(self): #Добавление заметки
        configuration_name, ok = QInputDialog.getText(main, lang.add_cofiguration, lang.name_of_cofiguration)
        if ok and configuration_name != '':
            self.hide_results()
            data[configuration_name] = {}
            self.configurations_list.addItem(configuration_name)
            self.writing()
        else:
            self.message(lang.name_unspecified)

    def delete_configuration(self):
        if self.configurations_list.selectedItems():
            self.hide_results()
            key = self.configurations_list.selectedItems()[0].text()
            data.pop(key)
            self.configurations_list.clear()
            self.appliance_list.clear()
            self.configurations_list.addItems(data)
            self.writing()
        else:
            self.message(lang.configuration_unselected_deleting)

    def save_appliance(self):
        if self.configurations_list.selectedItems() and self.appliance_list.selectedItems():
            if self.float_checking():
                if self.must_have_checker():
                    global d
                    key, key1 = self.configurations_list.selectedItems()[0].text(), self.appliance_list.selectedItems()[0].text()
                    number, power, time = self.must_have_checker()
                    if self.appliance_efficiency.text() != '':
                        n = float(self.appliance_efficiency.text())
                        data[key][key1]['data'] = [int(number), float(power), float(time), n, self.appliance_model.text(), data[key][key1]['data'][5]]
                        self.result(number, power, time * d, n)
                    else:
                        data[key][key1]['data'] = [int(number), float(power), float(time), '', self.appliance_model.text(), data[key][key1]['data'][5]]
                        self.result(number, power, time * d)
        else:
            self.message(lang.configuration_unselected_saving)

    def result(self, number, power, time, n=0, l=0):
        key, key1 = self.configurations_list.selectedItems()[0].text(), self.appliance_list.selectedItems()[0].text()
        if key[0] != 0:
            self.result_logs.addItem(key1)
            data[key][key1]['result'] = resulting(key1, power, time, number, n, l)

    def delete_appliance(self):
        if self.configurations_list.selectedItems() and self.appliance_list.selectedItems():
            self.hide_results()
            key, key1 = self.configurations_list.selectedItems()[0].text(), self.appliance_list.selectedItems()[0].text()
            data[key].pop([key1])
            self.appliance_list.clear()
            self.appliance_list.addItems(data[key])
            self.writing()
        else:
            self.message(lang.device_unselected)

    def add_appliance(self, text):
        try:
            if text not in data[self.configurations_list.selectedItems()[0].text()]:
                if text != '':
                    self.appliance_list.addItem(text)
                    data[self.configurations_list.selectedItems()[0].text()][str(text)] = {'data': [0, 0, 0, 0, '', ['', 0]], 'result': [0, 0]}
                    self.writing()
            else:
                self.message(lang.device_already_on_list)
        except IndexError:
            self.message(lang.configuration_unselected)

    def appliance_type_function(self, text):
        key, key1 = self.configurations_list.selectedItems()[0].text(), self.appliance_list.selectedItems()[0].text()
        data[key][key1]['data'][5] = [str(text), appliance[self.appliance_list.selectedItems()[0].text()][text]]

    def appliance_time_flag_function(self, text):
        global d
        if text == 'Часы':
            d = 3600
        elif text == 'Минуты':
            d = 60
        else:
            d = 1

    def float_checking(self):
        checker = {'время работы': self.appliance_time.text(), 'мощность': self.appliance_power.text(), 
            'количество': self.appliance_number.text(), 'КПД': self.appliance_efficiency.text()}
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
                        self.message(lang.parameter + str(key) + lang.must_be_an_integer)
                    else:
                        self.message((key) + 'должен содеражть число с плавающей точкой (',') или целое число')
                    flag = False
        return flag

    def must_have_checker(self):
        must_have = self.appliance_number.text(), self.appliance_power.text(), self.appliance_time.text()
        for data in must_have:
            if data == '':
                self.message(f'Параметр {data} обязателен для заполнения!')
                return False
        return int(self.appliance_number.text()), float(self.appliance_power.text()), float(self.appliance_time.text()) * d




if __name__ == '__main__':
    lang.choose_lang(0)
    start()
    #Виджеты
    app = QApplication([])

    main = Window()
    main.setWindowTitle('')
    main.resize(1900, 1000)


    main.message('Старт программы')

    try:
        import module as mod
    except ImportError:
        main.message('Файлы программы повреждены (module.py не найден). Обратитесь к разработчику.')


    #Запуск
    main.show()

    with open('D:\Учёба\Проект\data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    main.configurations_list.addItems(data)
    app.exec_()


    #setsize()
    #resize()