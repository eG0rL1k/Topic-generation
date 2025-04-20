import telebot
from telebot import types
import g4f
import logging
import codecs
from difflib import SequenceMatcher

# Константы
rulesForGPTPrompt = 'Эти правила обязательны к выполнению, при генерации ответов на запросы: все ответы должны выдаваться на русском языке (Кроме тех случаев, когда секция проекта подразумевает написание на английском языке. В этом случае дополнительно к названию проекта должна указываться секция) БЕЗ ИСПОЛЬЗОВАНИЯ ССЫЛОК'
createTopics = 'Как можно быстрее придумай 4 темы проекта для конференции (Одним коротким сообщением, не более 10 слов) для конференции. Всегда нумеруй их. Каждая тема с новой строки'
createOtherTopics = 'Придумай и пришли название других четырёх тем для школьного проекта (Одним коротким сообщением, не более 10 слов) для конференции. Всегда нумеруй их. Каждая тема с новой строки'
roadmapPrompt = '''Разработай подробный пошаговый план реализации научного проекта по теме "{topic}". Его длинна не должна быть больше 2000 символов!. 
Формат:
1. Подготовительный этап (2 недели):
- Поиск и анализ литературы
- Формулировка гипотезы
- Составление плана исследований

2. Исследовательский этап (3 недели):
- Проведение экспериментов/исследований
- Сбор данных
- Промежуточный анализ

3. Аналитический этап (1 неделя):
- Обработка полученных данных
- Проверка гипотезы
- Формулировка выводов

4. Этап оформления (1 неделя):
- Подготовка текста работы
- Создание презентации
- Оформление наглядных материалов

5. Презентация (1 неделя):
- Репетиция выступления
- Подготовка к вопросам
- Финальное оформление работы

Для каждого пункта укажи конкретные рекомендуемые действия, адаптированные под выбранную тему проекта.'''

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    filename='bot_debug.log'
)

try:
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
except Exception as e:
    logging.error(f"Ошибка загрузки данных победителей: {str(e)}")
    EOF_list = SIM_list = SFL_list = KP_list = ""


