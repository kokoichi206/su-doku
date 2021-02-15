import requests
import urllib.request
import os
from bs4 import BeautifulSoup
import re


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

                    cand_trans = self.transpose(self.candidates)
                    det_trans = self.transpose(self.decided_places)
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


def scraping_all_problem():
     defo_url = "http://numberplace.net/" 
     # BeautifulSoupオブジェクト生成
     headers = {"User-Agent": "Mozilla/5.0"}
     ## これでurllib.error.HTTPErrorを解決できるかと思ったけど、無理でした。
     # headers = {"User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0"}


     probs = []
     # 毎日20問あるらしいので、その問題を全て取ってくる
     # b = soup.find_all("table", id='qlink')
     # print(b)
     for i in range(1, 21):
          url = defo_url + f'?no={i}'
          soup = BeautifulSoup(requests.get(
               url, headers=headers).content, 'html.parser')
          a = soup.find_all("script", type="text/javascript")
          str_html = str(a[0])  
          # print(str_html)
          prob = re.findall(r"var toi = '([\d]{81})'", str_html)
          
          # 後で扱いやすいように整形してからappend
          probs.append(cut_prob(prob[0]))
          
     return probs

def cut_prob(x: str):
     # 81桁の数字(str)を9*9に1文字ずつ分割し、
     # それぞれstrの2次元配列で保存
     tmp = []
     for i in range(9):
          tmp.append(list(x[9*i:9*i+9]))
     return tmp

def print_initial(x: list):
     for y in x:
          tmp = ['_' if y[i] == '0' else y[i] for i in range(9)]
          print(tmp)

if __name__ == '__main__':

     all_maps = scraping_all_problem()
     for i in range(20):
          maps = all_maps[i]
          # 初期boardの確認
          print(f'===== #{i+1} =====')
          print('----- initial board -----')
          print_initial(maps)


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
          print(board.cnt)

          # 最終MAPの表示
          print('----- final board -----')
          for x in board.decided_places:
               # print(''.join(x))
               print(x)

