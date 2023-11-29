#Импортирование Библиотек
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QComboBox, QSizePolicy
from sys import argv, exit
import time
from json import load, dump
import localization as lang

results_shown = False
data = {}

class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        configurations_list_label = QLabel('Выберите конфигурацию из уже существующих или добавьте новую:')
        configurations_list_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.configurations_list = QListWidget()
        self.configurations_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        configurations_create = QPushButton('Создать')
        configurations_delete = QPushButton('Удалить')
        configurations_create.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        configurations_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        configurations_create.setObjectName('configurations_buttons')
        configurations_delete.setObjectName('configurations_buttons')

        result_label = QLabel("Результаты вычислений:")
        result_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_all_loss = QLabel("")
        self.result_all_money = QLabel("")
        self.result_all_loss.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_all_money.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_all_loss.setObjectName('result_info')
        self.result_all_money.setObjectName('result_info')
        self.result_logs = QListWidget()
        self.result_logs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_logs.setObjectName('result_logs')
        self.result_loss = QLabel("")
        self.result_money = QLabel("")
        self.result_loss.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_money.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_loss.setObjectName('result_info')
        self.result_money.setObjectName('result_info')

        appliance_information_label = QLabel('Введите данные. Обязательные для ввода поля помечены *')
        appliance_information_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        appliance_information_label.setObjectName('appliance_information_label')
        appliance_type_label = QLabel('Выберите тип электроприбора *')
        appliance_type_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_type = QComboBox()
        self.appliance_type.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_type.setEnabled(False)
        self.appliance_model = QLineEdit()
        self.appliance_number  = QLineEdit()
        self.appliance_power = QLineEdit()
        self.appliance_time = QLineEdit()
        self.appliance_efficiency = QLineEdit()
        self.appliance_model.setPlaceholderText('Модель / марка прибора')
        self.appliance_number.setPlaceholderText('Количество приборов *')
        self.appliance_power.setPlaceholderText('Мощность приборов *')
        self.appliance_time.setPlaceholderText('Время работы в сутки *')
        self.appliance_efficiency.setPlaceholderText('КПД прибора в %')
        self.appliance_model.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_number.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_power.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_time.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_efficiency.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_model.setObjectName('appliance_args')
        self.appliance_number.setObjectName('appliance_args')
        self.appliance_power.setObjectName('appliance_args')
        self.appliance_time.setObjectName('appliance_args')
        self.appliance_efficiency.setObjectName('appliance_args')
        self.appliance_model.setEnabled(False)
        self.appliance_number.setEnabled(False)
        self.appliance_power.setEnabled(False)
        self.appliance_time.setEnabled(False)
        self.appliance_efficiency.setEnabled(False)
        appliance_time_label = QLabel('Выберите указанную единицу измерения *')
        appliance_time_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_time_flag = QComboBox()
        self.appliance_time_flag.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_time_flag.addItem('Часы')
        self.appliance_time_flag.addItem('Минуты')
        self.appliance_time_flag.addItem('Секунды')
        self.appliance_time_flag.activated[str].connect(self.appliance_time_flag_function)
        self.appliance_time_flag.setEnabled(False)

        appliance_save = QPushButton('Сохранить')
        appliance_save.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        appliance_save.setObjectName('appliance_save')

        self.information_logs = QListWidget()
        self.information_logs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.information_logs.setObjectName('information_logs')


        appliance_list_label = QLabel('Выберите электроприбор:')
        appliance_list_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_list = QListWidget()
        self.appliance_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_list.setObjectName('self.appliance_list')

        appliance_delete = QPushButton('Удалить')
        appliance_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        appliance_delete.setObjectName('appliance_delete')

        appliance_add_box = QComboBox()
        appliance_add_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        appliance_add_box.setObjectName('appliance_add_box')
        appliance_add_box.addItem('')
        for key in appliance:
            appliance_add_box.addItem(str(key))
        appliance_add_box.activated[str].connect(self.add_appliance)   

        spacer = QLabel()
        spacer.setObjectName('spacer')


        main_layout = QHBoxLayout()
        layout_first = QVBoxLayout()
        self.layout_second = QVBoxLayout()
        layout_third = QVBoxLayout()
        layout_c_buttons = QHBoxLayout()
        layout_a_buttons = QVBoxLayout()
        layout_device = QVBoxLayout()
        self.layout_result = QVBoxLayout()
        self.layout_result_selected = QHBoxLayout() 

        self.layout_result_selected.addWidget(self.result_money)
        self.layout_result_selected.addWidget(self.result_loss)

        self.layout_result.addWidget(self.result_all_money)
        self.layout_result.addWidget(self.result_all_loss)

        layout_c_buttons.addWidget(configurations_create)
        layout_c_buttons.addWidget(configurations_delete)

        layout_device.addWidget(appliance_information_label, stretch=1)
        layout_device.addWidget(appliance_type_label, stretch=1)
        layout_device.addWidget(self.appliance_type, stretch=1)
        layout_device.addWidget(self.appliance_model, stretch=1)
        layout_device.addWidget(self.appliance_number, stretch=1)
        layout_device.addWidget(self.appliance_power, stretch=1)
        layout_device.addWidget(self.appliance_time, stretch=1)
        layout_device.addWidget(appliance_time_label, stretch=1)
        layout_device.addWidget(self.appliance_time_flag, stretch=1)
        layout_device.addWidget(self.appliance_efficiency, stretch=1)
        layout_device.addWidget(appliance_save, stretch=1)

        layout_a_buttons.addWidget(appliance_delete)
        layout_a_buttons.addWidget(appliance_add_box)

        layout_first.addWidget(configurations_list_label, stretch=2) #изменить
        layout_first.addWidget(self.configurations_list, stretch=64)
        layout_first.addLayout(layout_c_buttons, stretch=5)
        
        self.layout_second.addWidget(result_label, stretch=2)
        self.layout_second.addWidget(self.result_logs, stretch=2)
        self.layout_second.addWidget(spacer, stretch=2)
        self.layout_second.addLayout(layout_device, stretch=8)
        self.layout_second.addWidget(self.information_logs, stretch=4)

        layout_third.addWidget(appliance_list_label, stretch=1)
        layout_third.addWidget(self.appliance_list, stretch=64)
        layout_third.addLayout(layout_a_buttons, stretch=5)

        main_layout.addLayout(layout_first, stretch=2)
        main_layout.addLayout(self.layout_second, stretch=7)
        main_layout.addLayout(layout_third, stretch=3)

        self.configurations_list.itemClicked.connect(self.show_third)
        configurations_create.clicked.connect(self.create_configuration)
        configurations_delete.clicked.connect(self.delete_configuration)
        self.appliance_list.itemClicked.connect(self.show_second_list)
        self.result_logs.itemClicked.connect(self.show_results)
        appliance_delete.clicked.connect(self.delete_appliance)
        appliance_save.clicked.connect(self.save_appliance)

        self.setLayout(main_layout)

        self.d = 1

    #!Методы
    '''
    writing():
        Метод, сохраняющий данные в файл
    message(message):
        Метод, показывающий пользователю информацию о работе программы через information_logs
        Специальные аргументы метода:
            message - сообщение, выводимое пользователю

    show_results():
        Метод, показывающий результаты работы программы в специально отведённой для этого врехней части центральной части программы
    hide_results():
        Метод, скрывающий результаты работы программы (необходимо при изменении конфигурации)

    show_third():
        Метод, меняющий информацию в правой части приложения при смене конфигурации

    show_second_list():
        Метод, отвечающий за показ результатов вычислений в центральном секторе
    show_second(name):
        Метож, меняющий информацию в центральном секторе при смене прибора
        Специальные аргументы метода:
            name.

    create_configuration():
        Метод создания конфигурации
    delete_configuration():
        Метод удаления выбранной конфигурации

    add_appliance():
        Метод добавления выбранного прибора
    save_appliance():
        Метод сохранения инфрмации о редактируемом приборе
    delete_appliance():
        Метод удаления выбранного прибора

    result(number, power, time, n, l):
        Метод, связывающий расчёты в файле module.py с файлом main.py
        Специальные аргументы метода:
            number - количсетво электроприборов
            power - мощность электроприборов
            time - среднее время работы электроприбора в день
            n - КПД электроприбора (если известно). По умолчанию = 100
            l - длина кабеля до электроприбора. Специальная величина, которая будет в дальнейших версиях позволит делать точные расчёты даже для многоквартирных домов

    appliance_type_function(text):
        Метод, добавляющий в appliance_type возможные стандартные типы электроприборов (например, чайник может быть стеклянным, пластмассовым или же металлическим, и в зависимости от данного свойства можно определить приблизительное его КПД)
        Специальные аргументы метода:
            text - вид выфбранного электроприбора
    appliance_time_flag_function(text):
        Метод перевода часов и минут в секунды. Как оказалось, делать это самостоятельно компьютер не хочет.
        Специальные аргументы метода:
            text - выбранная единица измерения (часы, минуты, секунды)

    float_checking():
        Метод проверки правильного введения данных в поля ввода (в данных полях должны быть введены данные типа float, т.е. дробные или целочисленные значения. Никаких букв или специальных символов!)
    must_have_checker():
        Метод проверки достаточности введённых в поля ввода данных для расчётов (каким образом можно вычислить расходы, если сам пользователь не знает, сколько чайников у него работает?)
    '''
    #TODO def _widget(self, parent, **kwargs): #TODO Instead of setting size policy, object name and etc. in __init__ I can do it in private method. But how?
    #TODO     widget = parent(kwargs['text'])
    #TODO     widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    #TODO     widget.setObjectName(kwargs['text'])
    #TODO     return widget

    #?Упрощающие жизнь методы
    def writing(self) -> None:
        with open(r'data\user_data\config\data.json', 'w', encoding='utf-8') as file:          
            dump(data, file, sort_keys=True, ensure_ascii=False, indent=4)   

    def message(self, message: str) -> None:
        self.information_logs.addItem(f"[{str(time.ctime(time.time()))}]:       {message}") 


    #?Контроль панели результатов
    def show_results(self) -> None:
        self.layout_second.insertLayout(1, self.layout_result)              
        self.layout_second.insertLayout(3, self.layout_result_selected)     
        self.show_second(name=self.result_logs.selectedItems()[0].text())   

    def hide_results(self) -> None:
        if results_shown:                                    
            self.layout_second.removeItem(self.layout_result)                   
            self.layout_second.removeItem(self.layout_result_selected)          
            self.show_second(name=self.result_logs.selectedItems()[0].text())   


    #?Контроль правого сектора приложения
    def show_third(self) -> None:
        key = self.configurations_list.selectedItems()[0].text()    
        self.appliance_list.clear()                                 
        self.appliance_list.addItems(data[key])                     
        self.result_logs.clear()                                    
        for item in data[key]:                               
            self.result_logs.addItem(item)


    #?Контроль центрального сектора приложения
    def show_second_list(self) -> None:
        self.show_second(name=self.appliance_list.selectedItems()[0].text()) 

    def show_second(self, name: str) -> None:
        key = self.configurations_list.selectedItems()[0].text()                                             
        self.appliance_type.clear()                                                                                     
        self.appliance_type.setEnabled(True)                                                                            
        self.appliance_model.clear()                                                                                    
        self.appliance_model.setEnabled(True)                                                                          
        self.appliance_number.clear()                          
        self.appliance_number.setEnabled(True)                 
        self.appliance_power.clear()                           
        self.appliance_power.setEnabled(True)                  
        self.appliance_time.clear()                            
        self.appliance_time.setEnabled(True)                   
        self.appliance_efficiency.clear()                      
        self.appliance_efficiency.setEnabled(True)                                                                                    
        self.appliance_time_flag.setCurrentText('Секунды')                                                                         
        self.appliance_time_flag.setEnabled(True)
        if appliance[name] != '':
            for item in appliance[name]:     
                self.appliance_type.addItem(str(item))
            self.appliance_type.activated[str].connect(self.appliance_type_function)
        if data[key][name]['data'][0] != 0:
            self.appliance_number.setText(str(data[key][name]['data'][0]))             
            self.appliance_power.setText(str(data[key][name]['data'][1]))                                 
            self.appliance_time.setText(str(data[key][name]['data'][2]))
            self.appliance_efficiency.setText(str(data[key][name]['data'][3] * 100))
            self.appliance_model.setText(data[key][name]['data'][4])
            self.appliance_type.setCurrentText(str(data[key][name]['data'][5][0]))
            self.result_loss.setText('Потери для электроприбора:' + str(data[key][name]['result'][0]))
            self.result_money.setText('Затраты на электроприбор:' + str(data[key][name]['result'][1]))
            self.result_all_loss.setText('Потери всего:' + '\t' + str(sum(data[key][key1]['result'][0] for key1 in data[key])))
            self.result_all_money.setText('Затраты всего:' + '\t' + str(sum(data[key][key1]['result'][1] for key1 in data[key])))


    #?Сонтроль конфигураций
    def create_configuration(self) -> None:
        configuration_name, ok = QInputDialog.getText(main, lang.add_cofiguration, lang.name_of_cofiguration)
        if ok and configuration_name != '':
            self.hide_results()
            data.update({configuration_name: {}})
            self.configurations_list.addItem(configuration_name)
            self.writing()
        elif configuration_name == '':
            self.message(lang.name_unspecified)                                                                 

    def delete_configuration(self) -> None:
        if self.configurations_list.selectedItems():
            self.hide_results()
            data.pop(self.configurations_list.selectedItems()[0].text())
            self.configurations_list.clear()
            self.appliance_list.clear()
            self.configurations_list.addItems(data)
            self.writing()
        else:
            self.message(lang.configuration_unselected_deleting)            


    #?Контроль приборов
    def add_appliance(self, text:str) -> None:
        try:
            if text != '':
                self.appliance_list.addItem(text)
                data[self.configurations_list.selectedItems()[0].text()][str(text)] = {'data': [0, 0, 0, 0, '', ['', 0]], 'result': [0, 0]}
                self.writing()
        except IndexError:
            self.message(lang.configuration_unselected)                                                                                     


    def save_appliance(self) -> None:
        if self.configurations_list.selectedItems() and self.appliance_list.selectedItems():
            if self.float_checking() and self.must_have_checker():
                key, key1 = self.configurations_list.selectedItems()[0].text(), self.appliance_list.selectedItems()[0].text()
                number, power, time = self.must_have_checker()
                self.appliance_type_function()
                if self.appliance_efficiency.text() != '':
                    n = float(self.appliance_efficiency.text()) / 100
                else:
                    n = data[key][key1]['data'][5][1]
                data[key][key1]['data'] = [int(number), float(power), float(time), n, self.appliance_model.text(), data[key][key1]['data'][5]]
                self.appliance_efficiency.setText(str(n * 100))     
                self.result(number, power, time * self.d, n)
        else:
            self.message(lang.configuration_unselected_saving)                                                                                  

    def delete_appliance(self) -> None:
        if self.configurations_list.selectedItems() and self.appliance_list.selectedItems():
            self.hide_results()
            key, key1 = self.configurations_list.selectedItems()[0].text(), self.appliance_list.selectedItems()[0].text()
            data[key].pop([key1])
            self.appliance_list.clear()
            self.appliance_list.addItems(data[key])
            self.writing()
        else:
            self.message(lang.device_unselected)                                                                            


    #?Результат
    def result(self, number:int, power:float, time:float, n:float, l=1) -> None:
        key, key1 = self.configurations_list.selectedItems()[0].text(), self.appliance_list.selectedItems()[0].text()
        if key[0] != 0:
            self.result_logs.clear()
            data[key][key1]['result'] = resulting(key1, power, time, number, n, l)
            for item in data[key]:
                self.result_logs.addItem(item)
            self.writing()                                                                                              


    #?Методы работы с QComboBox
    def appliance_type_function(self) -> None:
        text = self.appliance_type.currentText()
        key, key1 = self.configurations_list.selectedItems()[0].text(), self.appliance_list.selectedItems()[0].text()
        data[key][key1]['data'][5] = [str(text), appliance[self.appliance_list.selectedItems()[0].text()][text]]        

    def appliance_time_flag_function(self, text:str) -> None:
        if text == 'Часы':
            self.d = 3600
        elif text == 'Минуты':                          
            self.d = 60
        else:                                           
            self.d = 1


    #?Проверяющие методы (Методы контроля вводимых данных) (Checkers)
    def float_checking(self) -> bool:
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
                        self.message((key) + 'должен содеражть число с плавающей точкой (",") или целое число') 
                    flag = False
        return flag                                                                                             

    def must_have_checker(self) -> tuple:
        must_have = self.appliance_number.text(), self.appliance_power.text(), self.appliance_time.text()
        for data in must_have:
            if data == '':
                self.message(f'Параметр {data} обязателен для заполнения!')
                return False
        return int(self.appliance_number.text()), float(self.appliance_power.text()), float(self.appliance_time.text()) * self.d    



if __name__ == '__main__':
    app = QApplication([argv])                                                                  

    try:
        from module import resulting, appliance, start                            
                                                                 
        start()                                                                                 

        main = Window()                              
        main.setWindowTitle('ElectricityManager')
        main.resize(1900, 1080)                                                                 


        main.message('Старт программы')                                                         


        with open(r'data\user_data\config\data.json', 'r', encoding='utf-8') as file:
            data = load(file)
        main.configurations_list.addItems(data)
        #?В данном файле содержится инструкции оформления приложения в формате qss (аналог css для Qt)
        with open(r'design\main.qss', 'r') as file:
            app.setStyleSheet(file.read())                                                      

        main.show()                                                                             

        exit(app.exec_())                                              

    except ImportError:
        print('Файлы программы повреждены (module.py не найден). Обратитесь к разработчику.')
    except FileNotFoundError:
        print('Файлы программы повреждены. Обратитесь к разработчику.')                         