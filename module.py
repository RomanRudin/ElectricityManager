from json import load

#Словарь средних КПД для различных типов различных приборов
with open(r"data\constants\appliance.json", 'r', encoding='utf-8') as types:
    appliance = load(types)

#Словарь стандартных значений коэффициента φ (фи) для различных электроприборов
with open(r"data\constants\fi.json", 'r', encoding='utf-8') as coef:
    fi = load(coef)

#Словарь стандартных значений для различных проводов
with open(r"data\constants\standart_values.json", 'r', encoding='utf-8') as values:
    standart_values = load(values)

#Заполняемый в процессе вычислений список данных
values = []

#
def start() -> None:
    try:
        with open(r"data\user_data\settings.txt", 'r', encoding='utf-8') as settings:                                                                                                               #Открытие файла settings.txt для чтения в кодировке utf-8. Теперь к этому файлу в пределах действия ключевого слова with можно обращаться settings
            global values                                                                                                                                                           #Далее будет исползоваться глобальная переменная values
            Material, U, S = settings.readline()[:2], settings.readline()[:3], settings.readline()[:4]                                                                              #Парсинг данных из фалйа в переменные
            values = {'p': standart_values['P'][Material][U][S], 'U': int(U), 'S': float(S), 'ro': standart_values['ro'][Material], 'Money': float(S) / (3600 * 1000)}              #
            #Мне необходимы действия / 1_000 * 3600, так как параметр "money" считается по киловатт-часам          
    except FileNotFoundError:                                                                                                                                                       #
        pass                                                                                                                                                                        #

#Функция, собирающая результаты вычислений других функций воедино
def resulting(appliance_name:str, power:float, time:float, number:int, n:float, l:float) -> list:
    return [round(loss_counting(appliance_name, power, time, number, values['Money'], n, l), 2), round(money_counting(power, time, number, values['Money']), 2)]

#Функция, вычисляющая 
def loss_counting(appliance_name:str, power:float, time:float, number:int, money:float, n:float, l:float) -> float:
    power_loss = (2 * (values['p'] ** 2) * values['ro'] * l) / ((values['U'] ** 2) * (values['S'] * 10 ** (-6)) * (fi[appliance_name] ** 2)) * time
    n_loss = (1 - n) * power * number * time
    return (power_loss + n_loss) * money

#Функция, возвращающая потери в денежном эквиваленте
def money_counting(power:float, time:float, number:int, money:float) -> float:
    return (power * time * money * number)