CONFERENCES = {
    'Инженеры будущего': {
        'sections': {
            1: 'Анализ космических снимков и геопространственных данных',
            2: 'Аэрокосмические системы. Беспилотные и пилотируемые летательные аппараты',
            3: 'Большие данные, машинное обучение, прикладная математика',
            4: 'Веб-сайты и веб-приложения',
            5: 'Геотехнология и технологии геологоразведки',
            6: 'Инженерные и ИТ-проекты на английском языке',
            7: 'Инновации умного города',
            8: 'Интеллектуальные помощники и чат-боты',
            9: 'Интеллектуальные робототехнические системы, беспилотные наземные и водные аппараты',
            10: 'Информационная безопасность',
            11: 'Информационные технологии в медицине, биотехнологии, медицинское приборостроение, бионика',
            12: 'Машиностроение, транспорт',
            13: 'Приборостроение, микроэлектроника и схемотехника',
            14: 'Прикладная физика',
            15: 'Прикладная химия, физическая химия',
            16: 'Прикладное программирование. Разработка настольных и мобильных приложений',
            17: 'Современная энергетика',
            18: 'Строительство и архитектура',
            19: 'Технологии виртуальной и дополненной реальности, разработка компьютерных игр и цифровых арт-объектов',
            20: 'Технологии современного производства',
            21: 'Умный дом. Интернет вещей',
            22: 'Цифровые двойники: 3D-моделирование, реверс-инжиниринг'
        },
        'file': 'EOF_list'
    },
    'Старт в медицину': {
        'sections': {
            1: 'Анатомия и физиология человека',
            2: 'Безопасность жизнедеятельности человека',
            3: 'Биотехнология и биоинженерия в медицине',
            4: 'Биофизика',
            5: 'Биохимия',
            6: 'Зоология в медицине',
            7: 'История медицины',
            8: 'Лекарственные растения',
            9: 'Медицинская генетика',
            10: 'Микробиология и эпидемиология',
            11: 'Открытие (на английском языке)',
            12: 'Профилактическая медицина и гигиена',
            13: 'Психология человека и социология',
            14: 'Социологические исследования в сфере охраны здоровья',
            15: 'Стоматология',
            16: 'Фармацевтическая технология',
            17: 'Химия в фармации и медицине',
            18: 'Экология человека'
        },
        'file': 'SIM_list'
    },
    'Курчатовский проект': {
        'sections': {
            1: 'Первые шаги в науку (1-4 класс)',
            2: 'Идея',
            3: 'Метод',
            4: 'Среда',
            5: 'Поиск',
            6: 'Открытие – спикер-сет на иностранных языках',
            7: 'Междисциплинарные занятия',
            8: 'Организация проектной и исследовательской деятельности'
        },
        'file': 'KP_list'
    },
    'Наука для жизни': {
        'sections': {
            'sub_subsections': {
                'Многообразие науки': {
                    1: 'Агротехнологии. Селекция и семеноводство',
                    2: 'Астрономия',
                    3: 'Математика и кибернетика',
                    4: 'Молекулярная биология и биотехнологии',
                    5: 'Науки о Земле',
                    6: 'Неорганическая химия. Нанотехнологии и материаловедение',
                    7: 'Общая химия',
                    8: 'Общественно-научные предметы',
                    9: 'Органическая химия',
                    10: 'Психология и когнитивные науки',
                    11: 'Управление глобальными вызовами',
                    12: 'Филология',
                    13: 'Фундаментальная физика',
                    14: 'Экология и природопользование',
                    15: 'Экология и природопользование (секция на английском языке)',
                    16: 'Экономика',
                },
                'Мегаполис': {
                    1: 'Здоровый образ жизни и спорт в мегаполисе (5-6 класс)',
                    2: 'Проблемы XXI века (7-9 класс)',
                    3: 'Образование в XXI веке (7-9 класс)',
                    4: 'Урбанистика: среда и сообщества (7-9 класс)',
                    5: 'Культурно-исторический образ мегаполиса (7-9 класс)',
                    6: 'Здоровый образ жизни и спорт в мегаполисе (7-9 класс)',
                    7: 'Правовая ответственность и этика в мегаполисе (7-9 класс)',
                    8: 'Проблемы XXI века (10-11 класс)',
                    9: 'Образование в XXI веке (10-11 класс)',
                    10: 'Урбанистика: среда и сообщества (10-11 класс)',
                    11: 'Здоровый образ жизни и спорт в мегаполисе (10-11 класс)',
                    12: 'Культурно-исторический образ мегаполиса (10-11 класс)',
                    13: 'Правовая ответственность и этика в мегаполисе (10-11 класс)',
                    14: 'Urban life: challenges and opportunities / Городская жизнь: вызовы и возможности (10-11 класс)',
                    15: 'Город как учебник: опыт реализации проекта "Новый педагогический класс в московской школе"'
                },
                'Медиастарт': {
                    1: 'Медиажурналистика',
                    2: 'Медиакоммуникации в социальных сетях',
                    3: 'Фотожурналистика',
                    4: 'Радиожурналистика',
                    5: 'Тележурналистика',
                    6: 'Реклама и связи с общественностью',
                    7: 'Кинематограф и аудиовизуальная культура',
                    8: 'Графический дизайн',
                    9: 'Urban Life: Challenges and Opportunities/Город: вызовы и возможности (секция на иностранном языке: английский / французский / немецкий / испанский / китайский)'
                },
                'Шаг в бизнес': {
                    1: 'Предпринимательство в сфере услуг',
                    2: 'Предпринимательство в сфере торговли',
                    3: 'Технологическое предпринимательство',
                    4: 'Цифровое предпринимательство',
                    5: 'Социальное и экологическое предпринимательство',
                    6: 'Бизнес-проекты на английском языке',
                    7: 'Бизнес начинающих предпринимателей (секция для школьников, которые имеют действующий бизнес)'
                }
            }
        },
        'file': 'SFL_list'
    }
}


# Глобальные переменные
user_state = {}
used_topics = {}
topic_similarity_threshold = 0.7
roadmap_requests = {}

bot = telebot.TeleBot('TOKEN')


def log_action(func_name, chat_id, additional_info=""):
    log_msg = f"{func_name} - User {chat_id}"
    if additional_info:
        log_msg += f" | {additional_info}"
    print(log_msg)
    logging.info(log_msg)


