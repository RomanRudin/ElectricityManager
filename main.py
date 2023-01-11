#Импортирование Библиотек
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QComboBox, QSizePolicy
from sys import argv, exit
import time
import json
import localization as lang

results_shown = False
data = {}

class Window(QWidget): #Класс, объекты которого являются самим приложением. Является дочерним классом QWidget
    def __init__(self): #Конструктор класса
        super().__init__()#Указание, что данный класс наследует все свойства родительского класса
        '''
        QLabel('text') - виджет, представляющий из себя строку текста text.
        QListWidget() - виджет, представляющий из себя пролистываемый список выбираемых объектов-строчек.
        QPushButton('text') - виджет, представляющий из себя кнопку с текстом text.
        QComboBox() - виджет, представляющий из себя выпадающий список с выбираемыми объектами-строчками.
        QLineEdit() - виджет, представляющий из себя доступную для редактирования строчку текста. Поле ввода в одну строчку.
        QLineEditWidget.setPlaceholderText('text') - команда, устанавливающая для QLineEdit виджета текст по умолчанию
        QInputDialog('text', 'button1', 'button2' ...) - виджет, представляющий из себя отдельно открывающееся окно однострочным текстом text и выбираемым количеством кнопок (по умолчанию - 2) с текстами button1, button2 и т.д. соответственно.
        №№№Виджет - 
        №№№Layout - тип виджетов, являющийся структурным элементом и позволяющий удобно располагать виджеты в приложении.
        QHBoxLayout() - вертикальный Layout.
        QVBoxLayout() - горизонтальный Layout.
        object.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) - команда, разрешающая виджетам менять свои абсолютные размеры при изменении разрешения экрана, сохраняя относительные размеры.
        object.setObjectName('object_name') - 
        '''


        #Левая часть приложения. Отвечает за создание, выбор и удаление конфигураций.
        #Надпись 'Выберите конфигурацию из уже существующих или добавьте новую:'
        configurations_list_label = QLabel('Выберите конфигурацию из уже существующих или добавьте новую:')
        configurations_list_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #Список существующих конфигураций
        self.configurations_list = QListWidget()
        self.configurations_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        #Кнопки создания и удаления конфигураций
        configurations_create = QPushButton('Создать')
        configurations_delete = QPushButton('Удалить')
        configurations_create.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        configurations_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        configurations_create.setObjectName('configurations_buttons')
        configurations_delete.setObjectName('configurations_buttons')


        #Центральная часть приложения. Отвечает за редактирование параметров прибора, показ сообщений о работе приложения, результаты работы программы.
        #Надпись "Результаты вычислений:"
        result_label = QLabel("Результаты вычислений:")
        result_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #Надписи для вывода потерь электроэнергии и денег для всех приборов 
        self.result_all_loss = QLabel("")
        self.result_all_money = QLabel("")
        self.result_all_loss.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_all_money.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_all_loss.setObjectName('result_info')
        self.result_all_money.setObjectName('result_info')
        #Список типов приборов, для которых были выполнены вычисления
        self.result_logs = QListWidget()
        self.result_logs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_logs.setObjectName('result_logs')
        #Надписи для вывода потерь электроэнергии и денег для выбранного типа электроприборов 
        self.result_loss = QLabel("")
        self.result_money = QLabel("")
        self.result_loss.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_money.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.result_loss.setObjectName('result_info')
        self.result_money.setObjectName('result_info')

        #Надпись 'Введите данные. Обязательные для ввода поля помечены *'
        appliance_information_label = QLabel('Введите данные. Обязательные для ввода поля помечены *')
        appliance_information_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        appliance_information_label.setObjectName('appliance_information_label')
        #Надпись 'Выберите тип электроприбора *'
        appliance_type_label = QLabel('Выберите тип электроприбора *')
        appliance_type_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #Выпадающее меню выбора свойств прибора
        self.appliance_type = QComboBox()
        self.appliance_type.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #Поля ввода данных
        self.appliance_model = QLineEdit()
        self.appliance_number  = QLineEdit()
        self.appliance_power = QLineEdit()
        self.appliance_time = QLineEdit()
        self.appliance_efficiency = QLineEdit()
        self.appliance_model.setPlaceholderText('Модель / марка прибора')
        self.appliance_number.setPlaceholderText('Количество приборов *')
        self.appliance_power.setPlaceholderText('Мощность приборов *')
        self.appliance_time.setPlaceholderText('Время работы в сутки *')
        self.appliance_efficiency.setPlaceholderText('КПД прибора')
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
        #Надпись 'Выберите указанную единицу измерения *'
        appliance_time_label = QLabel('Выберите указанную единицу измерения *')
        appliance_time_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #Выпадающее меню выбора единиц измерения времени
        self.appliance_time_flag = QComboBox()
        self.appliance_time_flag.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_time_flag.addItem('Часы')
        self.appliance_time_flag.addItem('Минуты')
        self.appliance_time_flag.addItem('Секунды')
        self.appliance_time_flag.activated[str].connect(self.appliance_time_flag_function) #Подключение метода appliance_time_flag_function для активированного appliance_time_flag

        #Кнопка сохранения 
        appliance_save = QPushButton('Сохранить')
        appliance_save.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        appliance_save.setObjectName('appliance_save')

        #Информационные логи, т.е. место для вывода сообщений для пользователя
        self.information_logs = QListWidget()
        self.information_logs.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.information_logs.setObjectName('information_logs')


        #Правая часть приложения. Отвечает за добавление, выбор и удаление приборов.
        #Надпись 'Выберите электроприбор:'
        appliance_list_label = QLabel('Выберите электроприбор:')
        appliance_list_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #Список существующих приборов
        self.appliance_list = QListWidget()
        self.appliance_list.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.appliance_list.setObjectName('self.appliance_list')

        #Кнопка удаления существующего прибора
        appliance_delete = QPushButton('Удалить')
        appliance_delete.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        appliance_delete.setObjectName('appliance_delete')

        #Выпадающее меню выбора электроприбора для добавления
        appliance_add_box = QComboBox()
        appliance_add_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        appliance_add_box.setObjectName('appliance_add_box')
        appliance_add_box.addItem('')
        for key in appliance: #цикл, перебирающий ключи словаря appliance 
            appliance_add_box.addItem(str(key)) #добавление элемента key в виджет appliance_add_box
        appliance_add_box.activated[str].connect(self.add_appliance)   

        #Виджет-пробел. Сделан для лучшего дизайна приложения. Костыль, но переделывать лень.
        spacer = QLabel()
        spacer.setObjectName('spacer')


        #Layouts
        main_layout = QHBoxLayout()                 #Главный layout
        layout_first = QVBoxLayout()                #Layout левого сектора 
        self.layout_second = QVBoxLayout()          #Layout центрального сектора 
        layout_third = QVBoxLayout()                #Layout правого сектора 
        layout_c_buttons = QHBoxLayout()            #Layout кнопок управления конфигурациями
        layout_a_buttons = QVBoxLayout()            #Layout кнопок управления приборами
        layout_device = QVBoxLayout()               #Layout редактирования приборов
        self.layout_result = QVBoxLayout()          #Динамический layout  #? dynamic layout 
        self.layout_result_selected = QHBoxLayout() #Динамический layout  #? dynamic layout

        #Добавление виджетов в layout_result_selected:
        self.layout_result_selected.addWidget(self.result_money)
        self.layout_result_selected.addWidget(self.result_loss)

        #Добавление виджетов в layout_result
        self.layout_result.addWidget(self.result_all_money)
        self.layout_result.addWidget(self.result_all_loss)

        #Добавление виджетов в layout_c_buttons
        layout_c_buttons.addWidget(configurations_create)
        layout_c_buttons.addWidget(configurations_delete)

        #Добавление виджетов в layout_device
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

        #Добавление виджетов в layout_a_buttons
        layout_a_buttons.addWidget(appliance_delete)
        layout_a_buttons.addWidget(appliance_add_box)

        #Добавление виджетов и layout-ов в layout_first
        layout_first.addWidget(configurations_list_label, stretch=2) #изменить
        layout_first.addWidget(self.configurations_list, stretch=64)
        layout_first.addLayout(layout_c_buttons, stretch=5)
        
        #Добавление виджетов и layout-ов в layout_second
        self.layout_second.addWidget(result_label, stretch=2)
        self.layout_second.addWidget(self.result_logs, stretch=2)
        self.layout_second.addWidget(spacer, stretch=2)
        self.layout_second.addLayout(layout_device, stretch=8)
        self.layout_second.addWidget(self.information_logs, stretch=4)

        #Добавление виджетов и layout-ов в layout_third
        layout_third.addWidget(appliance_list_label, stretch=1)
        layout_third.addWidget(self.appliance_list, stretch=64)
        layout_third.addLayout(layout_a_buttons, stretch=5)

        #Добавление layout-ов в main_layout
        main_layout.addLayout(layout_first, stretch=2)
        main_layout.addLayout(self.layout_second, stretch=7)
        main_layout.addLayout(layout_third, stretch=3)

        #Обработка событий, т.е. подключение методов из аргументов connect() к активированным виджетам
        self.configurations_list.itemClicked.connect(self.show_third)
        configurations_create.clicked.connect(self.create_configuration)
        configurations_delete.clicked.connect(self.delete_configuration)
        self.appliance_list.itemClicked.connect(self.show_second_list)
        self.result_logs.itemClicked.connect(self.show_results)
        appliance_delete.clicked.connect(self.delete_appliance)
        appliance_save.clicked.connect(self.save_appliance)

        #Установка главного layout-а
        self.setLayout(main_layout)

        #Перемнная для перевода времени в секунды
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
            name - не помню №№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№№

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

    #Упрощающие жизнь методы
    def writing(self):
        with open('data.json', 'w', encoding='utf-8') as file:          #Открытие файла data.json для перезаписи в кодировке utf-8. Теперь к этому файлу в пределах действия ключевого слова with можно обращаться file
            json.dump(data, file, sort_keys=True, ensure_ascii=False)   #Запись данных из словаря data в file. Ключи сортируются, перевод символов в кодировку ASCII не производится

    def message(self, message):
        self.information_logs.addItem(f"[{str(time.ctime(time.time()))}]:       {message}") #Добавление элемента с текстом сообщения и временем получения данного сообщения в information_logs


    #Контроль панели результатов
    def show_results(self):
        self.layout_second.insertLayout(1, self.layout_result)              #Добавление layout_result в layout_second на первое место
        self.layout_second.insertLayout(3, self.layout_result_selected)     #Добавление layout_result_selected в layout_second на третее место
        self.show_second(name=self.result_logs.selectedItems()[0].text())   #Вызов метода show_second с аргументом name равным тексту первого выбранного элемента result_logs

    def hide_results(self):
        if results_shown:                                                       #Если результаты уже были показаны:
            self.layout_second.removeItem(self.layout_result)                   #Удаление layout_result из layout_second
            self.layout_second.removeItem(self.layout_result_selected)          #Удаление layout_result_selected из layout_second
            self.show_second(name=self.result_logs.selectedItems()[0].text())   #Вызов метода show_second с аргументом name равным тексту первого выбранного элемента result_logs


    #Контроль правого сектора приложения
    def show_third(self):
        key = self.configurations_list.selectedItems()[0].text()    #В перемнную key записывается первый выбранный элемент из configurations_list
        self.appliance_list.clear()                                 #Очистка appliance_list
        self.appliance_list.addItems(data[key])                     #Добавление элементов из словаря, находящегося в словару data под ключом key в appliance_list
        self.result_logs.clear()                                    #Очистка result_logs
        for item in data[key]:                                      #Цикл перебирает элементы из словаря, находящегося в словару data под ключом key в appliance_list, называя при каждой итерации соответсвующую информацию из data[key] item
            self.result_logs.addItem(item)                          #Добавление элемента item в result_logs


    #Контроль центрального сектора приложения
    def show_second_list(self):
        self.show_second(name=self.appliance_list.selectedItems()[0].text()) #Вызов метода show_second с аргументом name равным тексту первого выбранного элемента appliance_list

    def show_second(self, name):
        key = self.configurations_list.selectedItems()[0].text()                                                    #В перемнную key записывается первый выбранный элемент из configurations_list
        self.appliance_type.clear()                                                                                 #Очистка appliance_type
        self.appliance_number.clear()                                                                               #Очистка appliance_number
        self.appliance_power.clear()                                                                                #Очистка appliance_power
        self.appliance_time.clear()                                                                                 #Очистка appliance_time
        self.appliance_efficiency.clear()                                                                           #Очистка appliance_efficiency
        self.appliance_time_flag.setCurrentText('Секунды')                                                          #Установка выбранного значения appliance_time_flag на стандартное (секунды)
        if appliance[name] != '':                                                                                   #Если у прибора с названием name есть какие-то специальнык свойства, т.е. если словарь appliance содержит хоть какие-то элементы:
            for item in appliance[name]:                                                                            #Цикл, перебирающий данные из appliance[name]
                self.appliance_type.addItem(str(item))                                                              #Добавление элемента item в appliance_type
            self.appliance_type.activated[str].connect(self.appliance_type_function)                                #Подключение метода appliance_type_function к событию активации appliance_type
        if data[key][name]['data'][0] != 0:                                                                         #Если какие-то данные для этого электроприбора уже были сохранены, т.е. если первый элемент списка под ключом data словаря под ключом name в словаре под ключом key в словаре data, являющийся количеством жлектроприборов, (т.е. обязательным элементом) не равен нулю (т.е. был сохранён):
            #data showing                           
            self.appliance_number.setText(str(data[key][name]['data'][0]))                                          #Установка в appliance_number сохранённого количества электроприборов для данного вида приборов, т.е. первого элемента списка под ключом data словаря под ключом name в словаре под ключом key в словаре data
            self.appliance_power.setText(str(data[key][name]['data'][1]))                                           #Установка в appliance_power сохранённой мощности электроприборов для данного вида приборов,
            self.appliance_time.setText(str(data[key][name]['data'][2]))                                            #Установка в appliance_time сохранённого времени работы  электроприборов для данного вида приборов,
            self.appliance_efficiency.setText(str(data[key][name]['data'][3]))                                      #Установка в appliance_efficiency сохранённого КПД электроприборов для данного вида приборов,
            self.appliance_model.setText(data[key][name]['data'][4])                                                #Установка в appliance_model сохранённой можели электроприборов для данного вида приборов,
            self.appliance_type.setCurrentText(str(data[key][name]['data'][5][0]))                                  #Установка в appliance_type сохранённого типа (свойства) электроприборов для данного вида приборов,
            #result showing                         
            self.result_loss.setText('' + str(data[key][name]['result'][0]))                                        #Установка в result_loss сохранённых потерь электроэнергии электроприборов для данного вида приборов,
            self.result_money.setText('' + str(data[key][name]['result'][1]))                                       #Установка в result_money сохранённоых потерь денег электроприборов для данного вида приборов,
            self.result_all_loss.setText('Loss' + str(sum(data[key][key1]['result'][0] for key1 in data[key])))     #Установка в result_all_loss сохранённых потерь электроэнергии суммарно
            self.result_all_money.setText('Money' + str(sum(data[key][key1]['result'][1] for key1 in data[key])))   #Установка в result_all_money сохранённых потерь денег суммарно


    #Сонтроль конфигураций
    def create_configuration(self): #Добавление заметки
        configuration_name, ok = QInputDialog.getText(main, lang.add_cofiguration, lang.name_of_cofiguration)   #Создание диалогового окна
        if ok and configuration_name != '':                                                                     #Если пользователь нажал на кнопку ok и имя конфигурации заполнено:
            self.hide_results()                                                                                 #Вызов метода, скрывающего результаты предыдущих вычислений
            data.update({configuration_name: {}})                                                               #Добавление в словарь data пары значение-ключ configuration_name: {}
            self.configurations_list.addItem(configuration_name)                                                #Добавление элемента configuration_name в виджет configurations_list
            self.writing()                                                                                      #Сохранение изменений
        elif configuration_name == '':                                                                          #Если название конфигурации не было выбрано:
            self.message(lang.name_unspecified)                                                                 #Вывод сообщения "имя конфигурации не может быть пустым"

    def delete_configuration(self): 
        if self.configurations_list.selectedItems():                        #Если какие-либо из элементов configurations_list были выделены:
            self.hide_results()                                             #Вызов метода, скрывающего результаты предыдущих вычислений
            data.pop(self.configurations_list.selectedItems()[0].text())    #Запись первого из выбранных элементов configurations_list в переменную key
            self.configurations_list.clear()                                #Очистка configurations_list
            self.appliance_list.clear()                                     #Очистка appliance_list
            self.configurations_list.addItems(data)                         #Добавление элементов из data в configurations_list
            self.writing()                                                  #Сохранение изменений
        else:                                                               #Иначе:
            self.message(lang.configuration_unselected_deleting)            #Вывод сообщения "конфигурация для удаления не выбрана"


    #Контроль приборов
    def add_appliance(self, text):
        try:                                                                                                                                    #Попробовать выполнить дальнейший код:
            if text != '':                                                                                                                  #Если text не является пустой строкой:
                self.appliance_list.addItem(text)                                                                                           #Добавление в appliance_list элемента text
                data[self.configurations_list.selectedItems()[0].text()][str(text)] = {'data': [0, 0, 0, 0, '', ['', 0]], 'result': [0, 0]} #Создание новой пустой формы для типа электроприборов
                self.writing()                                                                                                              #Сохранение изменений
        except IndexError:                                                                                                                      #Если возникла ошибка превышения индекса списка:
            self.message(lang.configuration_unselected)                                                                                         #Вывод сообщения "Конфигурация не выбрана"

    def save_appliance(self):
        if self.configurations_list.selectedItems() and self.appliance_list.selectedItems():                                                        #Если какие-либо конфигурация и электроприбор выделены:
            if self.float_checking() and self.must_have_checker():                                                                                  #Если данные из центрального сектора прошли проверку на тип и достаточность:
                key, key1 = self.configurations_list.selectedItems()[0].text(), self.appliance_list.selectedItems()[0].text()                       #Запись первого элемента выбранных конфигурации и типа электроприбора в переменные key и key1 соответственно
                number, power, time = self.must_have_checker()                                                                                      #Запись преобразованных в тип float и возвращённых методом must_have_checker данных
                if self.appliance_efficiency.text() != '':                                                                                          #Если поле КПД заполнено:
                    n = float(self.appliance_efficiency.text()) / 100                                                                               #Запись преобразованного в тип float КПД
                    data[key][key1]['data'] = [int(number), float(power), float(time), n, self.appliance_model.text(), data[key][key1]['data'][5]]  #Запись введённых данных в созданную форму
                    self.result(number, power, time * self.d, n)                                                                                    #Вызов метода расчёта потерь с приведёнными данными
                else:                                                                                                                               #Иначе:
                    data[key][key1]['data'] = [int(number), float(power), float(time), '', self.appliance_model.text(), data[key][key1]['data'][5]] #Запись введённых данных в созданную форму
                    self.result(number, power, time * self.d)                                                                                       #Вызов метода расчёта потерь с приведёнными данными
        else:                                                                                                                                       #Иначе:
            self.message(lang.configuration_unselected_saving)                                                                                      #Вывод сообщения "Конфигурация или прибор не выбраны"

    def delete_appliance(self):
        if self.configurations_list.selectedItems() and self.appliance_list.selectedItems():                                #Если какие-либо конфигурация и электроприбор выделены:
            self.hide_results()                                                                                             #Вызов метода, скрывающего результаты предыдущих вычислений
            key, key1 = self.configurations_list.selectedItems()[0].text(), self.appliance_list.selectedItems()[0].text()   #Запись первого элемента выбранных конфигурации и типа электроприбора в переменные key и key1 соответственно
            data[key].pop([key1])                                                                                           #Удаление элемента key1 из словаря под ключом key словаря data
            self.appliance_list.clear()                                                                                     #Очистка appliance_list
            self.appliance_list.addItems(data[key])                                                                         #Добавление элементов из словаря под ключом key словаря data в appliance_list
            self.writing()                                                                                                  #Сохранение изменений
        else:                                                                                                               #Иначе:
            self.message(lang.device_unselected)                                                                            #Вывод сообщения "Прибор не выбран"


    #Результат
    def result(self, number, power, time, n=0, l=0):
        key, key1 = self.configurations_list.selectedItems()[0].text(), self.appliance_list.selectedItems()[0].text()   #Запись первого элемента выбранных конфигурации и типа электроприбора в переменные key и key1 соответственно
        if key[0] != 0:                                                                                                 #Если первый элемент key не равен нулю, т.е. был изменён пользователем:
                self.result_logs.clear()                                                                                #Очистка result_logs
                data[key][key1]['result'] = resulting(key1, power, time, number, n, l)                                  #Запись данных, полученных а результате вычислений в data (а точнее в список-форму под ключом result словаря под ключом key1 под ключом key словаря data)
                for item in data[key]:                                                                                  #Цикл перебирает элементы из словаря, находящегося в словару data под ключом key в appliance_list, называя при каждой итерации соответсвующую информацию из data[key] item
                    self.result_logs.addItem(item)                                                                      ##Добавление элемента item в result_logs
                self.writing()                                                                                          #Сохранение изменений


    #Упрощающие жизнь методы
    def appliance_type_function(self, text):
        key, key1 = self.configurations_list.selectedItems()[0].text(), self.appliance_list.selectedItems()[0].text()   #Запись первого элемента выбранных конфигурации и типа электроприбора в переменные key и key1 соответственно
        data[key][key1]['data'][5] = [str(text), appliance[self.appliance_list.selectedItems()[0].text()][text]]        #Запись текста свойства прибора и данных КПД из словаря appliance для этого свойства в data

    def appliance_time_flag_function(self, text):
        if text == 'Часы':                              #Если выбранный элемент appiance_time_flag - Часы
            self.d = 3600                               #Переменная d используется для перевода введённого пользователем времени в секунды
        elif text == 'Минуты':                          #Если выбранный элемент appiance_time_flag - Минуты
            self.d = 60                                      
        else:                                           #Иначе
            self.d = 1


    #Проверяющие методы (Checkers)
    def float_checking(self):
        checker = {'время работы': self.appliance_time.text(), 'мощность': self.appliance_power.text(),         #Перезапись введённых данных в словарь для большего удобство работы с ними в дальнейшем
            'количество': self.appliance_number.text(), 'КПД': self.appliance_efficiency.text()}                
        flag = True                                                                                             
        for key in checker:                                                                                     #Для каждого из элементов checker:
            data = checker[key]                                                                                 
            if data != '':                                                                                      #Если перебираемые данные всё же были введены
                try:                                                                                            #Попробовать выполнить дальнейший код:
                    if key == 'количество':                                                                     #Если итерируемые сейчас данные - это количество электроприборов:
                        data = int(data)                                                                        
                    else:                                                                                       #Иначе:
                        data = float(data)                                                                      
                except ValueError:                                                                              #Если возникла ошибка перевода значения из одного типа в другой (например, если количество приборов - не целое число или при его наборе пользователь использовал буквы):
                    if key == 'количество':                                                                     #Если ошибка возникла при попытке перевода количества в целочисленнок значение:
                        self.message(lang.parameter + str(key) + lang.must_be_an_integer)                       #Вывод сообщения "Количество приборов должно быть целым числом"
                    else:                                                                                       #Иначе:
                        self.message((key) + 'должен содеражть число с плавающей точкой (",") или целое число') #Вывод сообщения "... должен содеражть число с плавающей точкой (",") или целое число'"
                    flag = False                                                                                
        return flag                                                                                             #Метод при вызове вернёт значение переменной flag

    def must_have_checker(self):
        must_have = self.appliance_number.text(), self.appliance_power.text(), self.appliance_time.text()                           #Запись значений, введённых пользователем в указанные поля ввода в переменную-кортеж (tuple) must_have
        for data in must_have:                                                                                                      #Для каждого элемента в must_have:
            if data == '':                                                                                                          #Если этот элемент не был введён:
                self.message(f'Параметр {data} обязателен для заполнения!')                                                         #Вывод сообщения "Параметр ... обязателен для заполнения!"
                return False                                                                                                        #В этом случае метод вернёт значение False
        return int(self.appliance_number.text()), float(self.appliance_power.text()), float(self.appliance_time.text()) * self.d    #Так как return прерывает дальнейшее выполнение метода, то если все обязательные данные введены, метод вернёт преобразованные значения




