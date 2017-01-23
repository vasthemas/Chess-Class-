MOVEMAP = {'a':0 , 'b': 1, 'c': 2, 'd': 3,'e': 4,'f': 5, 'g': 6, 'h': 7,
                   '1': 7, '2': 6, '3' : 5, '4': 4, '5': 3, '6':2, '7':1, '8':0}

PIECEMAP = {'P': [(1,0),(-1,0),(0,1),(0,-1)],
            'R': [(1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0), 
                  (-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0),
                  (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
                  (0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7)],
            'N' : [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(-1,2),(1,-2),(-1,-2)],
            'B' : [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),
                  (1,-1),(2,-2),(3,-3),(4,-4),(5,-5),(6,-6),(7,-7),
                  (-1,1),(-2,2),(-3,3),(-4,4),(-5,5),(-6,6),(-7,7),
                  (-1,-1),(-2,-2),(-3,-3),(-4,-4),(-5,-5),(-6,-6),(-7,-7)],
            'Q' : [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7),
                  (1,-1),(2,-2),(3,-3),(4,-4),(5,-5),(6,-6),(7,-7),
                  (-1,1),(-2,2),(-3,3),(-4,4),(-5,5),(-6,6),(-7,7),
                  (-1,-1),(-2,-2),(-3,-3),(-4,-4),(-5,-5),(-6,-6),(-7,-7),
                   (1,0),(2,0),(3,0),(4,0),(5,0),(6,0),(7,0), 
                  (-1,0),(-2,0),(-3,0),(-4,0),(-5,0),(-6,0),(-7,0),
                  (0,1),(0,2),(0,3),(0,4),(0,5),(0,6),(0,7),
                  (0,-1),(0,-2),(0,-3),(0,-4),(0,-5),(0,-6),(0,-7)],
            'K' : [(1,0),(-1,0),(0,1),(0,-1),(-1,1),(1,-1),(-1,-1),(1,1)]}


CHECK = False 
CHECKMATE = False
            

