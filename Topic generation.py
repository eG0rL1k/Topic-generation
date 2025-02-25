import telebot
from telebot import types
import g4f
import codecs
# Дефолтные промпты для запросов к gpt (просто чтоб меньше места занимало в самом коде)
rulesForGPTPrompt = 'Эти правила обязательны к выполнению, при генерации ответов на запросы: все ответы должны выдаваться на  русском языке (Кроме тех случаев, когда секция проекта подрозумевает написание на английском языке. В этом случае дополнительно к названию проекта должна указываться секция) БЕЗ ИСПОЛЬЗОВАНИЯ ССЫЛОК'
createTopics = 'Как можно быстрее придумай 4 темы проекта для конференции (Одним коротким сообщением, не более 10 слов) для конференции'
createOtherTopics = 'Придумай и пришли название других четырёх тем для школьного проекта (Одним коротким сообщением, не более 10 слов) для конференции'
EOF = 'Инженеры будущего'
SIM = 'Старт в медицину'
SFL = 'Наука для жизни'
KP = 'Курчатовский проект - от знаний к практике, от практики к результату'
# Направленности для конференции "Инженеры будущего"
directivityForEOF = '1)	Прикладная физика; \n'+\
'2) Машиностроение, транспорт; \n'+\
'3) Интеллектуальные робототехнические системы, беспилотные наземные и водные аппараты; \n'+\
'4) Приборостроение, микроэлектроника и схемотехника; \n'+\
'5) Прикладная химия, физическая химия; \n'+\
'6) Строительство, дизайн и архитектура; \n'+\
'7) 3D-моделирование, 3D-печать и VR/AR-технологии; \n'+\
'8) Программирование. Разработка программ, приложений, веб-сайтов; \n'+\
'9) Информационные технологии в медицине, биотехнологии, медицинское приборостроение, бионика; \n'+\
'10) Энергия будущего. Цифровая энергетика; \n'+\
'11) Инновации умного города. Умная школа; \n'+\
'12) Инновации умного города. Умная школа (секция на английском языке); \n'+\
'13) Аэрокосмические системы. Беспилотные и пилотируемые летательные аппараты; \n'+\
'14) Информационная безопасность; \n'+\
'15) Большие данные, прикладная математика; \n'+\
'16) Технологии связи.'
# Направленности для конференции "Старт в медицину"
directivityForSIM = '1) Анатомия и физиология человека; \n'+\
'2) Безопасность жизнедеятельности человека; \n'+\
'3) Биотехнология и биоинженерия в медицине; \n'+\
'4) Биофизика; \n'+\
'5) Биохимия; \n'+\
'6) Зоология в медицине; \n'+\
'7) История медицины; \n'+\
'8) Лекарственные растения; \n'+\
'9) Медицинская генетика; \n'+\
'10) Микробиология и эпидемиология; \n'+\
'11) Открытие (на английском языке); \n'+\
'12) Профилактическая медицина и гигиена; \n'+\
'13) Психология человека и социология; \n'+\
'14) Фармацевтическая технология; \n'+\
'15) Химия в фармации и медицине; \n'+\
'16) Экология человека'
# Направленности для конференции "Курчатовский проект — от знаний к практике, от практики к результату"
directivityForKP = '1) Первые шаги в науку (1-4 класс); \n '+\
'2) Идея; \n'+\
'3) Метод; \n'+\
'4) Среда; \n'+\
'5) Поиск; \n'+\
'6) Открытие – спикер-сет на иностранных языках'
# Направленности для конференции "Наука для жизни"
directivityForSFL_list_a = ['Агротехнологии. Селекция и семеноводство', 'Астрономия и космические технологии', 'Биотехнологии. Молекулярная биология. Генетика', 'Информационные технологии. Программирование. Кибернетика', 'Математика и механика', 'Машиностроение и транспорт. Робототехника', 'Неорганическая химия. Нанотехнологии и материаловедение', 'Науки о Земле', 'Общественно-научные предметы', 'Оптика. Лазерные технологии', 'Органическая химия', 'Прикладная химия', 'Психология и когнитивные науки', 'Управление глобальными вызовами', 'Филология', 'Экология и природопользование', 'Экология и природопользование (секция на английском языке)', 'Экономика', 'Электроника и приборостроение', 'Энергетика']
directivityForSFL_list_b = ['Здоровый образ жизни и спорт в мегаполисе (5-6 класс)', 'Проблемы XXI века (7-9 класс)', 'Образование в XXI веке (7-9 класс)', 'Урбанистика: среда и сообщества (7-9 класс)', 'Культурно-исторический образ мегаполиса (7-9 класс)', 'Здоровый образ жизни и спорт в мегаполисе (7-9 класс)', 'Правовая ответственность и этика в мегаполисе (7-9 класс)', 'Проблемы XXI века (10-11 класс)', 'Образование в XXI веке (10-11 класс)', 'Урбанистика: среда и сообщества (10-11 класс)', 'Здоровый образ жизни и спорт в мегаполисе (10-11 класс)', 'Культурно-исторический образ мегаполиса (10-11 класс)', 'Urban Life: Challenges and Opportunities / Городская жизнь: вызовы и возможности (10-11 класс)', 'Город как учебник: опыт реализации проекта «Новый педагогический класс в московской школе']
directivityForSFL_list_c = ['Медиажурналистика', 'Медиакоммуникации в социальных сетях', 'Фотожурналистика', 'Радиожурналистика', 'Тележурналистика', 'Реклама и связи с общественностью', 'Кинематограф и аудиовизуальная культура', 'Медиа-арт', 'Urban Life: Challenges and Opportunities/Город: вызовы и возможности (секция на иностранном языке (английский/французский/немецкий/испанский/китайский)']
directivityForSFL_list_d = ['Посредническое предпринимательство', 'Социальное и экологическое предпринимательство', 'Технологическое предпринимательство', 'Предпринимательство в сфере услуг', 'Цифровое предпринимательство', 'Бизнес-проекты (секция на английском языке)']
directivityForSFL = 'a. Многообразие науки\n\n'+\
'1) Агротехнологии. Селекция и семеноводство; \n'+\
'2) Астрономия и космические технологии; \n'+\
'3) Биотехнологии. Молекулярная биология. Генетика; \n'+\
'4) Информационные технологии. Программирование. Кибернетика; \n'+\
'5) Математика и механика; \n'+\
'6) Машиностроение и транспорт. Робототехника; \n'+\
'7) Неорганическая химия. Нанотехнологии и материаловедение; \n'+\
'8) Науки о Земле; \n'+\
'9) Общественно-научные предметы; \n'+\
'10) Оптика. Лазерные технологии; \n'+\
'11) Органическая химия; \n'+\
'12) Прикладная химия; \n'+\
'13) Психология и когнитивные науки; \n'+\
'14) Управление глобальными вызовами; \n'+\
'15) Филология; \n'+\
'16) Экология и природопользование; \n'+\
'17) Экология и природопользование (секция на английском языке); \n'+\
'18) Экономика; \n'+\
'19) Электроника и приборостроение; \n'+\
'20) Энергетика. \n\n'+\
'b.	Мегаполис как пространство успеха и социальной ответственности\n\n'+\
'1) Здоровый образ жизни и спорт в мегаполисе (5-6 класс); \n'+\
'2) Проблемы XXI века (7-9 класс); \n'+\
'3) Образование в XXI веке (7-9 класс); \n'+\
'4) Урбанистика: среда и сообщества (7-9 класс); \n'+\
'5) Культурно-исторический образ мегаполиса (7-9 класс); \n'+\
'6) Здоровый образ жизни и спорт в мегаполисе (7-9 класс); \n'+\
'7) Правовая ответственность и этика в мегаполисе (7-9 класс); \n'+\
'8) Проблемы XXI века (10-11 класс); \n'+\
'9) Образование в XXI веке (10-11 класс); \n'+\
'10) Урбанистика: среда и сообщества (10-11 класс); \n'+\
'11) Здоровый образ жизни и спорт в мегаполисе (10-11 класс); \n'+\
'12) Культурно-исторический образ мегаполиса (10-11 класс); \n'+\
'13) Правовая ответственность и этика в мегаполисе (10-11 класс); \n'+\
'14) Urban Life: Challenges and Opportunities / Городская жизнь: вызовы и возможности (10-11 класс); \n'+\
'15) Город как учебник: опыт реализации проекта «Новый педагогический класс в московской школе; \n\n'+\
'c.	Медиастарт\n\n'+\
'1)	Медиажурналистика; \n'+\
'2)	Медиакоммуникации в социальных сетях; \n'+\
'3)	Фотожурналистика; \n'+\
'4)	Радиожурналистика; \n'+\
'5)	Тележурналистика; \n'+\
'6)	Реклама и связи с общественностью; \n'+\
'7)	Кинематограф и аудиовизуальная культура; \n'+\
'8)	Медиа-арт; \n'+\
'9)	Urban Life: Challenges and Opportunities/Город: вызовы и возможности (секция на иностранном языке (английский/французский/немецкий/испанский/китайский).\n\n'+\
'd.	Шаг в бизнес\n\n'+\
'1)	Посредническое предпринимательство; \n'+\
'2)	Социальное и экологическое предпринимательство; \n'+\
'3)	Технологическое предпринимательство; \n'+\
'4)	Предпринимательство в сфере услуг; \n'+\
'5)	Цифровое предпринимательство; \n'+\
'6)	Бизнес-проекты (секция на английском языке);'