def similar(a, b):
    ratio = SequenceMatcher(None, a.lower(), b.lower()).ratio()
    log_action("similar", "system", f"Comparing '{a}' and '{b}': {ratio}")
    return ratio > topic_similarity_threshold


def topics_are_unique(new_topics, previous_topics):
    log_action("topics_are_unique", "system", f"Checking {len(previous_topics)} previous topics")
    for new_topic in new_topics.split('\n'):
        for old_topic in previous_topics:
            if similar(new_topic.strip(), old_topic.strip()):
                log_action("topics_are_unique", "system", f"Found similar: '{new_topic}' and '{old_topic}'")
                return False
    return True


def get_unique_topics(prompt, chat_id, previous_topics, max_attempts=3):
    log_action("get_unique_topics", chat_id, f"Attempts: {max_attempts}, Previous topics count: {len(previous_topics)}")

    for attempt in range(max_attempts):
        log_action("get_unique_topics", chat_id, f"Attempt {attempt + 1}")
        new_topics = get_gpt_response(prompt)
        topics_list = [t.strip() for t in new_topics.split('\n') if t.strip()]

        if not previous_topics or topics_are_unique(new_topics, previous_topics):
            log_action("get_unique_topics", chat_id, "Unique topics generated")
            return new_topics

        prompt += f"\nИзбегай тем, похожих на эти: {', '.join(previous_topics[-3:])}"

    log_action("get_unique_topics", chat_id, "Failed to generate unique topics")
    return "Не удалось сгенерировать уникальные темы. Попробуйте изменить параметры запроса."


def generate_roadmap(topic, chat_id):
    log_action("generate_roadmap", chat_id, f"Generating roadmap for: {topic}")
    prompt = roadmapPrompt.format(topic=topic)
    response = get_gpt_response(prompt)

    # Удаляем возможные предложения о помощи (на случай если GPT их добавит)
    unwanted_phrases = [
        "Если хочешь, могу помочь",
        "Вот стандартный RoadMap",
        "Можешь обратиться за дополнительной помощью",
        "Это базовый план"
    ]

    for phrase in unwanted_phrases:
        response = response.replace(phrase, "")

    roadmap_requests[chat_id] = response
    return response


def get_gpt_response(prompt):
    try:
        log_action("get_gpt_response", "system", f"Sending prompt: {prompt[:100]}...")
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            messages=[{'role': 'user', 'content': prompt}],
        )
        log_action("get_gpt_response", "system", f"Received response: {response[:200]}...")
        return response
    except Exception as e:
        log_action("get_gpt_response", "system", f"Error: {str(e)}")
        return "Ошибка генерации. Пожалуйста, попробуйте позже."


@bot.message_handler(commands=['start'])
def start(message):
    log_action("start", message.chat.id)
    bot.send_message(message.chat.id,
                     'Привет! Я помогу выбрать тему для школьного проекта!',
                     reply_markup=main_menu_keyboard())
    user_state[message.chat.id] = {'step': 'main_menu'}
    bot.register_next_step_handler(message, handle_main_menu)


def main_menu_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('Выбрать направление проекта'))
    markup.row(types.KeyboardButton('У меня есть идея собственного проекта'))
    markup.row(types.KeyboardButton('Справка'), types.KeyboardButton('Создатели проекта'))
    return markup


def directions_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(
        types.KeyboardButton('Инженеры будущего'),
        types.KeyboardButton('Наука для жизни')
    )
    markup.row(
        types.KeyboardButton('Старт в медицину'),
        types.KeyboardButton('Курчатовский проект')
    )
    markup.row(types.KeyboardButton('Назад'))
    return markup


def topics_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('Сгенерировать другие темы'))
    markup.row(types.KeyboardButton('Сгенерировать RoadMap'))
    markup.row(types.KeyboardButton('Вернуться к конференциям'))
    return markup


def finish_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton('Закончить генерацию'))
    return markup


