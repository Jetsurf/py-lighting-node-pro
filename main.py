#!/usr/bin/python3

#import libs
import usb.core, usb.util, sys, time
#import modules
import controller

node = controller.Controller()

node.send_set_color_mode()

#R base address - send 16 bytes - each LED - per fan till 4th fan
fanr = bytearray(b'\x32\x00\x00\x32\x00')
#G base address - send 16 bytes - each LED - per fan till 4th fan
fang = bytearray(b'\x32\x00\x00\x32\x01')
#B bas addresss - send 16 bytes - each LED - per fan till 4th fan
fanb = bytearray(b'\x32\x00\x00\x32\x02')

cnt = 0
while cnt < 48:
	fanr, fang, fanb = node.make_color(fanr, fang, fanb)
	cnt+=1

node.send_packet(fanr)
node.send_packet(fang)
node.send_packet(fanb)

while True:
	node.send_packet(b'\x33\xff')
	time.sleep(1)