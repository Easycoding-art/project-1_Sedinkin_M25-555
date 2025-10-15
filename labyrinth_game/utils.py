import math

import labyrinth_game.constants as consts
import labyrinth_game.player_actions as pa


def describe_current_room(game_state):
    '''
    Последовательный вывод на экран:
    Название комнаты в верхнем регистре.
    Описание комнаты.
    Список видимых предметов, если они есть.
    Доступные выходы.
    Сообщение о наличии загадки, если она есть.
    '''
    room_name = game_state.get('current_room')
    print(f'== {room_name.upper()} ==')
    room = consts.ROOMS.get(room_name)
    description = room.get('description')
    print(f'{description}')
    items = room.get('items')
    if len(items) != 0:
        print(f"Заметные предметы: {', '.join(items)}")
    exits = room.get('exits')
    print(f"Выходы: {', '.join(exits)}")
    puzzle = room.get('puzzle')
    if puzzle is not None:
        print("Кажется, здесь есть загадка(используйте команду solve).")
    return game_state

def solve_puzzle(game_state):
    '''
    Если загадка есть, выводит на экран вопрос.
    Получает ответ от пользователя.
    '''
    puzzle = consts.ROOMS.get(game_state.get('current_room')).get('puzzle')
    if puzzle is None:
        print("Загадок здесь нет.")
        return game_state
    puzzle_text, answer = puzzle
    print(puzzle_text)
    while True:
        solution = pa.get_input()
        if solution.lower() != answer.lower():
            if game_state.get('current_room') == 'trap_room':
                trigger_trap(game_state)
            else:
                print("Неверно. Попробуйте снова.")
        else:
            print("Сработало!")
            break
    consts.ROOMS[game_state.get('current_room')]['puzzle'] = None
    match game_state.get('current_room'):
        case 'hall':
            game_state['player_inventory'].append('treasure key')
            print(f"Вы получили: {'treasure key'}") 
        case 'library':
            game_state['player_inventory'].append('rusty key')
            print(f"Вы получили: {'rusty key'}")
        case _:
            pass
    return game_state

def attempt_open_treasure(game_state):
    '''
    Открытие сундука с сокровищами для завершения игры
    '''
    items = consts.ROOMS.get(game_state.get('current_room')).get('items')
    inventory = game_state.get('player_inventory')
    if 'treasure chest' not in items:
        print("Сундук уже открыт или отсутствует..")
        return game_state
    if 'treasure key' in inventory or 'rusty key' in inventory:
        print('Вы применяете ключ, и замок щёлкает. Сундук открыт!')
        consts.ROOMS[game_state.get('current_room')]['items'].remove('treasure chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return game_state
    print("Сундук заперт.\nВвести код? (да/нет)")
    answer = pa.get_input()
    match answer:
        case 'да':
            _, answer = consts.ROOMS.get(game_state.get('current_room')).get('puzzle')
            solution = pa.get_input()
            if solution.lower() != answer.lower():
                print("Неверно.")
            else:
                print('Сундук открыт!')
                consts.ROOMS[game_state.get('current_room')]['items'].remove('treasure chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
        case 'нет':
            print("Вы отступаете от сундука.")
    return game_state

def pseudo_random(seed, modulo):
    '''
    Cоздание предсказуемых случайных целых чисел в диапазоне [0, modulo).
    '''
    x = math.sin(seed * 18.9871) * 9548.7813
    result = (x - math.floor(x)) * modulo
    return math.floor(result)

def trigger_trap(game_state):
    '''
    Эта функция имитирует срабатывание ловушки.
    '''
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state.get('player_inventory')
    seed = game_state.get('steps_taken')
    if len(inventory) == 0:
        damage = pseudo_random(seed, 9)
        if damage < 3:
            print('Вы чудом уцелели.')
        else:
            print("Вы погибли!")
            game_state['game_over'] = True
    else:
        item_index = pseudo_random(seed, len(inventory))
        item_name = game_state['player_inventory'].pop(item_index)
        print(f'Вы потеряли {item_name}!')
    return game_state


def random_event(game_state):
    '''
    Создаем случайные события, после перемещения в комнату.
    '''
    seed = game_state.get('steps_taken')
    event_probability = pseudo_random(seed, 10)
    if event_probability == 0:
        return game_state
    event_number = pseudo_random(seed, 2)
    match event_number:
        case 1:
            game_state['player_inventory'].append('coin')
            print("Вы нашли монету.")
        case 2:
            print('Послышался шорох...')
            if 'sword' in game_state.get('player_inventory'):
                print('Таинственное существо испугалось вашего меча.')
        case 3:
            if game_state.get('current_room') == 'trap_room' and 'torch' not in game_state.get('player_inventory'):
                print('Остерегайтесь ловушки!')
                game_state = trigger_trap(game_state)
    return game_state

def show_help(commands=consts.COMMANDS):
    print("\nДоступные команды:")
    for command, description in zip(commands.keys(), commands.values()):
        print(f"  {command}  - {description}")