from apps.custom_modules.FileDialog import open_file as of


def open_file():
    file = of()

    if file:
        with open(file, "r") as f:
            for line in f.readlines():
                line_split = line.split(",")
                ip = line_split[0].strip()
                mac = line_split[1].strip()
                print("IP    {}\t\t\tMAC {}".format(ip, mac))