def handle_main_menu(message):
    log_action("handle_main_menu", message.chat.id, f"Choice: {message.text}")

    if message.text == 'Выбрать направление проекта':
        bot.send_message(message.chat.id, 'Выберите конференцию:', reply_markup=directions_keyboard())
        user_state[message.chat.id]['step'] = 'conference_selection'
        bot.register_next_step_handler(message, handle_conference_selection)
    elif message.text == 'У меня есть идея собственного проекта':
        bot.send_message(message.chat.id, 'Напишите в формате: "Конференция - Тема"')
        user_state[message.chat.id]['step'] = 'custom_idea'
        bot.register_next_step_handler(message, handle_custom_idea)
    elif message.text == 'Справка':
        bot.send_message(message.chat.id, 'Этот проект был создан для участия в конференции "Инженеры будущего"')
        bot.register_next_step_handler(message, handle_main_menu)
    elif message.text == 'Создатели проекта':
        bot.send_message(message.chat.id, 'Орлов Егор Александрович \n Лепников Дмитрий Алексеевич \n Ким Виталий Валериянович')
        bot.register_next_step_handler(message, handle_main_menu)
    else:
        bot.send_message(message.chat.id, 'Используйте кнопки меню')
        bot.register_next_step_handler(message, handle_main_menu)


def handle_conference_selection(message):
    log_action("handle_conference_selection", message.chat.id, f"Choice: {message.text}")

    if message.text == 'Назад':
        bot.send_message(message.chat.id, 'Главное меню', reply_markup=main_menu_keyboard())
        user_state[message.chat.id]['step'] = 'main_menu'
        bot.register_next_step_handler(message, handle_main_menu)
        return

    if message.text not in CONFERENCES:
        bot.send_message(message.chat.id, 'Выберите конференцию из списка')
        bot.register_next_step_handler(message, handle_conference_selection)
        return

    user_state[message.chat.id]['conference'] = message.text
    conference = message.text

    if conference == 'Наука для жизни':
        sections = CONFERENCES[conference]['sections']['sub_subsections']
        sections_text = "Выберите категорию:\n" + "\n".join(
            f"{i}. {cat}" for i, cat in enumerate(sections.keys(), 1)
        )
        bot.send_message(message.chat.id, sections_text)
        user_state[message.chat.id]['step'] = 'category_selection'
    else:
        sections = CONFERENCES[conference]['sections']
        sections_text = "Выберите секцию:\n" + "\n".join(
            f"{num}. {name}" for num, name in sections.items()
        )
        bot.send_message(message.chat.id, sections_text)
        user_state[message.chat.id]['step'] = 'section_selection'

    bot.register_next_step_handler(message, handle_section_selection)


