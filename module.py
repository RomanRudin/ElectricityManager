
from optparse import Values


appliance = {
    'Чайник' : {
        'Стеклянный' : 0,
        'Пластмассовый' : 0,
        'Стальной' : 0
    },
    'Лампочка' : {
        'Лампа накаливания' : 0,
        'Энергосберегающая лампа' : 0,
        'Светодиодная лампа' : 0
    },
    'Компьютер' : {
        'Любой' : 0
    },
    'Телевизор' : {
        'Любой' : 0
    },
    'Зарядка' : {
        'Любая' : 0
    },
    'Принтер' : {
        'Любой' : 0
    },
    'Холодильник' : {
        'Любой' : 0
    },
    'Микроволновая печь' : {
        'Любая' : 0
    },
    'Духовая печь' : {
        'Любая' : 0
    },
    'Индукционная плита' : {
        'Любая' : 0
    },
    'Утюг' : {
        'Любой' : 0
    },
    'Стиральная машина' : {
        'Любая' : 0
    },
    'Сушильная машина' : {
        'Любая' : 0
    },
    'Вентмашина' : {
        'Любая' : 0
    },
    'Обогреватель' : {
        'Любой' : 0
    },
    'Электрический котёл' : {
        'Любой' : 0
    },
    'Пылесос' : {
        'Подключаемый' : 0,
        'Заряжаемый' : 0
    }
}

fi = {
    'Чайник' : 1,
    'Лампочка' : 0.95,
    'Компьютер' : 0.95,
    'Телевизор' : 1,
    'Зарядка' : 1,
    'Принтер' : 1,
    'Холодильник' : 0.95,
    'Микроволновая печь' : 1,
    'Духовая печь' : 1,
    'Индукционная плита' : 1,
    'Утюг' : 1,
    'Стиральная машина' : 0.9,
    'Сушильная машина' : 1,
    'Вентмашина' : 1,
    'Обогреватель' : 1,
    'Электрический котёл' : 1,
    'Пылесос' : 0.9
}

#To understand, what's happening here, you must be drunk (but if it's 5 a.m. - than it' it's just optional) an
# you must have links/standart_values.jpg opened on the second screen

standart_values = {'P': {'Cu': {220: {0.50: 1300, 0.75: 2200, 1.00: 3100, 1.50: 3300, 2.00: 4200, 
                                      2.50: 4600, 4.00: 5900, 6.00: 7500, 10.0: 11000}, 
                                380: {0.50: 2300, 0.75: 3800, 1.00: 5300, 1.50: 5700, 2.00: 7200, 
                                      2.50: 8000, 4.00: 10300, 6.00: 12900, 10.0: 19000}},
                        
                         'Al': {220: {1.50: 2200, 2.00: 3100, 2.50: 3500, 
                                      4.00: 4600, 6.00: 5700, 10.0: 8400}, 
                                380: {1.50: 3800, 2.00: 5300, 2.50: 6100, 
                                      4.00: 8000, 6.00: 9900, 10.0: 14400}}},
                   'ro': {'Cu': 1.68 * 10 ** (- 8),
                          'Al': 2.7 * 10 ** (-8)}}

values = []

def start():
    try:
        with open('settings.txt', 'r', encoding='utf-8') as settings:
            global values
            Material, U, S = settings.readline()[:2], int(settings.readline()[:3]), float(settings.readline()[:4])
            values = {'p': standart_values['P'][Material][U][S], 'U': U, 'S': S, 'ro': standart_values['ro'][Material], 'Money': float(settings.readline()[:4]) * 3600 / 1000}
            #Because parameter "money" counts in rilowatts per hour I need / 1_000 * 3600
    except FileNotFoundError:
        pass


def resulting(appliance_name, power, time, number, n, l):
    return [loss_counting(appliance_name, power, time, number, values['Money'], n, l), money_counting(power, time, number, values['Money'])]

def loss_counting(appliance_name, power, time, number, money, n, l):
    power_loss = (2 * (values['p'] ** 2) * values['ro'] * l) / ((values['U'] ** 2) * (values['S'] * 10 ** (-6)) * (fi[appliance_name] ** 2)) * time
    print(power_loss)
    n_loss = (1 - n) * power * number * time
    print(power_loss)
    print((power_loss + n_loss) * money)
    return (power_loss + n_loss) * money

def money_counting(power, time, number, money):
    return (power * time * money * number)


