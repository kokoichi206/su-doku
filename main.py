import sys


class Board(object):
     def __init__(self, board):
          self.board = board

          decided_places = [[None for _ in range(9)] for _ in range(9)]
          candidates = [[[f'{i}' for i in range(1, 10)] for _ in range(9) ] for _ in range(9)]
          cnt = 0
          for i in range(9):
               for j in range(9):
                    # print(i, j, 'value = ', self.board[i][j])
                    if board[i][j] != '0':
                         # candidates[i][j] = None
                         candidates[i][j] = '0'
                         decided_places[i][j] = board[i][j]
                         cnt += 1
          # print(cnt) # 何箇所埋まっているか
          self.decided_places = decided_places
          self.candidates = candidates
          self.cnt = cnt

     # 2次元配列を転置する関数
     def transpose(self, x: list) -> list:
          row = len(x)
          col = len(x[0])
          tmp = [[['_'] for _ in range(row) ] for _ in range(col)]
          
          for i in range(row):
               for j in range(col):
                    tmp[j][i] = x[i][j]
          
          return tmp

     # candidateが0は、既に決定していることを表す
     def delete_candidate(self):
          for i in range(9):
               for j in range(9):
                    if self.decided_places[i][j]:
                         for k in range(9):
                              # print(self.candidates[i][k])
                              if self.decided_places[i][j] in list(self.candidates[i][k]):
                                   if self.candidates[i][k] != '0':
                                        self.candidates[i][k].remove(self.decided_places[i][j])
                              if self.decided_places[i][j] in list(self.candidates[k][j]):
                                   if self.candidates[k][j] != '0':
                                        self.candidates[k][j].remove(self.decided_places[i][j])
                         row_block = i // 3
                         colum_block = j // 3
                         for l in range(3):
                              for m in range(3):
                                   row = row_block * 3 + l
                                   colum = colum_block * 3 + m
                                   if self.decided_places[i][j] in list(self.candidates[row][colum]):
                                        if self.candidates[row][colum] != '0':
                                             self.candidates[row][colum].remove(self.decided_places[i][j])

     # 各要素に対して、候補が1なら決定する。
     def check_cand(self):
          for i in range(9):
               for j in range(9):
                    # print(self.candidates[i][j])
                    # print('len ',len(self.candidates[i][j]))
                    if (self.candidates[i][j]) and (len(self.candidates[i][j]) == 1):
                         if self.candidates[i][j] != '0':
                              self.decided_places[i][j] = self.candidates[i][j][0]
                              # self.candidates[i][j] = None
                              self.candidates[i][j] = '0'
                              self.cnt += 1
                              
                              # print(i,j) #確定させた場所のプリント

     # 各列、行、ブロックがその数字をもつかチェック
     def check_cand_by_num(self):
          cand_trans = self.transpose(self.candidates)
          det_trans = self.transpose(self.decided_places)
          # 各数字ごとにみていく
          for NUM in range(1, 10):
               # 各列と各行について
               for i in range(9):
                    r = 0
                    c = 0
                    if str(NUM) in self.decided_places[i]:
                         r += 1
                    if r == 0:
                         rr = []
                         for j in range(9):
                              if str(NUM) in self.candidates[i][j]:
                                   rr.append(j)
                         if len(rr) == 1:
                              self.candidates[i][rr[0]] = '0'
                              self.decided_places[i][rr[0]] = str(NUM)
                              self.cnt += 1

                    if str(NUM) in det_trans[i]:
                         c += 1
                    if c == 0:
                         cc = []
                         for j in range(9):
                              if str(NUM) in cand_trans[i][j]:
                                   cc.append(j)
                         if len(cc) == 1:
                              self.candidates[cc[0]][i] = '0'
                              self.decided_places[cc[0]][i] = str(NUM)
                              self.cnt += 1

               # 各ブロックについて
               for i in range(3):
                    for j in range(3):
                         # 各ブロック内での9個をチェック
                         b = 0
                         bb = []
                         for l in range(3):
                              for m in range(3):
                                   x = 3 * i + l
                                   y = 3 * j + m
                                   if self.decided_places[x][y] == str(NUM):
                                        b += 1
                                   if str(NUM) in self.candidates[x][y]:
                                        bb.append((x, y))
                         if b == 0:
                              if len(bb) == 1:
                                   x, y = bb[0]
                                   self.candidates[x][y] = '0'
                                   self.decided_places[x][y] = str(NUM)
                                   self.cnt += 1


     # def check_num_cand(self):
     #      # i番目はi+2個の候補がある
     #      tmp = [[] for _ in range(8)]
     #      for i in range(9):
     #           for j in range(9):
     #                num = len(self.candidates[i][j])
     #                if num >= 2:
     #                     tmp[num-2].append([i,j])
     #      print(tmp)
     #      self.num_of_cand = tmp

     # def afafa(self):
     #      for x in self.num_of_cand:
     #           for i,j in x:
     #                print(i, j)



