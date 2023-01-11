# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 16:09:05 2022

@author: user
"""


import random
import json
import os
path = os.getcwd()

filename = 'player'
ext = '.json'
filePathNameWExt = path + '\\'+filename + ext 
data = {'player' : 100} 
#print('原始籌碼:'+str(data)[11:14])

#存檔
def write_to_file(filename, data):
    with open(filename, 'w+') as json_file:
        json_file.write(json.dumps(data))
write_to_file(filename, data)        
#讀檔    
def read_to_file(filename):   
    with open('player.json') as json_file:    
        data = json.load(json_file)     
read_to_file('player.json')

#開始籌碼
def start_dollar():
    filename = 'player.json'
    read_to_file('player.json')
    with open(filename, 'w') as json_file:
        data['player'] = data['player'] 
    
        json.dump(data['player'], json_file)
        write_to_file(filename, data['player'])
    return data['player']

#start_dollar() 
print('開始遊戲，目前籌碼為:'+str(start_dollar()))

#輸錢
def loss_dollar():
    
    filename = 'player.json'
    read_to_file('player.json')
    with open(filename, 'w') as json_file:
        data['player'] = data['player'] - 10
    
        json.dump(data['player'], json_file)
        write_to_file(filename, data['player'])
    return data['player']

#loss_dollar() 
#print('籌碼為:'+str(loss_dollar()))

#贏錢
def win_dollar():
    filename = 'player.json'
    read_to_file('player.json')
    with open(filename, 'w') as json_file:
        data['player'] = data['player'] + 10
    
        json.dump(data['player'], json_file)
        write_to_file(filename, data['player'])
    return data['player']

#win_dollar()
#print('籌碼為:'+str(win_dollar()))

#這是一副牌
color = ['紅心','方塊','黑桃','梅花']
number = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
This_cards = []
for the_color in color:
    for the_number in number:
        This_cards.append(the_color +' '+the_number)
        random.shuffle(This_cards)
        
cards = []
for l in This_cards:    
    try:
        
        This_card_number = int((l[3:5]))
    except:
        
        if l[3:5]  == 'A':
            This_card_number = 11
        elif l[3:5]  == 'J' or 'Q' or 'K':
            This_card_number = 10
    cards.append(This_card_number)



#發牌
def deal_card():
    card = random.choice(cards)
    cards.remove(card)
    return card

#算牌
def calculate_points(cards):
    total_points = sum(cards)

    if len(cards) == 2:
        return total_points
    if total_points > 21:
        if 11 in cards:
            cards.remove(11)
            cards.append(1)
            total_points = sum(cards)

    return total_points

#玩牌
def play_blackjack():
    user_cards = []
    dealer_cards = []#空的牌

    for _ in range(2):
        user_cards.append(deal_card())
        dealer_cards.append(deal_card())

    print(f"玩家的牌：{user_cards}")
    print(f"莊家的明牌：{dealer_cards[1]}")
#玩家的牌
    ask_for_card = ""
    while ask_for_card != "2":
        ask_for_card = input("1.要牌、2.停牌，請輸入對應數字：")

        if ask_for_card == "1":
            user_cards.append(deal_card())
            user_points = calculate_points(user_cards)
            if user_points > 21:
                ask_for_card = "2"
            else:
                print(f"玩家的牌：{user_cards}")
        elif ask_for_card == "2":
            user_points = calculate_points(user_cards)
        else:
            print("請重新輸入！")

#莊家的牌
    dealer_points = calculate_points(dealer_cards)
    while dealer_points < 16:
        dealer_cards.append(deal_card())
        dealer_points = calculate_points(dealer_cards)

    
    print(f"玩家的牌：{user_cards}，共{user_points}點")
    print(f"莊家的牌：{dealer_cards}，共{dealer_points}點")

#計算點數
    if user_points > 21:
        print("沒收10點籌碼")
        loss_dollar() 
        print('籌碼為:'+str(loss_dollar()))
    elif dealer_points > 21:
        print("取得額外10點籌碼(共20點)")
        win_dollar()
        print('籌碼為:'+str(win_dollar()))
    elif user_points == dealer_points:
        print("退回籌碼")
    elif user_points > dealer_points:
        print("取得額外10點籌碼(共20點)")
        win_dollar()
        print('籌碼為:'+str(win_dollar()))
    else:
        print("沒收10點籌碼")
        #loss_dollar() 
        print('籌碼為:'+str(loss_dollar()))
#主程式
play_game = True
start_input = input(("1.要求洗牌、2.要求換一副新牌、3.發牌，請輸入對應數字："))
if start_input == '1':
    random.shuffle(cards)#應該是洗牌吧
    print("洗牌成功")
elif start_input == '2':
    This_cards = []
    for the_color in color:
        for the_number in number:
            This_cards.append(the_color +' '+the_number)
            random.shuffle(This_cards)
            
    cards = []
    for l in This_cards:    
        try:
            This_card_number = int((l[3:5]))
        except:
            if l[3:5]  == 'A':
                This_card_number = 11
            elif l[3:5]  == 'J' or 'Q' or 'K':
                This_card_number = 10
        cards.append(This_card_number)
    print("換牌成功")
elif start_input == '3':
    try:
        play_blackjack()
        #write_to_file('player.json', data)
        #read_to_file('player.json')
    except:
        This_cards = []
        for the_color in color:
            for the_number in number:
                This_cards.append(the_color +' '+the_number)
                random.shuffle(This_cards)
                
        cards = []
        for l in This_cards:    
            try:
                This_card_number = int((l[3:5]))
            except:
                if l[3:5]  == 'A':
                    This_card_number = 11
                elif l[3:5]  == 'J' or 'Q' or 'K':
                    This_card_number = 10
            cards.append(This_card_number)
        print('牌已發完，已重新換一副新牌')
        play_blackjack()
        #write_to_file('player.json', data)
        #read_to_file('player.json')
    
else:
    print('請重新輸入1 or 2 or 3!')

        

while play_game == True:
    print("=======================================")
    user_input = input("1.要求洗牌、2.要求換一副新牌、3.發牌，請輸入對應數字或輸入exit結束：")
    if user_input == '1':
        cards = random.shuffle(cards)
        print("洗牌成功")
    elif user_input == '2':
        This_cards = []
        for the_color in color:
            for the_number in number:
                This_cards.append(the_color +' '+the_number)
                random.shuffle(This_cards)
                
        cards = []
        for l in This_cards:    
            try:
                
                This_card_number = int((l[3:5]))
            except:
                
                if l[3:5]  == 'A':
                    This_card_number = 11
                elif l[3:5]  == 'J' or 'Q' or 'K':
                    This_card_number = 10
            cards.append(This_card_number)
        print("換牌成功")
    elif user_input == '3':
        try:
            play_blackjack()
            write_to_file('player.json', data)
            read_to_file('player.json')
        except:
            This_cards = []
            for the_color in color:
                for the_number in number:
                    This_cards.append(the_color +' '+the_number)
                    random.shuffle(This_cards)
                    
            cards = []
            for l in This_cards:    
                try:
                    This_card_number = int((l[3:5]))
                except:
                    if l[3:5]  == 'A':
                        This_card_number = 11
                    elif l[3:5]  == 'J' or 'Q' or 'K':
                        This_card_number = 10
                cards.append(This_card_number)
            print('牌已發完，已重新換一副新牌')
            #play_blackjack()
            write_to_file('player.json', data)
            read_to_file('player.json')
        
    elif user_input == "exit":
        play_game = False
        print("離開遊戲")
    else:
        print('請重新輸入1 or 2 or 3!')