def pkt_print(pkt=None):
    if not pkt == None:
        if pkt.haslayer(Dot11Beacon):
            print("Detected 802.11 Beacon Frame")
        elif pkt.haslayer(TCP):
            print("Detected 802.11 Probe Request Frame")
        elif pkt.haslayer(DNS):
            print("Detected a DNS packet")
        else:
            print("\nPacket:\t{}".format(pkt))
