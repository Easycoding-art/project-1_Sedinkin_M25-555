#!/usr/bin/env python3

import labyrinth_game.player_actions as pa
import labyrinth_game.utils as utils

game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'treasure_room_status': False, # Значения отокрытости сокровищницы
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}

def process_command(game_state, command):
    '''
    Обработка команд.
    '''
    parsed_command = command.split()
    match parsed_command[0]:
        case 'look':
            return utils.describe_current_room(game_state)
        case 'use':
            if parsed_command[1] == 'treasure_chest' and game_state.get('current_room') == 'treasure_room':
                return utils.attempt_open_treasure(game_state)
            else:
                return pa.use_item(game_state, parsed_command[1])
        case 'north' | 'south' | 'east' | 'west':
            return pa.move_player(game_state, parsed_command[0])
        case 'take':
            return pa.take_item(game_state, parsed_command[1])
        case 'inventory':
            return pa.show_inventory(game_state)
        case 'solve':
            if game_state.get('current_room') == 'treasure_room':
                return utils.attempt_open_treasure(game_state)
            else:
                return utils.solve_puzzle(game_state)
        case 'quit' | 'exit':
            game_state['game_over'] = True
            return game_state
        case 'help':
            utils.show_help()
            return game_state
        case _:
            utils.show_help()
            return game_state

def main():
    '''
    Главная функция.
    '''
    global game_state
    print("Добро пожаловать в Лабиринт сокровищ!")
    game_state = utils.describe_current_room(game_state)
    while not game_state.get('game_over'):
        command = pa.get_input()
        game_state = process_command(game_state, command)


if __name__ == '__main__':
    main()