def handle_section_selection(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id, {})
    log_action("handle_section_selection", chat_id, f"Processing: {message.text}")

    # Если пользователь нажал на кнопку другой конференции
    if message.text in CONFERENCES:
        user_state[chat_id]['conference'] = message.text
        conference = message.text

        if conference == 'Наука для жизни':
            sections = CONFERENCES[conference]['sections']['sub_subsections']
            sections_text = "Выберите категорию:\n" + "\n".join(
                f"{i}. {cat}" for i, cat in enumerate(sections.keys(), 1)
            )
            bot.send_message(chat_id, sections_text)
            user_state[chat_id]['step'] = 'category_selection'
        else:
            sections = CONFERENCES[conference]['sections']
            sections_text = "Выберите секцию:\n" + "\n".join(
                f"{num}. {name}" for num, name in sections.items()
            )
            bot.send_message(chat_id, sections_text)
            user_state[chat_id]['step'] = 'section_selection'

        bot.register_next_step_handler(message, handle_section_selection)
        return

    # Обработка кнопки "Назад"
    if message.text == 'Назад':
        bot.send_message(chat_id, 'Главное меню', reply_markup=main_menu_keyboard())
        user_state[chat_id]['step'] = 'main_menu'
        bot.register_next_step_handler(message, handle_main_menu)
        return

    try:
        if state['step'] == 'category_selection':
            categories = list(CONFERENCES[state['conference']]['sections']['sub_subsections'].keys())

            # Улучшенная проверка ввода для категории
            if not message.text.isdigit():
                raise ValueError("Введите номер категории цифрой")

            category_num = int(message.text)
            if category_num < 1 or category_num > len(categories):
                raise ValueError("Нет такой категории")

            category = categories[category_num - 1]
            user_state[chat_id]['category'] = category

            subsections = CONFERENCES[state['conference']]['sections']['sub_subsections'][category]
            subsections_text = "Выберите подсекцию:\n" + "\n".join(
                f"{num}. {name}" for num, name in subsections.items()
            )
            bot.send_message(chat_id, subsections_text)
            user_state[chat_id]['step'] = 'subsection_selection'
            bot.register_next_step_handler(message, handle_section_selection)

        elif state['step'] == 'subsection_selection':
            category = state['category']
            subsections = CONFERENCES[state['conference']]['sections']['sub_subsections'][category]

            # Улучшенная проверка ввода для подсекции
            if not message.text.isdigit():
                raise ValueError("Введите номер подсекции цифрой")

            subsection_num = int(message.text)
            if subsection_num not in subsections:
                raise ValueError("Нет такой подсекции")

            subsection = subsections[subsection_num]
            full_section_name = f"{category} - {subsection}"

            bot.send_message(chat_id, f'Генерирую темы для: {full_section_name}...')

            # Улучшенный промпт с учетом подсекции
            prompt = f"{rulesForGPTPrompt} {createTopics} для конференции {state['conference']}, секция: {full_section_name}"

            previous = used_topics.get(chat_id, [])
            topics = get_unique_topics(prompt, chat_id, previous)

            used_topics.setdefault(chat_id, []).append(topics)
            bot.send_message(chat_id, topics, reply_markup=topics_keyboard())

            user_state[chat_id].update({
                'step': 'topics_shown',
                'section': full_section_name,
                'last_topics': topics
            })
            bot.register_next_step_handler(message, handle_topics_menu)

        elif state['step'] == 'section_selection':
            # Существующая логика для других конференций остается без изменений
            section_num = int(message.text)
            section = CONFERENCES[state['conference']]['sections'][section_num]

            bot.send_message(chat_id, 'Генерирую уникальные темы...')
            prompt = f"{rulesForGPTPrompt} {createTopics} для {state['conference']}, {section}"

            previous = used_topics.get(chat_id, [])
            topics = get_unique_topics(prompt, chat_id, previous)

            used_topics.setdefault(chat_id, []).append(topics)
            bot.send_message(chat_id, topics, reply_markup=topics_keyboard())

            user_state[chat_id].update({
                'step': 'topics_shown',
                'section': section,
                'last_topics': topics
            })
            bot.register_next_step_handler(message, handle_topics_menu)

    except ValueError as e:
        error_msg = f"Ошибка: {str(e)}\n\n"
        if state.get('step') == 'category_selection':
            categories = CONFERENCES[state['conference']]['sections']['sub_subsections'].keys()
            error_msg += "Доступные категории:\n" + "\n".join(
                f"{i}. {cat}" for i, cat in enumerate(categories, 1)
            )
        elif state.get('step') == 'subsection_selection':
            subsections = CONFERENCES[state['conference']]['sections']['sub_subsections'][state['category']]
            error_msg += "Доступные подсекции:\n" + "\n".join(
                f"{num}. {name}" for num, name in subsections.items()
            )
        else:
            sections = CONFERENCES[state['conference']]['sections']
            error_msg += "Доступные секции:\n" + "\n".join(
                f"{num}. {name}" for num, name in sections.items()
            )

        log_action("handle_section_selection", chat_id, f"Error: {str(e)}")
        bot.send_message(chat_id, error_msg)
        bot.register_next_step_handler(message, handle_section_selection)
    except (KeyError, IndexError) as e:
        log_action("handle_section_selection", chat_id, f"Error: {str(e)}")
        bot.send_message(chat_id, 'Неверный выбор. Попробуйте еще раз.')
        bot.register_next_step_handler(message, handle_section_selection)


