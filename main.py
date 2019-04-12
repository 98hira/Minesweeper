#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ver1.0.0

import os
import sys
import random
from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox as tkmsg

BOM_MAX     = 10
WIDTH_SIZE  = 9
HEIGHT_SIZE = 9
T_SIZE = (WIDTH_SIZE * HEIGHT_SIZE)
play_table = [0] * T_SIZE
mondai_table = [0] * T_SIZE
open_counter = T_SIZE - BOM_MAX
bom_list = []
bom_mark_count = BOM_MAX

# 0:プレイ中,1:ゲームオーバー, 2:ゲームクリア
state_type = {"GAME_PLAY":0, "GAME_OVER":1, "GAME_CLEAR":2}
game_state = state_type["GAME_PLAY"]

# アイコン画像格納用
icon_list = []
IMG_PATH = "img/"
icon_name = [f"{IMG_PATH}game_play.png",
             f"{IMG_PATH}game_over.png",
             f"{IMG_PATH}game_clear.png"]

TABLE_ID = {"MARK_BLANK":0,
			"MARK_FLAG":1,
			"MARK_QUESTION":2,
			"BOARD_BOM":3,
			"BOARD_0":4,
			"BOARD_1":5,
			"BOARD_2":6,
			"BOARD_3":7,
			"BOARD_4":8,
			"BOARD_5":9,
			"BOARD_6":10,
			"BOARD_7":11,
			"BOARD_8":12}
TABLE_DEBUG = "＊Ｐ？＠・１２３４５６７８９"
TABLE_TYPE = [{
				"name":"MARK_BLANK",
				"text":"",
				"background":"SystemButtonFace",
				"foreground":"SystemButtonFace"
			},{
				"name":"MARK_FLAG",
				"text":"Ｐ",
				"background":"SystemButtonFace",
				"foreground":"red"
			},{
				"name":"MARK_QUESTION",
				"text":"？",
				"background":"SystemButtonFace",
				"foreground":"blue"
			},{
				"name":"BOARD_BOM",
				"background":"red",
				"foreground":"white"
			},{
				"name":"BOARD_0",
				"text":"・",
				"background":"white",
				"foreground":"white"
			},{
				"name":"BOARD_1",
				"text":"１",
				"background":"white",
				"foreground":"green"
			},{
				"name":"BOARD_2",
				"text":"２",
				"background":"white",
				"foreground":"red"
			},{
				"name":"BOARD_3",
				"text":"３",
				"background":"white",
				"foreground":"blue"
			},{
				"name":"BOARD_4",
				"text":"４",
				"background":"white",
				"foreground":"purple"
			},{
				"name":"BOARD_5",
				"text":"５",
				"background":"white",
				"foreground":"purple"
			},{
				"name":"BOARD_6",
				"text":"６",
				"background":"white",
				"foreground":"purple"
			},{
				"name":"BOARD_7",
				"text":"７",
				"background":"white",
				"foreground":"purple"
			},{
				"name":"BOARD_8",
				"text":"８",
				"background":"white",
				"foreground":"purple"
			}]

# ボタン格納用
buttons = []

# 共通関数
def reverse(id):
	y = int(id / WIDTH_SIZE)
	x = int(id % WIDTH_SIZE)
	return x,y

def convert(x, y):
	global WIDTH_SIZE
	return (y * WIDTH_SIZE) + x


# ボードテーブル制御関数
def init_table():
	global mondai_table
	global play_table
	global TABLE_ID
	global open_counter
	global bom_list

	open_counter = T_SIZE - BOM_MAX

	# tableの初期化
	play_table = [0 for i in range(T_SIZE)]
	mondai_table = [0 for i in range(T_SIZE)]

	# 爆弾をランダムに配置
	bom_list = random.sample(range(0, T_SIZE), BOM_MAX)
	for i in bom_list:
		mondai_table[i] = TABLE_ID["BOARD_BOM"]

	# 爆弾情報を求める
	for x in range(0, WIDTH_SIZE):
		for y in range(0, HEIGHT_SIZE):
			bom_count = 0
			xy = convert(x, y)
			if (mondai_table[xy] == TABLE_ID["BOARD_BOM"]):
				continue
			# y,tを基準にした周囲8マスの爆弾の数をカウントする
			for nx in range(x-1, x+2):
				for ny in range(y-1, y+2):
					# チェック対象のマスが有効範囲である事の確認
					if ((nx >= 0) and (nx < WIDTH_SIZE) and
						(ny >= 0) and (ny < HEIGHT_SIZE)):
						if(mondai_table[convert(nx, ny)] == TABLE_ID["BOARD_BOM"]):
							bom_count += 1
			mondai_table[xy] = TABLE_ID["BOARD_%d"%(bom_count)]
	print_table(mondai_table)


