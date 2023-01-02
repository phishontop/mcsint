from mcsint.server import Server


with open("sites.txt") as file:
    sites = file.readlines()
    servers = [
        Server(site.replace("\n", ""))
        for site in sites
    ]

username = input("Enter username: ")
for server in servers:
    punishments = server.get_punishments(name=username)
    for punishment in punishments:
        print(punishment.reason)
        print(punishment.date)