def handle_topics_menu(message):
    chat_id = message.chat.id
    state = user_state.get(chat_id, {})
    log_action("handle_topics_menu", chat_id, f"Action: {message.text}")

    # Обработка завершения работы
    if message.text == 'Закончить генерацию':
        bot.send_message(
            chat_id,
            "Рад, что смог помочь подготовить тему для проекта. Захочешь придумать новую тему, пиши!",
            reply_markup=main_menu_keyboard()
        )
        user_state[chat_id] = {'step': 'main_menu'}
        bot.register_next_step_handler(message, handle_main_menu)  # Важно: регистрируем обработчик главного меню
        return

    # Обработка выбора темы для RoadMap
    if state.get('awaiting_topic_choice'):
        try:
            topic_num = int(message.text)
            topics_list = [t.strip() for t in state['last_topics'].split('\n') if t.strip()]

            if 1 <= topic_num <= len(topics_list):
                selected_topic = topics_list[topic_num - 1].split('. ', 1)[-1]
                log_action("handle_topics_menu", chat_id, f"Selected topic: {selected_topic}")

                bot.send_message(chat_id, f"Генерирую RoadMap для темы: {selected_topic}...")
                roadmap = generate_roadmap(selected_topic, chat_id)
                bot.send_message(chat_id, roadmap, reply_markup=finish_keyboard())

                user_state[chat_id].update({
                    'step': 'roadmap_shown',
                    'awaiting_topic_choice': False,
                    'selected_topic': selected_topic
                })
            else:
                bot.send_message(chat_id, 'Неверный номер темы. Попробуйте еще раз.')
        except ValueError:
            bot.send_message(chat_id, 'Пожалуйста, введите номер темы цифрой.')
        bot.register_next_step_handler(message, handle_topics_menu)
        return

    # Стандартные действия
    if message.text == 'Сгенерировать другие темы':
        if state.get('step') != 'topics_shown':
            bot.send_message(chat_id, 'Сначала выберите секцию')
        else:
            bot.send_message(chat_id, 'Генерирую новые уникальные темы...')
            prompt = f"{rulesForGPTPrompt} {createOtherTopics} для {state['conference']}, {state['section']}"
            previous = used_topics.get(chat_id, [])
            topics = get_unique_topics(prompt, chat_id, previous)
            used_topics.setdefault(chat_id, []).append(topics)
            bot.send_message(chat_id, topics, reply_markup=topics_keyboard())
            user_state[chat_id]['last_topics'] = topics

    elif message.text == 'Сгенерировать RoadMap':
        if 'last_topics' in state:
            topics_list = [t.strip() for t in state['last_topics'].split('\n') if t.strip()]
            topics_text = "Выберите тему для RoadMap:\n"
            bot.send_message(chat_id, topics_text)
            user_state[chat_id]['awaiting_topic_choice'] = True
        elif 'topic' in state:
            bot.send_message(chat_id, f"Генерирую RoadMap для темы: {state['topic']}...")
            roadmap = generate_roadmap(state['topic'], chat_id)
            bot.send_message(chat_id, roadmap, reply_markup=finish_keyboard())
            user_state[chat_id]['step'] = 'roadmap_shown'
        else:
            bot.send_message(chat_id, 'Сначала выберите тему проекта')

    elif message.text == 'Вернуться к конференциям':
        bot.send_message(chat_id, 'Выберите конференцию:', reply_markup=directions_keyboard())
        user_state[chat_id]['step'] = 'conference_selection'
        bot.register_next_step_handler(message, handle_conference_selection)
        return
    else:
        bot.send_message(chat_id, 'Используйте кнопки меню')

    # Регистрируем обработчик для всех случаев, кроме "Закончить генерацию"
    if message.text != 'Закончить генерацию':
        bot.register_next_step_handler(message, handle_topics_menu)


def handle_custom_idea(message):
    chat_id = message.chat.id
    log_action("handle_custom_idea", chat_id, f"Received idea: {message.text}")

    if ' - ' in message.text:
        parts = message.text.split(' - ', 1)
        conference, topic = parts[0], parts[1]

        if conference in CONFERENCES:
            bot.send_message(chat_id, f'Отличная идея!\nКонференция: {conference}\nТема: {topic}')

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row(types.KeyboardButton('Сгенерировать RoadMap'))
            markup.row(types.KeyboardButton('Вернуться к конференциям'))

            bot.send_message(chat_id, 'Выберите действие:', reply_markup=markup)

            user_state[chat_id].update({
                'step': 'custom_idea_shown',
                'conference': conference,
                'section': 'Custom',
                'topic': topic
            })
            bot.register_next_step_handler(message, handle_topics_menu)
        else:
            bot.send_message(chat_id, 'Неизвестная конференция')
            bot.register_next_step_handler(message, handle_custom_idea)
    else:
        bot.send_message(chat_id, 'Используйте формат: "Конференция - Тема"')
        bot.register_next_step_handler(message, handle_custom_idea)


if __name__ == '__main__':
    print("Бот запущен...")
    bot.polling(none_stop=True)