import sys

# nuruomino.py: Template para implementação do projeto de Inteligência Artificial 2024/2025.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 05:
# 111139 Afonso Bastos
# 107192 David Santos

from search import (
    Problem,
    Node,
    depth_first_graph_search,
)

class Pieces:
    '''Classe que contém as peças do puzzle Nuruomino e as suas restrições.
    Restrições são: Top, Down, Left e Right.'''
    def __init__(self):
        self.pieces = ["0L1","1L1","0L2","1L2","0L3","1L3","0L4","1L4","0L5","1L5", 
                       "0L6","1L6","0L7","1L7","0L8","1L8","0I1","1I1","0I2","1I2", 
                       "0T1","1T1","2T1","0T2","1T2","2T2","0T3","1T3","2T3","0T4",
                       "1T4","2T4","0S1","1S1","0S2","1S2","0S3","1S3","0S4","1S4"]
        self.forbidden = {
            't': ["0L2","1L4","0L6","1L8","1I1","2T1","1T2","0T4","1S2","1S3"],
            'd': ["1L1","0L3","1L5","0L7","0I1","0T2","2T3","1T4","0S2","0S3"],
            'l': ["0L1","1L2","1L7","0L8","1I2","1T1","0T3","2T4","1S1","0S4"],
            'r': ["1L3","0L4","0L5","1L6","0I2","0T1","2T2","1T3","0S1","1S4"],
        }
        self.forbidden['T'] = self.forbidden['t'] + ["0L1","1L3","0L5","2T2","2T4","1T3","0T3","0S1","0S4"]
        self.forbidden['D'] = self.forbidden['d'] + ["1L2","0L4","1L6","0L8","0T1","1T1","2T2","2T4","1S1","1S4"]
        self.forbidden['L'] = self.forbidden['l'] + ["0L3","1L4","1L5","0L6","0T2","1T2","2T3","1S2","0S3"]
        self.forbidden['R'] = self.forbidden['r'] + ["1L1","0L2","0L7","1L8","2T1","2T3","1T4","0T4","0S2","1S3"]
    
    def piece_box(self, piece_config: str, coord: tuple):
        '''Dicionário com as possíveis configurações de cada peça, com base no
        ponto de referência da mesma. Devolve a peça com a respectiva configuração.'''
        x, y, config, piece = coord[0], coord[1], int(piece_config[0]), piece_config[1:]
        d = {"L1": [[(x,y),(x,y-1),(x-1,y-1),(x-2,y-1)],[(x,y),(x+1,y),(x+2,y),(x+2,y+1)]],             
             "L2": [[(x,y),(x-1,y),(x-1,y+1),(x-1,y+2)],[(x,y),(x,y-1),(x,y-2),(x+1,y-2)]],             
             "L3": [[(x,y),(x+1,y),(x+1,y-1),(x+1,y-2)],[(x,y),(x,y+1),(x,y+2),(x-1,y+2)]],
             "L4": [[(x,y),(x,y+1),(x+1,y+1),(x+2,y+1)],[(x,y),(x-1,y),(x-2,y),(x-2,y-1)]],
             "L5": [[(x,y),(x,y+1),(x-1,y+1),(x-2,y+1)],[(x,y),(x+1,y),(x+2,y),(x+2,y-1)]],
             "L6": [[(x,y),(x-1,y),(x-1,y-1),(x-1,y-2)],[(x,y),(x,y+1),(x,y+2),(x+1,y+2)]],
             "L7": [[(x,y),(x+1,y),(x+1,y+1),(x+1,y+2)],[(x,y),(x,y-1),(x,y-2),(x-1,y-2)]],             
             "L8": [[(x,y),(x,y-1),(x+1,y-1),(x+2,y-1)],[(x,y),(x-1,y),(x-2,y),(x-2,y+1)]],
             "I1": [[(x,y),(x+1,y),(x+2,y),(x+3,y)],[(x,y),(x-1,y),(x-2,y),(x-3,y)]],
             "I2": [[(x,y),(x,y+1),(x,y+2),(x,y+3)],[(x,y),(x,y-1),(x,y-2),(x,y-3)]],
             "T1": [[(x,y),(x,y+1),(x+1,y+1),(x,y+2)],[(x,y),(x,y-1),(x+1,y-1),(x,y-2)],[(x,y),(x-1,y-1),(x-1,y),(x-1,y+1)]],
             "T2": [[(x,y),(x+1,y),(x+1,y-1),(x+2,y)],[(x,y),(x-1,y),(x-1,y-1),(x-2,y)],[(x,y),(x,y+1),(x-1,y+1),(x+1,y+1)]],
             "T3": [[(x,y),(x,y-1),(x-1,y-1),(x,y-2)],[(x,y),(x,y+1),(x-1,y+1),(x,y+2)],[(x,y),(x+1,y),(x+1,y-1),(x+1,y+1)]],
             "T4": [[(x,y),(x-1,y),(x-1,y+1),(x-2,y)],[(x,y),(x+1,y),(x+1,y+1),(x+2,y)],[(x,y),(x,y-1),(x+1,y-1),(x-1,y-1)]],
             "S1": [[(x,y),(x,y+1),(x-1,y+1),(x-1,y+2)],[(x,y),(x,y-1),(x+1,y-1),(x+1,y-2)]],
             "S2": [[(x,y),(x+1,y),(x+1,y+1),(x+2,y+1)],[(x,y),(x-1,y),(x-1,y-1),(x-2,y-1)]],
             "S3": [[(x,y),(x+1,y),(x+1,y-1),(x+2,y-1)],[(x,y),(x-1,y),(x-1,y+1),(x-2,y+1)]],
             "S4": [[(x,y),(x,y-1),(x-1,y-1),(x-1,y-2)],[(x,y),(x,y+1),(x+1,y+1),(x+1,y+2)]],
            }
        return d[piece][config]
    
    def get_redundant_actions(self, action: tuple) -> list:
        ''' Retorna todas as ações redundantes.
        Cada Action é da forma (coordenada, peça).
        '''
        coord, piece = action[0], action[1]
        x, y = coord[0], coord[1]
        d = {
         '0L1': [((x-2, y-1), '1L1')],
         '1L1': [((x+2, y+1), '0L1')],
         '0L2': [((x-1, y+2), '1L2')],
         '1L2': [((x+1, y-2), '0L2')],
         '0L3': [((x-1, y+2), '1L3')],
         '1L3': [((x+1, y-2), '0L3')],
         '0L4': [((x+2, y+1), '1L4')],
         '1L4': [((x-2, y-1), '0L4')],
         '0L5': [((x-2, y+1), '1L5')],
         '1L5': [((x+2, y-1), '0L5')],
         '0L6': [((x-1, y-2), '1L6')],
         '1L6': [((x+1, y+2), '0L6')],
         '0L7': [((x+1, y+2), '1L7')],
         '1L7': [((x-1, y-2), '0L7')],
         '0L8': [((x+2, y-1), '1L8')],
         '1L8': [((x-2, y+1), '0L8')],
         '0I1': [((x+3, y), '1I1')],
         '1I1': [((x-3, y), '0I1')],
         '0I2': [((x, y+3), '1I2')],
         '1I2': [((x, y-3), '0I2')],
         '0T1': [((x, y+2), '1T1'), ((x+1, y+1), '2T1')],
         '1T1': [((x, y-2), '0T1'), ((x+1, y-1), '2T1')],
         '2T1': [((x-1, y-1), '0T1'), ((x-1, y+1), '1T1')],
         '0T2': [((x+2, y), '1T2'), ((x+1, y-1), '2T2')],
         '1T2': [((x-2, y), '0T2'), ((x-1, y-1), '2T2')],
         '2T2': [((x-1, y+1), '0T2'), ((x+1, y+1), '1T2')],
         '0T3': [((x, y-2), '1T3'), ((x-1, y-1), '2T3')],
         '1T3': [((x, y+2), '0T3'), ((x-1, y+1), '2T3')],
         '2T3': [((x+1, y+1), '0T3'), ((x+1, y-1), '1T3')],
         '0T4': [((x-2, y), '1T4'), ((x-1, y+1), '2T4')],
         '1T4': [((x+2, y), '0T4'), ((x+1, y+1), '2T4')],
         '2T4': [((x+1, y-1), '0T4'), ((x-1, y-1), '1T4')],
         '0S1': [((x-1, y+2), '1S1')],
         '1S1': [((x+1, y-2), '0S1')],
         '0S2': [((x+2, y+1), '1S2')],
         '1S2': [((x-2, y-1), '0S2')],
         '0S3': [((x+2, y-1), '1S3')],
         '1S3': [((x-2, y+1), '0S3')],
         '0S4': [((x-1, y-2), '1S4')],
         '1S4': [((x+1, y+2), '0S4')]
        }     
        return d[piece]        

    
    def get_permited_pieces(self, restrictions: str) -> list:
        '''Devolve uma lista das peças que podem ser colocadas'''
        f = []
        for c in restrictions:
            f.extend(self.forbidden[c])
        return [p for p in self.pieces if p not in f]

