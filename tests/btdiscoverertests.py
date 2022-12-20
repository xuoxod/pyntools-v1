from apps.custom_modules.BtDiscoverer import (
    enable_discovery_mode as edm,
    start_sniff as ss,
    disable_discovery_mode as ddm,
    collect_advertising_reports as car,
)


bt = edm()

print("Bluetooth Object: {}\n".format(bt) + "-" * 100 + "\n")

adverts = ss(bt)

print("Advertises: {}\n".format(adverts) + "-" * 100 + "\n")

bt = ddm()

print("Bluetooth Object: {}\n".format(bt) + "-" * 100 + "\n")

pkts, devs, rpts = car(adverts)

print(
    "Packets: {}\nDevices: {}\nReports: {}\n".format(pkts, devs, rpts)
    + "-" * 100
    + "\n"
)

-----------------------------------


from apps.custom_modules.BtDiscoverer import (
    send_receive as senrec,
    send_receive2 as senrec2,
    start_sniff as ss,
)

ans, unans, bt = senrec()

# print("{}\n{}\n".format(ans.summary(), ans.show()))

ans, unans = senrec2(bt)

# print("Ans: {}".format(ans))

adv = ss(bt)

# print("Adv: {}\nSniffed: {}".format(adv, dir(adv)))

# print(adv.summary())

# print(adv.show())

# print(adv.sr())

print("\nSR: {}".format(adv.sr()[0]))

print("\nStats: {}".format(adv.stats))

# res = adv.res


# for r in res:
#     print("{}\n".format(r))