class Board: 
    
    def __init__(self,board = None): 
        
        
        
        if board == None: 
        
            self.board = [['WR','WN','WB','WQ','WK','WB','WN','WR'],
                      ['WP','WP','WP','WP','WP','WP','WP','WP'],
                      ['0 ','0 ','0 ','0 ','0 ','0 ','0 ','0 '],
                      ['0 ','0 ','0 ','0 ','0 ','0 ','0 ','0 '],
                      ['0 ','0 ','0 ','0 ','0 ','0 ','0 ','0 '],
                      ['0 ','0 ','0 ','0 ','0 ','0 ','0 ','0 '],
                      ['BP','BP','BP','BP','BP','BP','BP','BP'],
                      ['BR','BN','BB','BQ','BK','BB','BN','BR']] 
        else: 
                self.board = [[board[row][col] for col in range(8)] 
                           for row in range(8)]
        
        
        
    def __str__(self):
        
        '''
        returns human readable board representation of given game state
        '''
        y = ['8','7','6','5','4','3','2','1']
        x = '   a,    b,    c,    d,    e,    f,    g,    h'
        ans = ""
        for row in range(8):
                ans += y[row] + str(self.board[row])
                ans += "\n"
        ans += x 
        return ans
    
    
    
    def is_empty(self,x,y):
        '''
        determines if the given cell is empty 
        ''' 
        
        if self.board[x][y] == '0 ': 
            return True
        else:
            return False
    
    def clone(self): 
        
        
        return Board(board = self.board)
  

        
    def is_inpath(self,x,y,v,w):
        '''
        determines list of coordinates that correspond to the path from the given points
        '''
        
        path = []
        piece = self.board[x][y]
        prev_pos = (x,y) 
        new_pos = (v,w) 
        diff = (x - v, y - w) 
        
        #avoid dividing by zero to determine offset 
        if diff[0] == 0: 
            offset = diff[0],diff[1]/abs(diff[1])
        elif diff[1] == 0: 
            offset = diff[0]/abs(diff[0]),diff[1]
        else: 
            offset = diff[0]/abs(diff[0]),diff[1]/abs(diff[1]) 
            
            
        
        while new_pos != prev_pos: 
            new_pos = new_pos[0] + offset[0],new_pos[1] + offset[1]  
            path.append(new_pos)
           
        return path 
        
         
    
    def switch_player(self,player): 
        
        if player == 'B': 
            return 'W'
        elif player == 'W': 
            return 'B' 
    
    def find_pieces(self,piece):
        
        
        coord = []
        for i in range(8): 
                for j in range(8): 
                    if self.board[i][j] == piece: 
                        coord.append((i,j)) 
        return coord
    
    def in_danger(self,x,y): 
        
        '''
        determines whether piece is one move away from being killed
        ''' 
        piece = self.board[x][y]
        player = piece[0] 
        coord = (x,y) 
        enemies = [] 
        for i in range(8): 
            for j in range(8):
                look_in = self.board[i][j]
                if look_in[0] != player and look_in[0] != '0':
                    
                    enemies.append((i,j))
        
        
        hostiles = []   
        for enemy in enemies: 
            if self.is_possible(enemy[0],enemy[1],x,y,self.switch_player(player)) == True: 
                hostiles.append(enemy)  
        if len(hostiles) > 0: 
            return True
        else: 
            return False 
            
    def string_coord(self,x,y): 
        
        keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', '1', '2', '3', '4', '5', '6', '7', '8']
        
        x_axis = keys[y]
        y_axis = keys[15 - x] 
        
        pos = str(x_axis)  + str(y_axis) 
        
        return pos 
    
    def check_or_checkmate(self,player):
        
        ''' 
        Check if opposing player is in check or checkmate
        ''' 
        
        
        CHECK = False 
        CHECKMATE = False
        draw = False 
        possible_mov = []
        only_moves = []
        mov_range = PIECEMAP['K']
        
        
        #Determine where king is 
        if player == 'B': 
            coord = self.find_pieces('WK')[0] 
        elif player == 'W': 
            coord = self.find_pieces('BK')[0]
            
            
        str_coord = self.string_coord(coord[0],coord[1]) 
        
        
        #check if opposing player is in check
        if self.in_danger(coord[0],coord[1]) == True: 
                CHECK = True
                         
            

    
        #check whether piece is in checkmate 
        #Create list of possible movements 
        for mov in mov_range:
            c = (coord[0] + mov[0],coord[1] + mov[1])
            if 8 > c[0] > -1 and 8 > c[1] > -1: 
                possible_mov.append(c)
        
        
        #Create list of possible moves 
        for mov in possible_mov: 
            if self.is_possible(coord[0],coord[1],mov[0],mov[1],self.switch_player(player)) == True:
                only_moves.append((mov[0],mov[1]))
        
        
        
        checkless_moves = []
  

        #simulate each possible each possible move to determine checkmate  
        for mov in only_moves:
            simu_game = self.clone()
            simu_coord = self.string_coord(mov[0],mov[1])
            simu_game.move(str_coord,simu_coord,self.switch_player(player))

            if simu_game.in_danger(mov[0],mov[1]) == False:     
                        checkless_moves.append(mov)

        print checkless_moves 
        if len(checkless_moves) == 0:   
                CHECKMATE = True
            

        if CHECK == True and CHECKMATE == True:   
                    print str(self.switch_player(player)) + 'hite player in Checkmate'
                    return CHECKMATE 
        elif CHECK == True and CHECKMATE == False: 
                print str(self.switch_player(player)) + 'Check'
                return CHECK  
        else: 
                return CHECK 
            
   
            
  
    def is_possible(self,x,y,v,w,player):
        '''
        determines if the given move allowed to be placed in the game
        '''
        
        n_mov = (v,w) 
        move = (x,y)
        piece = self.board[x][y]
        n_piece = self.board[v][w]
        
        
        if piece == '0 ' :
 
            return False 
        
        
        mov_range = PIECEMAP[piece[1]]
        possible_mov = []
        passable = []
        impassable = []
        
        if piece[0] != player: 
            return False 
        
        
        # if pawn is attacking 
        if piece[1] == 'P' and n_piece[0] != player and n_piece[0] != '0': 
            if piece[0] == 'B': 
                mov_range = [(-1,-1),(-1,1)]
            elif piece[0] == 'W':
                mov_range = [(1,1),(1,-1)] 
        
        
        
        # All possible moves on board
        for mov in mov_range:
           c = (move[0] + mov[0],move[1] + mov[1])
           if 8 > c[0] > -1 and 8 > c[1] > -1: 
                possible_mov.append(c)
        
 
        # All passable moves that are not obstructed by player's pieces   
        for mov in possible_mov:
            piece_mov = self.board[mov[0]][mov[1]]
            if player == 'B':
                
                if piece_mov[0] != 'B':
                    passable.append(mov) 
                else: 
                    impassable.append(mov)
            elif player == 'W':
                
                if piece_mov[0] != 'W':
                    passable.append(mov) 
                else: 
                    impassable.append(mov)
        
        # Knight exception for passable moves 
        if piece[1] == 'N':
            if n_mov in passable: 
                return True
            else: 
                return False
        #Determine path and if movement is obstucted     
        else:
            if n_mov not in passable: 
                return False 
            
            else: 
                path = self.is_inpath(x,y,v,w)
                if len(set(impassable).intersection(path)) > 0:
                    return False
                else: 
                    return True
               

    
    def move(self,prev_move,new_move,player):
        '''
        places new move into board, given that the move is possible 
        '''  
        # Coordinated of move 
        new_pos =  MOVEMAP[new_move[1]],MOVEMAP[new_move[0]]
        prev_pos = MOVEMAP[prev_move[1]],MOVEMAP[prev_move[0]]
        
        # if move is empty or the attack or path is not obstructed 
        if self.is_possible(prev_pos[0],prev_pos[1],new_pos[0],new_pos[1],player) == True:
            old = self.board[prev_pos[0]][prev_pos[1]]
            new = self.board[new_pos[0]][new_pos[1]]
            
            #replace killed piece with empty 
            if new[0] != player: 
                self.board[new_pos[0]][new_pos[1]] = old
                self.board[prev_pos[0]][prev_pos[1]] = '0 '
       
            else: 
                self.board[new_pos[0]][new_pos[1]] = old
                self.board[prev_pos[0]][prev_pos[1]] = new
      
           
        else: 
            return False
               
      
     
        
                                          
#########################################################################################
 #User Interface
###################################################################################

def play():
            
    game = Board()
    print game
    player = 'B'

    while CHECKMATE == False:        
        
         if player == 'B':
             Player = 'Black'
         elif player == 'W':
             Player = 'White'

         move = raw_input( Player + "'s Move: ")  

         current_move = move[0:2]
         new_move =  move[2:4]
         if game.move(current_move,new_move, player) == False:
             print 'Input incorrect: please try again'
         else:
             game.check_or_checkmate(player) 
             print game
             player =  game.switch_player(player)
             
 #        game.move(current_move,new_move, player)
          
 
         
test= Board()

test.move('e2','e3','B')

test.move('d1','h5','B')

test.move('h5','f7','B')

test.move('f1','c4','B')



test.check_or_checkmate('B')


print test


            




