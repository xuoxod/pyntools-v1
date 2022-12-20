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
    "s": SYN_FLAG,
    "a": ACK_FLAG,
    "r": RST_FLAG,
    "d": D_FLAG,
    "f": FIN_FLAG,
    "df": D_FIN_FLAG,
    "ar": ACK_RST_FLAG,
    "sa": SYN_ACK_FLAG,
}