used_topics = []
bot = telebot.TeleBot('7496221021:AAEe3')#Сюда API
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt_1 = types.KeyboardButton('Справка')
    bt_2 = types.KeyboardButton('Выбрать направление проекта')
    bt_3 = types.KeyboardButton('Создатели проекта')
    bt_4 = types.KeyboardButton('У меня есть идея собственного проекта')
    markup.row(bt_2)
    markup.row(bt_4)
    markup.row(bt_1, bt_3)
    bot.send_message(message.chat.id, f'Привет!\n Я - бот, который поможет тебе определиться с темой для школьного проекта!', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)

def back_to_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt_1 = types.KeyboardButton('Справка')
    bt_2 = types.KeyboardButton('Выбрать направление проекта')
    bt_3 = types.KeyboardButton('Создатели проекта')
    bt_4 = types.KeyboardButton('У меня есть идея собственного проекта')
    markup.row(bt_2)
    markup.row(bt_4)
    markup.row(bt_1, bt_3)
    bot.send_message(message.chat.id, 'Давай вернёмся', reply_markup=markup)

def directions(message):
    bot.send_message(message.chat.id, 'Вот 4 направления на выбор')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt_1 = types.KeyboardButton('Инженеры будущего')
    bt_2 = types.KeyboardButton('Наука для жизни')
    bt_3 = types.KeyboardButton('Старт в медицину')
    bt_4 = types.KeyboardButton('Курчатовский проект - от знаний к практике, от практики к результату')
    bt_5 = types.KeyboardButton('Назад')
    markup.row(bt_1, bt_2)
    markup.row(bt_3, bt_4)
    markup.row(bt_5)
    bot.send_message(message.chat.id, 'Выбирай то, которое тебе больше нравится', reply_markup=markup)

