import xml.etree.ElementTree as ET
import graphviz
from Linkedlist import LinkedList
import copy


def display_pattern(pattern):
    for row in pattern:
        print(''.join(row).replace('B', '⬜').replace('N', '⬛'))

def generar_dot(pattern, output_dot_file):
    dot = graphviz.Digraph()

    dot.node_attr.update(shape='box', style='filled', fillcolor='#E6E6E6')  
    dot.edge_attr.update(style='invis')
    dot.body.append('label="Piso"')

    for i, row in enumerate(pattern):
        for j, cell in enumerate(row):
            color = '#E6E6E6' if cell == 'B' else 'black' 
            dot.node(f'node_{i}_{j}', label=' ', style='filled', fillcolor=color, width='1.5', height='1.5')
            if j > 0:
                dot.edge(f'node_{i}_{j-1}', f'node_{i}_{j}', style='invis')
            if i > 0:
                dot.edge(f'node_{i-1}_{j}', f'node_{i}_{j}', style='invis')

    dot.render(output_dot_file, view=True)

def convert_pattern(floor_name, initial_code, target_code, floors):
    current_floor = floors.search_floor(floor_name)
    if current_floor is None:
        print('Piso no encontrado.')
        return

    initial_pattern, initial_pattern_str = floors.search_pattern(floor_name, initial_code)
    target_pattern, target_pattern_str = floors.search_pattern(floor_name, target_code)

    if initial_pattern is None or target_pattern is None:
        print('Código de patrón no encontrado.')
        return

    print(f'\nPatrón inicial:')
    display_pattern(initial_pattern_str)
    generar_dot(initial_pattern_str, f'patron_inicial_{floor_name}_{initial_code}')

    print(f'\nPatrón final:')
    display_pattern(target_pattern_str)
    generar_dot(target_pattern_str, f'patron_final_{floor_name}_{target_code}')

    min_cost, steps = calculate_min_cost(current_floor.F, current_floor.S, initial_pattern_str, target_pattern_str)

    print(f'\nCosto mínimo para cambiar de patrón inicial a patrón final: {min_cost} Quetzales')
    print('Paso a paso:')
    step = 0
    for step, pattern in enumerate(steps, 1):
        print(f'\nPaso {step - 1}:')
        print(f'Operación: {pattern[1]}')
        print(f'Patrón:')
        display_pattern(pattern[0])
    print(f'\nPaso {step}:')
    print(f'Patrón:')
    print(f'Operación: Final')
    display_pattern(target_pattern_str)
    

def calculate_min_cost(F, S, initial_pattern, target_pattern):

    def makeFlip(pattern):
        for i in range(len(pattern)):
            for j in range(len(pattern[i])):
                if (pattern[i][j] != target_pattern[i][j]):
                    pattern_tmp = copy.deepcopy(pattern)
                    pattern[i][j] = target_pattern[i][j]
                    return pattern, pattern_tmp
        return pattern, pattern
    
    def makeSwap(pattern, e):
        for i in range(len(pattern)):
            for j in range(len(pattern[i])):
                if (pattern[i][j] != target_pattern[i][j]):
                    if e == 0 and i > 0 and pattern[i - 1][j] == target_pattern[i][j]:
                        pattern_tmp = copy.deepcopy(pattern)
                        pattern[i][j] = pattern[i - 1][j]
                        pattern[i - 1][j] = pattern_tmp[i][j]
                        return pattern, pattern_tmp
                    if e == 1 and i < len(pattern) - 1 and pattern[i + 1][j] == target_pattern[i][j]:
                        pattern_tmp = copy.deepcopy(pattern)
                        pattern[i][j] = pattern[i + 1][j]
                        pattern[i + 1][j] = pattern_tmp[i][j]
                        return pattern, pattern_tmp
                    if e == 2 and j > 0 and pattern[i][j - 1] == target_pattern[i][j]:
                        pattern_tmp = copy.deepcopy(pattern)
                        pattern[i][j] = pattern[i][j - 1]
                        pattern[i][j - 1] = pattern_tmp[i][j]
                        return pattern, pattern_tmp
                    if e == 3 and j < len(pattern[i]) - 1 and pattern[i][j + 1] == target_pattern[i][j]:
                        pattern_tmp = copy.deepcopy(pattern)
                        pattern[i][j] = pattern[i][j + 1]
                        pattern[i][j + 1] = pattern_tmp[i][j]
                        return pattern, pattern_tmp
        return pattern, pattern

    def dfs(current_pattern, current_cost, path, deep):
        nonlocal min_cost, min_path, target_pattern
        if current_pattern == target_pattern:
            if current_cost < min_cost:
                min_cost = current_cost
                min_path = path
        elif current_cost < min_cost:
            pattern_new, pattern = makeFlip(copy.deepcopy(current_pattern))
            if pattern_new != pattern:
                new_cost = current_cost + F
                path_tmp = copy.deepcopy(path)
                path_tmp.append([pattern, 'Flip'])
                if deep < 10: dfs(pattern_new, new_cost, path_tmp, deep + 1)
            pattern_new, pattern = makeSwap(copy.deepcopy(current_pattern), 0)
            if pattern_new != pattern:
                new_cost = current_cost + S
                path_tmp = copy.deepcopy(path)
                path_tmp.append([pattern, 'Swipe'])
                if deep < 7: dfs(pattern_new, new_cost, path_tmp, deep + 1)
            pattern_new, pattern = makeSwap(copy.deepcopy(current_pattern), 1)
            if pattern_new != pattern:
                new_cost = current_cost + S
                path_tmp = copy.deepcopy(path)
                path_tmp.append([pattern, 'Swipe'])
                if deep < 7: dfs(pattern_new, new_cost, path_tmp, deep + 1)
            pattern_new, pattern = makeSwap(copy.deepcopy(current_pattern), 2)
            if pattern_new != pattern:
                new_cost = current_cost + S
                path_tmp = copy.deepcopy(path)
                path_tmp.append([pattern, 'Swipe'])
                if deep < 7: dfs(pattern_new, new_cost, path_tmp, deep + 1)
            pattern_new, pattern = makeSwap(copy.deepcopy(current_pattern), 3)
            if pattern_new != pattern:
                new_cost = current_cost + S
                path_tmp = copy.deepcopy(path)
                path_tmp.append([pattern, 'Swipe'])
                if deep < 7: dfs(pattern_new, new_cost, path_tmp, deep + 1)

    min_cost = float('inf')
    min_path = []

    dfs(initial_pattern, 0, [[copy.deepcopy(initial_pattern), "Original"]], 0)

    return min_cost, min_path