class NuruominoState:
    '''Representação interna de um estado do Puzzle Nuruomino.'''
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NuruominoState.state_id
        NuruominoState.state_id += 1

    def __lt__(self, other):
        ''' Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. '''
        return self.id < other.id

class Board:
    ''' Representação interna de um tabuleiro do Puzzle Nuruomino.'''
    def __init__(self, grid:list, alt_grid: list, grid_size:int, num_regions:int, regions:dict, region_adjacency:dict, locked: list, connections: dict, actions_dict: dict, actions: list, is_solution: bool):
        self.grid = grid
        self.alt_grid = alt_grid
        self.grid_size = grid_size
        self.num_regions = num_regions
        self.regions = regions
        self.region_adjacency = region_adjacency
        self.locked = locked
        self.connections = connections
        self.actions_dict = actions_dict
        self.actions = actions
        self.is_solution = is_solution

    
    def copy(self):
        '''Cria uma deep copy do tabuleiro, copiando a grid, a grid alternativa (usada 
        posteriormente na matriz de adjacências), o tamanho da grid, as regiões e 
        o número das mesmas, bem como as suas adjacências, bem como as regiões
        já ocupadas, as conexões entre regiões e um valor que verifica 
        se o state é uma solução do problema.'''
        grid = [row[:] for row in self.grid]
        alt_grid = self.alt_grid
        grid_size = self.grid_size
        num_regions = self.num_regions
        regions = self.regions
        region_adjacency = self.region_adjacency
        locked = self.locked[:]
        connections = {key: value[:] for key, value in self.connections.items()}
        actions_dict = {key: value[:] for key, value in self.actions_dict.items()}
        actions = self.actions[:]
        is_solution = self.is_solution
        return Board(grid, alt_grid, grid_size, num_regions, regions, region_adjacency, locked, connections,actions_dict, actions, is_solution)

    
    def valid_coord(self, coord: tuple) -> bool:
        '''Verifica se as coordenadas são válidas.'''
        return coord[0] >= 0 and coord[1] >= 0
    
    def filter_coord(self, tpl: tuple) -> tuple:
        return tpl[0]
    
    def filter_restriction(self, tpl: tuple) -> str:
        return tpl[1]

    def adjacent_regions(self, region:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento."""
        return self.region_adjacency[region]
    
    def get_locked_adjacent_regions(self, region: int) -> list:
        return [regions for regions in self.adjacent_regions(region) if self.locked[regions-1]]
    
    def adjacent_positions(self, coord: tuple) -> list:
        """Devolve as coordenadas adjacentes à região, em todas as direções, incluindo diagonais."""
        row, col = coord[0], coord[1]
        cima = (row-1, col) if row-1 >= 0 else None
        baixo = (row+1, col) if row+1 < self.grid_size else None
        esquerda = (row, col-1) if col-1 >= 0 else None
        direita = (row, col+1) if col+1 < self.grid_size else None
        diag_sup_esq = (row-1, col-1) if row-1 >= 0 and col-1 >= 0 else None
        diag_sup_dir = (row-1, col+1) if row-1 >= 0 and col+1 < self.grid_size else None
        diag_inf_esq = (row+1, col-1) if row+1 < self.grid_size and col-1 >= 0 else None
        diag_inf_dir = (row+1, col+1) if row+1 < self.grid_size and col+1 < self.grid_size else None
        return [cima, baixo, esquerda, direita, diag_sup_esq, diag_sup_dir, diag_inf_esq, diag_inf_dir]
    
    def get_value(self, coord: tuple):
        row, col = coord[0], coord[1]
        return self.grid[row][col]
    
    def set_value(self, coord: tuple, val):
        row, col = coord[0], coord[1]
        self.grid[row][col] = val

    def adjacent_values(self, coord: tuple) -> list:
        """Devolve os valores das celulas adjacentes à região, em todas as direções, incluindo diagonais."""
        values = []
        adjacent_positions = self.adjacent_positions(coord)
        for coords in adjacent_positions:
            if coords is None: 
                values.append(None)
            else: 
                values.append(self.get_value(coords))
        return values
    
    def belongs_to_region(self, coord: tuple, region: int) -> bool:
        """
        Checks if a coordinate belongs to the region
        """
        value = self.get_value(coord)
        if isinstance(value, str):
            if len(value[1:]) > 0:
                return int(value[1:]) == region
            return False
        return value == region
    
    def check_squares(self, box:list, c: list, a: list):
        """
        Função que verifica a existência de áreas 2x2 no tabuleiro.
        c: lista de posições adjacentes e diagonais
        a: lista de valores adjacentes e diagonais
        """
        if (isinstance(a[0], str) or c[0] in box) and (isinstance(a[4], str) or c[4] in box) and (isinstance(a[2], str) or c[2] in box):
            return True
        if (isinstance(a[0], str) or c[0] in box) and (isinstance(a[5], str) or c[5] in box) and (isinstance(a[3], str) or c[3] in box):
            return True
        if (isinstance(a[1], str) or c[1] in box) and (isinstance(a[2], str) or c[2] in box) and (isinstance(a[6], str) or c[6] in box):
            return True
        if (isinstance(a[1], str) or c[1] in box) and (isinstance(a[3], str) or c[3] in box) and (isinstance(a[7], str) or c[7] in box):
            return True
        return False
    
    def valid_connection(self, a: list, piece: str, region: int):
        '''Verifica se a peça pode ser colocada na região, de acordo com as regras do jogo.
        A peça é válida se as posições adjacentes não forem ocupadas por peças do mesmo tipo.'''
        def valid(ortogonal_value, piece: str):
            '''Verifica se a peça é válida de acordo com as regras do jogo.
            ortogonal_value: valor de posição ortogonal''' 
            kind = piece[1]
            if isinstance(ortogonal_value, str):
                if ortogonal_value[0] != kind:
                    return True
                #Para tamanhos maiores que 2
                if len(ortogonal_value[1:]) > 0:
                    return int(ortogonal_value[1:]) == region
                else:
                    return False
            return True
        return valid(a[0], piece) and valid(a[1], piece) and valid(a[2], piece) and valid(a[3], piece)            
    
    def fits(self, box:list, region: int, piece: str):
        ''' Verifica se a hitbox da peça pode ser colocada no tabuleiro 
        a partir de uma dada coordenada.
        '''
        try:
            for coord in box:
                if not (self.valid_coord(coord) and self.belongs_to_region(coord, region)):
                    return False
                c = self.adjacent_positions(coord)
                a = self.adjacent_values(coord)
                if self.check_squares(box, c, a) or not self.valid_connection(a, piece, region):
                    return False
        except IndexError:
            return False
        return True
    
    def connects(self, box: list, region: int):
        '''
        Verifica se uma certa peça conecta com outra de uma região diferente.
        '''
        for coord in box:
            a = self.adjacent_values(coord)
            for i in range(4):
                if a[i] is None:
                    continue
                if isinstance(a[i], str) and len(a[i]) == 1:
                    return True
        return False
    
    def get_value_alt(self, coord: tuple):
        row, col = coord[0], coord[1]
        return self.alt_grid[row][col]
    
    def print_grid(self):
        for row in self.grid:
            print('\t'.join(str(x) for x in row))


    @staticmethod
    def parse_instance():
        '''Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.
        '''
        grid = []
        regions = {}
        region_adjacency = {}

        def set_adjacency(current, second):
            '''Função que define a adjacência entre duas regiões.'''
            try:
                if second not in region_adjacency[current]:
                    region_adjacency[current] += [second]
            except KeyError or IndexError:
                region_adjacency[current] = [second]
            try:
                if current not in region_adjacency[second]:
                    region_adjacency[second] += [current]
            except KeyError or IndexError:
                region_adjacency[second] = [current]


        for line in sys.stdin:
            if line.strip():  # skip empty lines
                row = [int(x) for x in line.strip().split('\t')]
                grid.append(row)
                
        size = len(grid[0])
        alt_grid = [el[:] for el in grid]

        def add_to_regions(region, t):
            '''Função que adiciona uma região à lista de regiões.'''
            try:
                regions[region] += [t]
            except KeyError or IndexError:
                regions[region] = [t]

        def compute_regions(coord):
            '''Função que regista as regiões do tabuleiro.'''
            kind = ""
            is_edge = False
            row = coord[0]
            col = coord[1]
            current = grid[row][col]
            #cima
            if row == 0:
                kind += 'T'
            elif row > 0 and grid[row-1][col] != current:
                is_edge = True
                kind += 't'
                set_adjacency(current, grid[row-1][col])
            #baixo
            if row == size-1:
                kind += 'D'
            elif row < size-1 and grid[row+1][col] != current:
                is_edge = True
                kind += 'd'
                set_adjacency(current, grid[row+1][col])
            #esquerda
            if col == 0:
                kind += 'L'
            elif col > 0 and grid[row][col-1] != current:
                is_edge = True
                kind += 'l'
                set_adjacency(current, grid[row][col-1])
            #direita
            if col == size-1:
                kind += 'R'
            elif col < size-1 and grid[row][col+1] != current:
                is_edge = True
                kind += 'r'
                set_adjacency(current, grid[row][col+1])
            if is_edge:
                add_to_regions(current, (coord, kind))

        for i in range(size):
            for j in range(size):
                compute_regions((i, j))

        num_regions = len(regions)
        locked = [False for _ in range(num_regions)]
        connections = {region: [] for region in range(1, num_regions+1)}
        actions_dict = {region: [] for region in range(1, num_regions+1)}
        return Board(grid, alt_grid, size, num_regions, regions, region_adjacency, locked, connections, actions_dict, [], False) 

class Nuruomino(Problem):
    '''Classe que representa o problema Nuruomino.'''
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial = NuruominoState(board)
        self.pieces = Pieces()


    def paint(self, board: Board, box: list, paint: str):
        '''Função que pinta a área da peça no tabuleiro.'''
        for coord in box:
            board.set_value(coord, paint)

    
    def update_grey_area(self, carry: list, new: list, flag: bool):
        '''Função que atualiza a área cinza (grey area) do tabuleiro.
        Uma grey area é uma área que pode ser imediatamente preenchida,
        independentemente da peça que vá lá ser colocada. As grey areas 
        são apenas para read, e não computadas no resultado final.'''
        size = len(carry)
        if size == 0 and not flag:
            carry[:] = new
            flag = True
        elif size > 0 and flag:
            carry[:] = list(set(carry) & set(new))
        return flag
    
    def connect_regions(self, board: Board, box: list, region: int):
        '''Função que conecta as regiões adjacentes à região atual.'''
        connecting = []
        for coord in box:
            a = board.adjacent_positions(coord)
            v = board.adjacent_values(coord)
            for i in range(4):
                if a[i] is None:
                    continue
                current_adj = board.get_value_alt(a[i])
                if isinstance(v[i], str) and len(v[i]) == 1 and current_adj != region:
                    if current_adj not in board.connections[region]:
                        connecting.append(current_adj)
                    if region not in board.connections[current_adj]:
                        board.connections[current_adj].append(region)
        board.connections[region].extend(connecting)


    def has_islands(self, connections: dict):
        '''Verifica se existem ilhas no tabuleiro.
        Uma ilha é uma reigião/conjunto de regiões com peça(s) lá dentro que
        não estão conectadas a outras regiões.'''
        visited = set()

        def dfs(node):
            if node in visited:
                return
            visited.add(node)
            for neighbor in connections.get(node, []):
                dfs(neighbor)

        # Start DFS from the first region
        start_node = next(iter(connections))
        dfs(start_node)

        # If the number of visited nodes is less than total, there are islands
        return len(visited) != len(connections)    
        

    def actions(self, state: NuruominoState):
        '''Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. Action terá o seguinte
        formato: (região, coordenada, peça)'''
        return state.board.actions

    def result(self, state: NuruominoState, action):
        '''Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state).'''
        def toggle(f: bool):
            f = False if f == True else False
            return f
        
        actions = []
        #Executes the action
        region, coord, piece = action[0], action[1], action[2]
        box = self.pieces.piece_box(piece, coord)
        board = state.board.copy()
        if not state.board.fits(box, region, piece):
            board.actions = []
            return NuruominoState(board)
        board.actions.clear()
        self.connect_regions(board, box, region)
        self.paint(board, box, piece[1])
        board.locked[region-1] = True
        #Checks for winning conditions after the action
        if sum(board.locked) == board.num_regions:
            has_islands = self.has_islands(board.connections)
            if has_islands:
                board.actions = []
                return NuruominoState(board)
            board.is_solution = True
            board.actions = []
            return NuruominoState(board)
        
        #Calculates possible actions and performs destructive procedures
        pieces = self.pieces
        first_time = True
        num_regions = board.num_regions
        num_actions = [0 for _ in range(num_regions)]
        locked = board.locked
        for region in range(1, num_regions + 1):
            if locked[region-1]:
                continue  
            isolated = False
            too_large = False
            surrounded = False
            if len(board.regions[region]) > 7:
                too_large = True
            num_locked_adjacent_regions = len(board.get_locked_adjacent_regions(region))
            if num_locked_adjacent_regions == 0:
                isolated = True
            if too_large and isolated:
                continue
            if num_locked_adjacent_regions == len(board.adjacent_regions(region)):
                surrounded = True
            gray_area = []
            flag = False
            common_piece = None
            for action in board.actions_dict[region][:]:
                    coord = action[1]
                    p = action[2]
                    box = pieces.piece_box(p, coord)
                    if not board.fits(box, region, p) or (surrounded and not board.connects(box, region)):
                        board.actions_dict[region].remove(action)
                    else:
                        if not flag:                            
                            common_piece = p[1]
                        else:
                            if p[1] != common_piece:
                                common_piece = None
                        flag = self.update_grey_area(gray_area, box, flag)
            
            paint: any
            size = len(board.actions_dict[region])
            if size == 0:
                board.actions = []
                return NuruominoState(board)
            elif size == 1:
                piece, coor = board.actions_dict[region][0][2], board.actions_dict[region][0][1]
                box = pieces.piece_box(piece, coor)
                self.connect_regions(board, box, region)
                self.paint(board, box, piece[1])
                locked[region-1] = True
                board.actions_dict[region].clear()
                if sum(board.locked) == num_regions:
                    has_islands = self.has_islands(board.connections)
                    if has_islands:
                        board.actions = []
                        return NuruominoState(board)
                    board.is_solution = True
                    board.actions = []
                    return NuruominoState(board)
            else:
                if common_piece != None:
                    paint = common_piece+str(region)
                else:
                    paint = 'G'+str(region)
                self.paint(board, gray_area, paint)
            if isolated and not first_time:
                num_actions[region-1] = 0
                continue

            first_time = toggle(first_time)
            num_actions[region-1] += len(board.actions_dict[region])
            actions.extend(board.actions_dict[region])        
                 
        actions.sort(key = lambda action: (num_actions[action[0]-1], -len(board.get_locked_adjacent_regions(action[0]))))
        board.actions = actions
        return NuruominoState(board)
        

    def goal_test(self, state: NuruominoState):
        '''Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema.'''      
        return state.board.is_solution
    
    def initialization(self):
        board = self.initial.board
        def toggle(f: bool):
            f = False if f == True else False
            return f
        
        pieces = self.pieces
        first_time = True
        num_regions = board.num_regions
        num_actions = [0 for _ in range(num_regions)]
        regions = board.regions
        locked = board.locked
        actions = []
        for region in range(1, num_regions + 1):
            isolated = False
            too_large = False
            surrounded = False
            if len(board.regions[region]) > 7:
                too_large = True
            num_locked_adjacent_regions = len(board.get_locked_adjacent_regions(region))
            if num_locked_adjacent_regions == 0:
                isolated = True
            if num_locked_adjacent_regions == len(board.adjacent_regions(region)):
                surrounded = True                  
            cords = regions[region]
            possible_actions = []
            redundant_actions = []
            gray_area = []
            flag = False
            common_piece = None
            for c in cords:
                coord = board.filter_coord(c)
                restrictions = board.filter_restriction(c)
                permited_pieces = pieces.get_permited_pieces(restrictions)
                for p in permited_pieces:
                    box = pieces.piece_box(p, coord)
                    if (coord, p) not in redundant_actions and board.fits(box, region, p):                       
                        if surrounded and not board.connects(box, region):
                            continue
                        possible_actions.append((region, coord, p))
                        redundant_actions.extend(pieces.get_redundant_actions((coord, p)))
                        if not flag:                            
                            common_piece = p[1]
                        else:
                            if p[1] != common_piece:
                                common_piece = None
                        flag = self.update_grey_area(gray_area, box, flag)
            
            paint: any
            size = len(possible_actions)
            if size == 1:
                piece, coor = possible_actions[0][2], possible_actions[0][1]
                box = pieces.piece_box(piece, coor)
                self.connect_regions(board, box, region)
                self.paint(board, box, piece[1])
                locked[region-1] = True
                possible_actions.clear()
            else:
                if common_piece != None:
                    paint = common_piece+str(region)
                else:
                    paint = 'G'+str(region)
                self.paint(board, gray_area, paint)
            board.actions_dict[region].extend(possible_actions)
            if too_large and isolated:
                possible_actions.clear()
            elif isolated and first_time:
                first_time = toggle(first_time)
            elif isolated and not first_time:
                possible_actions.clear()

            
            num_actions[region-1] += len(possible_actions)
            actions.extend(possible_actions)        
                 
        actions.sort(key = lambda action: (num_actions[action[0]-1], -len(board.get_locked_adjacent_regions(action[0]))))
        board.actions = actions

board = Board.parse_instance()
problem = Nuruomino(board)
problem.initialization()
solution_node = depth_first_graph_search(problem)
if solution_node is not None:
   solution_node.state.board.print_grid()
