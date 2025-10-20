import labyrinth_game.constants as consts
import labyrinth_game.utils as utils


def show_inventory(game_state):
    '''
    Прочитать и вывести содержимое инвентаря.
    '''
    inventory_list = game_state['player_inventory']
    match len(inventory_list):
        case 0:
            print('Инвентарь пуст!')
        case _:
            inventory_sting = ', '.join(inventory_list)
            print(f'У вас в инвентаре:\n{inventory_sting}')
    return game_state

def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"
    
def move_player(game_state, direction):
    '''
    Для продвижения по лабиринту.
    Проверяет, существует ли выход в этом направлении.
    Если вход в сокровищницу - применяет ключ
    '''
    exits = consts.ROOMS.get(game_state.get('current_room')).get('exits')
    if direction in exits.keys():
        next_room = exits.get(direction)
        if next_room == 'treasure_room' and game_state.get('treasure_room_status'):
            if 'rusty_key' in game_state['player_inventory']:
                game_state['player_inventory'].remove('rusty_key')
                game_state['treasure_room_status'] = True
                print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.")
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return game_state
        game_state['current_room'] = next_room
        game_state['steps_taken'] +=1
        game_state = utils.describe_current_room(game_state)
        game_state = utils.random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")
    return game_state


def take_item(game_state, item_name):
    '''
    Проверяет, есть ли предмет в комнате.
    Если предмет есть:
    Добавляет его в инвентарь игрока.
    Удаляет его из списка предметов комнаты.
    '''
    items = consts.ROOMS.get(game_state.get('current_room')).get('items')
    if item_name in items:
        consts.ROOMS[game_state.get('current_room')]['items'].remove(item_name)
        game_state['player_inventory'].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")
    return game_state

def use_item(game_state, item_name):
    '''
    Использование предметов
    '''
    if item_name not in game_state['player_inventory']:
        print('У вас нет такого предмета.')
    else:
        match item_name:
            case 'torch':
                print('Cтало гораздо светлее.')
            case 'sword':
                print('Ты чувствуешь себя намного увереннее')
            case 'bronze_box':
                print('Шкатулка открыта!')
                if item_name not in game_state['player_inventory']:
                    game_state['player_inventory'].append('rusty_key')
                    print('Ты нашел ключ.')
                game_state['player_inventory'].remove('bronze_box')
            case _:
                print('Я не знаю, что с этим делать...')
    return game_state