def sort_linked_list(linked_list, key=lambda x: x):

    sorted_head = None
    current = linked_list.head

    while current:
        next_node = current.next
        sorted_head = sorted_insert(sorted_head, current, key)
        current = next_node

    linked_list.head = sorted_head

    return linked_list

def sorted_insert(sorted_head, new_node, key=lambda x: x):

    if not sorted_head or key(new_node) < key(sorted_head):
        new_node.next = sorted_head
        return new_node

    current = sorted_head
    while current.next and key(current.next) < key(new_node):
        current = current.next

    new_node.next = current.next
    current.next = new_node

    return sorted_head


def show_floors_and_patterns(floors):
    print('Pisos y patrones disponibles:')
    current = floors.head
    floors_sorted = LinkedList() 
    while current:
        floor_name = current.floor_name
        R = current.R
        C = current.C
        F = current.F
        S = current.S
        patterns = current.patterns

        sorted_patterns = {code: patterns[code] for code in sorted(patterns.keys())}

        floors_sorted.append(floor_name, R, C, F, S, sorted_patterns)  
        current = current.next

    floors_sorted = sort_linked_list(floors_sorted, key=lambda x: x.floor_name)

    current_sorted = floors_sorted.head
    while current_sorted:
        floor_name = current_sorted.floor_name
        R = current_sorted.R
        C = current_sorted.C
        F = current_sorted.F
        S = current_sorted.S
        patterns = current_sorted.patterns
        print(f'Piso: {floor_name}')
        print(f'Dimensiones: {R} x {C}')
        print(f'Costo de voltear azulejo: {F} Quetzales')
        print(f'Costo de intercambiar azulejos: {S} Quetzales')
        print('Patrones disponibles:')
        for code, (pattern_str, _) in patterns.items():
            print(f'Código: {code}, Patrón: {pattern_str}')
        print()
        current_sorted = current_sorted.next


    floors_sorted = sort_linked_list(floors_sorted, key=lambda x: x.floor_name)

    current_sorted = floors_sorted.head
    while current_sorted:
        floor_name = current_sorted.floor_name
        R = current_sorted.R
        C = current_sorted.C
        F = current_sorted.F
        S = current_sorted.S
        patterns = current_sorted.patterns
        print(f'Piso: {floor_name}')
        print(f'Dimensiones: {R} x {C}')
        print(f'Costo de voltear azulejo: {F} Quetzales')
        print(f'Costo de intercambiar azulejos: {S} Quetzales')
        print('Patrones disponibles:')
        for code, (pattern_str, _) in patterns.items():
            print(f'Código: {code}, Patrón: {pattern_str}')
        print()
        current_sorted = current_sorted.next



if __name__ == "__main__":
    floors = LinkedList()

    xml_file = input("Ingrese el nombre del archivo XML: ")
    tree = ET.parse(xml_file)
    root = tree.getroot()
    for floor in root.findall('piso'):
        name = floor.get('nombre')
        R = int(floor.find('R').text)
        C = int(floor.find('C').text)
        F = int(floor.find('F').text)
        S = int(floor.find('S').text)
        patterns = {}
        for pattern in floor.find('patrones'):
            code = pattern.get('codigo')
            pattern_str = pattern.text.replace('_', '')
            patterns[code] = (pattern_str, [list(pattern_str[i:i+C]) for i in range(0, len(pattern_str), C)])
        floors.append(name, R, C, F, S, patterns)

    while True:
        print('Seleccione una opción:')
        print('1. Convertir patrón')
        print('2. Mostrar pisos y patrones')
        print('3. Salir')
        choice = input('Opción: ')
        if choice == '1':
            floor_name = input('Ingrese el nombre del piso: ')
            initial_code = input('Ingrese el código del patrón inicial: ')
            target_code = input('Ingrese el código del patrón deseado: ')
            convert_pattern(floor_name, initial_code, target_code, floors)
        elif choice == '2':
            show_floors_and_patterns(floors)
        elif choice == '3':
            break
        else:
            print('Opción inválida. Intente nuevamente.')