def back_to_directions(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt_1 = types.KeyboardButton('Инженеры будущего')
    bt_2 = types.KeyboardButton('Наука для жизни')
    bt_3 = types.KeyboardButton('Старт в медицину')
    bt_4 = types.KeyboardButton('Курчатовский проект - от знаний к практике, от практики к результату')
    bt_5 = types.KeyboardButton('Назад')
    markup.row(bt_1, bt_2)
    markup.row(bt_3, bt_4)
    markup.row(bt_5)
    bot.send_message(message.chat.id, 'Выбирай то, которое тебе больше нравится', reply_markup=markup)

def topics(message):
    bot.send_message(message.chat.id, 'Вот 4 темы на выбор')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    bt_1 = types.KeyboardButton('Тема №1')
    bt_2 = types.KeyboardButton('Тема №2')
    bt_3 = types.KeyboardButton('Тема №3')
    bt_4 = types.KeyboardButton('Тема №4')
    bt_5 = types.KeyboardButton('Другие темы')
    bt_6 = types.KeyboardButton('Назад к направлениям')
    markup.row(bt_1, bt_2)
    markup.row(bt_3, bt_4)
    markup.row(bt_5)
    markup.row(bt_6)
    bot.send_message(message.chat.id, 'Выбирай ту, которая тебе больше нравится', reply_markup=markup)



def get_chatgpt_response(prompt):
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{'role': 'user', 'content': prompt}],
    )
    return response