if __name__ == '__main__':

     # 初期MAPの読み込み
     # 一応引数から他ファイルのMAPを読めるようにした
     if len(sys.argv) > 1:
          try:
               with open(sys.argv[1], mode='r') as f:
                    files = f.readlines()
                    print('file opened')
                    files = [x.replace('\n','') for x in files]
                    files = [x.split(' ') for x in files]
                    files = [[list(x) for x in files[i]] for i in range(9)]
                    maps = [x[0] + x[1] + x[2] for x in files]
          except:
               print('exception')
               pass
     else:
          # easy なやつ     
          # maps = [[['0', '1', '4'], ['6', '0', '8'], ['2', '7', '0']],
          # [['7', '0', '2'], ['4', '0', '9'], ['1', '0', '8']],
          # [['6', '8', '0'], ['2', '0', '1'], ['0', '3', '5']],
          # [['9', '5', '3'], ['0', '0', '0'], ['7', '4', '2']],
          # [['0', '0', '0'], ['0', '0', '0'], ['0', '0', '0']],
          # [['1', '2', '8'], ['0', '0', '0'], ['6', '5', '3']],
          # [['8', '7', '0'], ['9', '0', '2'], ['0', '1', '6']],
          # [['2', '0', '1'], ['5', '0', '3'], ['9', '0', '7']],
          # [['0', '9', '6'], ['1', '0', '7'], ['5', '2', '0']]]
          maps = [[['0', '5', '0'], ['0', '0', '0'], ['0', '9', '0']],
          [['0', '0', '7'], ['0', '0', '0'], ['0', '0', '0']],
          [['6', '0', '0'], ['4', '0', '2'], ['0', '0', '0']],
          [['0', '9', '0'], ['0', '0', '0'], ['3', '0', '5']],
          [['0', '0', '0'], ['8', '0', '1'], ['0', '0', '0']],
          [['0', '6', '2'], ['0', '0', '0'], ['0', '0', '1']],
          [['7', '0', '0'], ['1', '0', '8'], ['0', '4', '0']],
          [['3', '0', '0'], ['0', '0', '0'], ['0', '0', '0']],
          [['0', '0', '0'], ['6', '0', '0'], ['9', '8', '0']]]



     # board は 9*9 で与えることとする
     maps = [maps[i][0] + maps[i][1] + maps[i][2] for i in range(9)]


     # 初期boardの確認
     print('----- initial board -----')
     for x in maps:
          print(x)


     board = Board(maps)

     # 解くPART
     while(board.cnt < 81):
          board.check_cand()
          board.delete_candidate()
          board.check_cand_by_num()

          """ プリントしながら確認したいとき
          for y in board.candidates:
               print(y)

          print('------------------')
          for x in board.decided_places:
               print(x
          """


     # 最終MAPの表示
     print('----- final board -----')
     for x in board.decided_places:
          # print(''.join(x))
          print(x)