def print_table(table):
	for y in range(0, HEIGHT_SIZE):
		for x in range(0, WIDTH_SIZE):
			temp = convert(x, y)
			print("%c"%(TABLE_DEBUG[table[temp]]), end="")
		print()
	print()


def open_cell(x, y, mark=False):
	global play_table, mondai_table
	global open_counter
	global bom_mark_count
	global game_state
	ret = 0

	# 引数チェック
	if ((x < 0) or (x >= WIDTH_SIZE) or
		(y < 0) or (y >= HEIGHT_SIZE)):
		return 0
	in_xy = convert(x, y)

	# 既に開かれているマスなら何もしない
	if ((play_table[in_xy] != TABLE_ID["MARK_BLANK"]) and
		(play_table[in_xy] != TABLE_ID["MARK_FLAG"]) and
		(play_table[in_xy] != TABLE_ID["MARK_QUESTION"])):
		return 0

	# 選択マスにマークを付ける
	if (mark):
		# 更新前のマークが爆弾フラグだった場合
		if (play_table[in_xy] == TABLE_ID["MARK_FLAG"]):
			bom_mark_count += 1

		# マーク情報更新
		play_table[in_xy] += 1
		if (play_table[in_xy] > TABLE_ID["MARK_QUESTION"]):
			play_table[in_xy] = TABLE_ID["MARK_BLANK"]

		# 更新後がマークが爆弾フラグだった場合
		if (play_table[in_xy] == TABLE_ID["MARK_FLAG"]):
			bom_mark_count -= 1

		L1_buff.set("bom count:%d"%(bom_mark_count))
		button_style_change(in_xy, play_table[in_xy])
		return

	# ボムマスを選択したか
	if (mondai_table[in_xy] == TABLE_ID["BOARD_BOM"]):
		game_state = state_type["GAME_OVER"]
		for bom_xy in bom_list:
			play_table[bom_xy] = mondai_table[bom_xy]
			button_style_change(bom_xy, play_table[bom_xy])
		return

	# 現在選択中のマスをopenする
	play_table[in_xy] = mondai_table[in_xy]
	button_style_change(in_xy, play_table[in_xy])
	open_counter -= 1
	if (open_counter <= 0):
		game_state = state_type["GAME_CLEAR"]

	# 空白マスを選択した場合
	if (mondai_table[in_xy] == TABLE_ID["BOARD_0"]):
		for nx in range(x-1, x+2):
			for ny in range(y-1, y+2):
				open_cell(nx, ny) # 再帰呼び出し


# GUI制御関数
# マスを左クリックした時
def button_click_left(event):
	global timer_stated
	global game_state

	if (game_state != state_type["GAME_PLAY"]):
		return

	id = buttons.index(event.widget)
	xy = reverse(id)
	# L1_buff.set("click left %d [%d,%d]"%(id,xy[0],xy[1]))
	open_cell(xy[0], xy[1], mark=False)

	if (game_state != state_type["GAME_PLAY"]):
		global play_button
		play_button["image"] = icon_list[game_state]
		timer_control(timer_state["stop"])


# マスを右クリックした時
def button_click_right(event):
	global game_state

	if (game_state != state_type["GAME_PLAY"]):
		return

	id = buttons.index(event.widget)
	# L1_buff.set("click right %d [%d,%d]"%(id,xy[0],xy[1]))
	open_cell(*reverse(id), mark=True)


# マスにマウスが入った時
def button_enter_mous(event):
	id = buttons.index(event.widget)
	# L1_buff.set("mous enter %d"%id)

	if (game_state == state_type["GAME_PLAY"]):
		if(check_cell(*reverse(id)) == 1):
			event.widget["bg"] = "yellow"


# マスからマウスが抜けた時
def button_leave_mous(event):
	id = buttons.index(event.widget)
	# L1_buff.set("mous leav %d"%id)

	is_mark = check_cell(*reverse(id))
	if(is_mark == 1):
		event.widget["bg"] = "SystemButtonFace"