def split_vars(s):
    s = s.replace('1. ', '')
    s = s.replace('2. ', '')
    s = s.replace('3. ', '')
    s = s.replace('4. ', '')
    s = s.split(' \n')
    return s

def check_match(user_input):
    try:
        if len(user_input) > 5:
            splited_user_input = user_input.split(' - ')
            splited_user_input = splited_user_input[0]+splited_user_input[1][-4:]
            pattern = 'НаправлениеТема'
            if splited_user_input == pattern:
                return True
            else:
                return False
    except IndexError:
        pass

fileObj = codecs.open("Engineers of the future.txt", "r", "utf_8_sig")
EOF_list = fileObj.read()
fileObj.close()

fileObj = codecs.open("Start in medicine.txt", "r", "utf_8_sig")
SIM_list = fileObj.read()
fileObj.close()

fileObj = codecs.open("Science for Life.txt", "r", "utf_8_sig")
SFL_list = fileObj.read()
fileObj.close()

fileObj = codecs.open("The Kurchatov Project.txt", "r", "utf_8_sig")
KP_list = fileObj.read()
fileObj.close()

def on_click(message):
    global sv
    global used_topics # Для других направлений
    global chosenDirecton # Для других направлений
    global chosen_section
    global chosen_undersection
    global chosen_underundersection
    global text
    if message.text == 'Справка':
        bot.send_message(message.chat.id, 'Этот проект был создан для участия в конференции "Инженеры будущего"')
    elif message.text == 'Выбрать направление проекта':
        directions(message)
    elif message.text == 'Создатели проекта':
        bot.send_message(message.chat.id, f'Орлов Егор Александровчи\n Лепников Дмитрий Алексеевич\n Ким Виталий Валерьянович')
    elif message.text == 'У меня есть идея собственного проекта':
        bot.send_message(message.chat.id, 'Это просто замечательно! Тогда я помогу тебе соствить план для него!\n\n Напиши какое у твоего проекта направление и тема вот так:\n Направление - {направление твоего проекта}. Тема - {тема твоего проекта}')
    # =========================================================================================================== #
    elif message.text == 'Назад':
        back_to_start(message)
    elif message.text == 'Инженеры будущего':
        bot.send_message(message.chat.id, 'Хорошо, а какая именно секция тебя интересует?')
        bot.send_message(message.chat.id, f'{directivityForEOF}')
        bot.send_message(message.chat.id, 'Напиши её номер в чат.')
        chosenDirecton = EOF
    elif message.text == 'Наука для жизни':
        bot.send_message(message.chat.id, 'Хорошо, а какая именно секция тебя интересует?')
        bot.send_message(message.chat.id, f'{directivityForSFL}')
        bot.send_message(message.chat.id, 'Напиши её номер в чат в формате Категория (буква) и Номер (число) через пробел')
        chosenDirecton = SFL
    elif message.text == 'Старт в медицину':
        bot.send_message(message.chat.id, 'Хорошо, а какая именно секция тебя интересует?')
        bot.send_message(message.chat.id, f'{directivityForSIM}')
        bot.send_message(message.chat.id, 'Напиши её номер в чат в формате просто число')
        chosenDirecton = SIM
    elif message.text == 'Курчатовский проект - от знаний к практике, от практики к результату':
        bot.send_message(message.chat.id, 'Хорошо, а какая именно секция тебя интересует?')
        bot.send_message(message.chat.id, f'{directivityForKP}')
        bot.send_message(message.chat.id, 'Напиши её номер в чат в формате или просто число')
        chosenDirecton = KP
    # =========================================================================================================== #
    elif message.text == 'Другие темы':
        if chosenDirecton == EOF:
            text = EOF_list
            chosen_underundersection = 'В данном файле нет Подподсекции'
        if chosenDirecton == SIM:
            text = SIM_list
            chosen_underundersection = 'В данном файле нет Подподсекции'
        if chosenDirecton == SFL:
            text = SFL_list
        if chosenDirecton == KP:
            text = KP_list
            chosen_underundersection = 'В данном файле нет Подподсекции'
        bot.send_message(message.chat.id, 'Придумываю темы для проекта 🤓 Это может занять некоторое время.')
        TopicsVars = get_chatgpt_response(f'{createOtherTopics} {chosenDirecton}, ОСНОВЫВАЯСЬ (НЕ бери уже использовавшиеся темы) на Информационном секторе подсекции {chosen_section} из {text}  (Если {chosenDirecton} - SFL, то в качестве Подподсекции используй {chosen_underundersection}, Подсекция - {chosen_section}). В массиве {used_topics} находятся списки, в каждом из которых по 4 уже использовавшихся темы, поэтому новые темы не должны совпадать ни с одной из тех, которые находятся в списках массива {used_topics}. {rulesForGPTPrompt}')
        bot.send_message(message.chat.id, TopicsVars)
        sv = (split_vars(TopicsVars))
        used_topics.append(sv)
    elif message.text == 'Назад к направлениям':
        used_topics = []
        sv = []
        back_to_directions(message)
    elif message.text == 'Тема №1':
        bot.send_message(message.chat.id, 'Сейчас я создам план для твоего проекта. Это может занять некоторое время.')
        bot.send_message(message.chat.id, get_chatgpt_response(f'Cоздай план проекта по теме {sv[0]}. Соблюдай следующие правила: {rulesForGPTPrompt}'))
    elif message.text == 'Тема №2':
        bot.send_message(message.chat.id, 'Сейчас я создам план для твоего проекта. Это может занять некоторое время.')
        bot.send_message(message.chat.id, get_chatgpt_response(f'Cоздай план проекта по теме {sv[1]}. Соблюдай следующие правила: {rulesForGPTPrompt}'))
    elif message.text == 'Тема №3':
        bot.send_message(message.chat.id, 'Сейчас я создам план для твоего проекта. Это может занять некоторое время.')
        bot.send_message(message.chat.id, get_chatgpt_response(f'Cоздай план проекта по теме {sv[2]}. Соблюдай следующие правила: {rulesForGPTPrompt}'))
    elif message.text == 'Тема №4':
        bot.send_message(message.chat.id, 'Сейчас я создам план для твоего проекта. Это может занять некоторое время.')
        bot.send_message(message.chat.id, get_chatgpt_response(f'Cоздай план проекта по теме {sv[3]}. Соблюдай следующие правила: {rulesForGPTPrompt}'))
    # ========================================================================================================================================== #
    elif check_match(message.text) == True:
        bot.send_message(message.chat.id, 'Сейчас я создам план для твоего проекта. Это может занять некоторое время.')
        bot.send_message(message.chat.id, get_chatgpt_response(f'Создай план проекта, который написан в {message.text}. Соблюдай следующие правила: {rulesForGPTPrompt}'))
    elif check_match(message.text) == False:
        bot.send_message(message.chat.id,'Не обнаружено совпадение с примером заполнения')
    # ========================================================================================================================================== #
    elif (message.text in list(str(x) for x in range(1, 20)) or (message.text[0] in ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D'])):
        if chosenDirecton == EOF:
            bot.send_message(message.chat.id, 'Придумываю темы для проекта 🤓 Это может занять некоторое время.')
            chosen_section = get_chatgpt_response(f'Напиши только название секции под №{message.text} из {directivityForEOF}')
            TopicsVars = get_chatgpt_response(f'{rulesForGPTPrompt}, {createTopics} "{EOF}", ОСНОВЫВАЯСЬ (НЕ бери уже использовавшиеся темы) на Информационном секторе подсекции "{chosen_section}" из {EOF_list}')
            sv = (split_vars(TopicsVars))
            used_topics.append(sv)
            bot.send_message(message.chat.id, TopicsVars, topics(message))
        if chosenDirecton == SFL:
            bot.send_message(message.chat.id, 'Придумываю темы для проекта 🤓 Это может занять некоторое время.')
            chosen_section = get_chatgpt_response(f'Напиши только название секции под буквой {message.text[0]} из {directivityForSFL}')
            if message.text[0] == 'a' or message.text[0] == 'A':
                chosen_undersection = directivityForSFL_list_a
                chosen_underundersection = chosen_undersection[int(message.text[2:])-1]
            if message.text[0] == 'b' or message.text[0] == 'B':
                chosen_undersection = directivityForSFL_list_b
                chosen_underundersection = chosen_undersection[int(message.text[2:])-1]
            if message.text[0] == 'c' or message.text[0] == 'C':
                chosen_undersection = directivityForSFL_list_c
                chosen_underundersection = chosen_undersection[int(message.text[2:])-1]
            if message.text[0] == 'd' or message.text[0] == 'D':
                chosen_undersection = directivityForSFL_list_d
                chosen_underundersection =chosen_undersection[int(message.text[2:])-1]
            TopicsVars = get_chatgpt_response(f'{rulesForGPTPrompt}, {createTopics} "{SFL}", ОСНОВЫВАЯСЬ (НЕ бери уже использовавшиеся темы) на Информационном секторе Подподсекции {chosen_underundersection} Подсекции {chosen_undersection} из {SFL_list}')
            sv = (split_vars(TopicsVars))
            used_topics.append(sv)
            bot.send_message(message.chat.id, TopicsVars, topics(message))
        if chosenDirecton == KP:
            bot.send_message(message.chat.id, 'Придумываю темы для проекта 🤓 Это может занять некоторое время.')
            chosen_section = get_chatgpt_response(f'Напиши только название секции под №{message.text} из {directivityForKP}')
            TopicsVars = get_chatgpt_response(f'{rulesForGPTPrompt}, {createTopics} "{KP}", ОСНОВЫВАЯСЬ (НЕ бери уже использовавшиеся темы) на Информационном секторе подсекции "{chosen_section}" из {KP_list}')
            sv = (split_vars(TopicsVars))
            used_topics.append(sv)
            bot.send_message(message.chat.id, TopicsVars, topics(message))
        if chosenDirecton == SIM:
            bot.send_message(message.chat.id, 'Придумываю темы для проекта 🤓 Это может занять некоторое время.')
            chosen_section = get_chatgpt_response(f'Напиши ТОЛЬКО название секции {message.text}, где буква - категория цифра - номер секции в этой категории, из {directivityForSIM} без указания категории и секции. (Пример: в категории a под номером 8 идёт секция "Науки о Земле")')
            TopicsVars = get_chatgpt_response(f'{rulesForGPTPrompt}, {createTopics} "{SIM}", ОСНОВЫВАЯСЬ (НЕ бери уже использовавшиеся темы) на Информационном секторе подсекции "{chosen_section}" из {SIM_list}')
            sv = (split_vars(TopicsVars))
            used_topics.append(sv)
            bot.send_message(message.chat.id, TopicsVars, topics(message))
    bot.register_next_step_handler(message, on_click)

#Чтобы бот не прекращал работать и с ним можно было взаимодействовать bot.polling(none_stop=True) или bot.infinity_polling()
bot.polling(none_stop=True)
