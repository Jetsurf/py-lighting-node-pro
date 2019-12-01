import usb.core, usb.util, sys, time

class Controller():

	def __init__(self):
		self.nodeloc = None
		self.node = None
		self.cfg = None
		self.scan_for_node()
		self.setup_node()

	def scan_for_node(self):
		self.nodeloc = usb.core.find(idVendor=0x1b1c, idProduct=0x0c0b)

		if self.nodeloc is None:
			print("Error finding Lighting Node Pro, exiting")
			quit(0)
		else:
			print("Found Lighting Node Pro")

	def make_padded(self, packet):
		packet = bytearray(packet)
		while len(packet) < 64:
			packet.append(0)
		return packet

	def setup_node(self):
		print("Doing setup")
		self.nodeloc.reset()

		try:
			self.nodeloc.set_configuration()
			self.cfg = self.nodeloc.get_active_configuration()
			self.node = usb.util.find_descriptor(self.cfg[(0,0)], custom_match = lambda e: usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT)
		except Exception as e:
			exc = sys.exc_info()
			if exc[0] is usb.core.USBError:
				print('Error getting config/descriptor, are you running as root?')
				quit(1)

		print("Done")

	def send_packet(self, packet):
		#print("Sending: " + str(packet.decode('utf-8')))
		self.node.write(self.make_padded(packet))

	def make_color(self, rchan, bchan, gchan):
		rchan.append(25)
		gchan.append(0xA4)
		bchan.append(0xA4)
		return rchan, gchan, bchan

	def send_set_color_mode(self):
		self.send_packet(b'\x37')
		self.send_packet(b'\x35\x00\x00\x30\x00\x01\x01')
		self.send_packet(b'\x3b\x00\x01')
		self.send_packet(b'\x38\x00\x02')
		self.send_packet(b'\x34')
		self.send_packet(b'\x37\x01')
		self.send_packet(b'\x34\x01')
		self.send_packet(b'\x38\x01\x01')
		self.send_packet(b'\x33\xFF')