# アイコンを左クリックした時
def play_button_click(event):
	global play_table
	global game_state
	global bom_mark_count

	game_state = state_type["GAME_PLAY"]
	timer_control(timer_state["reset"])
	init_table()

	# ボム情報の初期化
	bom_mark_count = BOM_MAX
	L1_buff.set("bom count:%d"%(bom_mark_count))

	# GUIのリセット処理
	for i in range(len(play_table)):
		button_style_change(i, play_table[i])
	event.widget["image"] = icon_list[game_state]

	timer_control(timer_state["start"])


def check_cell(x, y, isMark=True):
	global play_table

	# 引数チェック
	if ((x < 0) or (x >= WIDTH_SIZE) or
		(y < 0) or (y >= HEIGHT_SIZE)):
		return -1
	in_xy = convert(x, y)

	if (isMark):
		if ((play_table[in_xy] == TABLE_ID["MARK_BLANK"]) or
			(play_table[in_xy] == TABLE_ID["MARK_FLAG"]) or
			(play_table[in_xy] == TABLE_ID["MARK_QUESTION"])):
			return 1
		else:
			return 0
	else:
		return play_table[in_xy]


def button_style_change(id, type):
	for key, val in TABLE_TYPE[type].items():
		# print("key:{0} val:{1}".format(key,val))
		if (key != "name"):
			buttons[id][key] = val


# 時間計測用
timer_stated = False
timer_counter = 0
timer_state = {"start":0,"stop":1,"reset":2}
timer_id = 0
def timer_control(state):
	global timer_stated
	global timer_counter
	global timer_id
	if (state == timer_state["start"]):
		if (timer_stated == False):
			timer_stated = True
			timer_id = root.after(1000, timer_count)
	elif (state == timer_state["stop"]):
		if (timer_stated == True):
			timer_stated = False
	elif (state == timer_state["reset"]):
		root.after_cancel(timer_id)
		timer_counter = 0
		timer_stated = False
		L2_buff.set("%d"%timer_counter)


def timer_count():
	global timer_counter
	global timer_stated
	global timer_id
	if (timer_stated):
		timer_counter += 1
		L2_buff.set("%d"%timer_counter)
		timer_id = root.after(1000, timer_count)


if __name__ == "__main__":
	init_table()

	root = Tk()
	root.resizable(0,0)
	f0 = Frame(root)
	f1 = Frame(root)

	# 画像ファイルの読み込み
	for iname in icon_name:
		work = ImageTk.PhotoImage(Image.open(iname))
		icon_list.append(work)

	# ラベル生成
	L1_buff = StringVar()
	L1_buff.set("bom count:%d"%(bom_mark_count))
	L1_obj = Label(f0, textvariable=L1_buff, height=2, width=18)
	L1_obj["relief"] = GROOVE
	L1_obj.pack(side=LEFT)

	play_button = Label(f0, height=30, width=30)
	play_button["relief"] = GROOVE
	play_button["image"] = icon_list[game_state]
	play_button.bind("<Button-1>", play_button_click)
	play_button.pack(side=LEFT)

	L2_buff = StringVar()
	L2_buff.set("timer")
	L2_obj = Label(f0, textvariable=L2_buff, height=2, width=18)
	L2_obj["relief"] = GROOVE
	L2_obj.pack(side=LEFT)

	# ボタン生成
	for y in range(HEIGHT_SIZE):
		for x in range(WIDTH_SIZE):
			id = (y * HEIGHT_SIZE) + x
			button = Label(f1)
			button["text"] = ""
			button["width"] = 4
			button["height"] = 2
			button["relief"] = GROOVE
			button["background"] = "SystemButtonFace"
			button.grid(row=y, column=x)
			button.bind("<Button-1>", button_click_left)	#左クリック時
			button.bind("<Button-2>", button_click_right)	#右クリック時
			button.bind("<Enter>",    button_enter_mous)	#マウスポインターがwidgetに入った時
			button.bind("<Leave>",    button_leave_mous)	#マウスポインターがwidgetから出た時
			buttons.append(button)

	# フレームの配置
	f0.pack()
	f1.pack(fill=BOTH)

	timer_control(timer_state["start"])
	game_state = state_type["GAME_PLAY"]

	root.mainloop()