if __name__ == '__main__':                                  #Если данный файл является главным (а не дополнительной библиотекой):
    lang.choose_lang(0)                                     #TODO
    start()                                                 #TODO
    app = QApplication([argv])                              #Создание объекта app - экземпляра класса управления логикой графики компьютера QApplication

    main = Window()                                         #Создание объекта main - экземпляра класса Window
    main.setWindowTitle('')                                 #Установка названия приложения
    main.resize(1900, 1080)                                 #Установка разрешения 1900 на 1080


    main.message('Старт программы')                         #Вывод сообщения "Старт программы"

    try:                                                    #Попробовать выполнить код:
        from module import resulting, appliance, start      #Из библиотеки module импортировать resulting, start, appliance
    except ImportError:                                     #Если произошла ошибка импортирования (ошибка подключения библиотеки):
        main.message('Файлы программы повреждены (module.py не найден). Обратитесь к разработчику.') #Вывод сообщения

    with open('data.json', 'r', encoding='utf-8') as file:  #Открытие файла data.json для чтения в кодировке utf-8. Теперь к этому файлу в пределах действия ключевого слова with можно обращаться file
        data = json.load(file)                              #Запись данных из file в словарь data 
    main.configurations_list.addItems(data)                 #Добавление элементов из data в configurations_list
    with open('main.qss', 'r') as file:                     #Открытие файла main.qss для чтения. Теперь к этому файлу в пределах действия ключевого слова with можно обращаться file. #?В данном фалйе содержится инструкции оформления приложения в формате qss (аналог css для Qt)
        app.setStyleSheet(file.read())                      #Установка заданного дизайна

    main.show()                                             #Запуск приложения
                                    
    exit(app.exec_())                                       #При попытке закрыть программу завершить её действие