#!/usr/bin/env python3

from labyrinth_game.player_actions import *
from labyrinth_game.utils import *

game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
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
            return describe_current_room(game_state)
        case 'use':
            if parsed_command[1] == 'treasure_chest' and game_state.get('current_room') == 'treasure_room':
                return attempt_open_treasure(game_state)
            else:
                return use_item(game_state, parsed_command[1])
        case 'north' | 'south' | 'east' | 'west':
            return move_player(game_state, parsed_command[0])
        case 'take':
            return take_item(game_state, parsed_command[1])
        case 'inventory':
            return show_inventory(game_state)
        case 'solve':
            if game_state.get('current_room') == 'treasure_room':
                return attempt_open_treasure(game_state)
            else:
                return solve_puzzle(game_state)
        case 'quit' | 'exit':
            game_state['game_over'] = True
            return game_state
        case 'help':
            show_help()
            return game_state
        case _:
            show_help()
            return game_state

def main():
    '''
    Главная функция.
    '''
    global game_state
    print("Добро пожаловать в Лабиринт сокровищ!")
    game_state = describe_current_room(game_state)
    while not game_state.get('game_over'):
        command = get_input()
        game_state = process_command(game_state, command)


if __name__ == '__main__':
    main()