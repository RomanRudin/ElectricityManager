language = 'EN'
def choose_lang(lang):
    global language
    if lang == 'EN':
        language = 'EN'
    elif lang == 'RU':
        language = 'RU'
    elif lang == 'PL':
        language = 'PL'
    else:
        language = 'EN'
    return lang

with open(f'language\{language}.txt', 'r', encoding='utf-8') as file:
    add_cofiguration = file.readline()
    name_of_cofiguration = file.readline()
    name_unspecified = file.readline()
    configuration_unselected_deleting = file.readline()
    configuration_unselected_saving = file.readline()
    device_unselected = 'The device for removal is not selected!', 'Прибор для удаления не выбран!'
    device_already_on_list = 'This device is already on the list!', 'Данный прибор уже есть в списке!'
    configuration_unselected = 'Configuration is not selected!', 'Конфигурация не выбрана!'
    parameter = 'Parameter', 'Параметр'
    must_be_an_integer = 'must_be_an_integer', 'должен содеражть целое число'

