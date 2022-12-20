TCP_SYN_FLAG = "SYN"
TCP_ACK_FLAG = "ACK"
TCP_RST_FLAG = "RST"
TCP_PSH_FLAG = "PSH"
TCP_URG_FLAG = "URG"
TCP_FIN_FLAG = "FIN"
D_FLAG = "D"

ACK_RST_FLAG = "AR"
SYN_ACK_FLAG = "SA"
D_FIN_FLAG = "DF"

FLAGS = {
    "syn": TCP_SYN_FLAG,
    "ack": TCP_ACK_FLAG,
    "rst": TCP_RST_FLAG,
    "psh": TCP_PSH_FLAG,
    "urg": TCP_URG_FLAG,
    "fin": TCP_FIN_FLAG,
    "d": D_FLAG,
    "ackrst": ACK_RST_FLAG,
    "synack": SYN_ACK_FLAG,
    "dfin": D_FIN_FLAG,
}
