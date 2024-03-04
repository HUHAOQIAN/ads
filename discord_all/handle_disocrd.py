import json
import os.path
import re
import time


def is_dir(path):
    if not os.path.exists(path):
        with open(path, 'w') as f:
            json.dump([], f)





import json

def write_json():
    open_file = r"D:\code\python2\ads\discord_all\constants\2024\2024022801.txt"
    write_file = r"D:\code\python2\ads\discord_all\constants\2024\2024022801.json"
    discord_infos = []

    with open(open_file, "r") as f:
        datas = f.readlines()

    for data in datas:
        # Skip empty lines
        if not data.strip():
            continue

        # Split the line into parts
        parts = data.split(":")
        if len(parts) < 3:
            print(f"Skipping line due to incorrect format: {data}")
            continue

        # The email, password, and token are the last three parts
        email = parts[-3]
        password = parts[-2]
        token = parts[-1].strip()

        discord_info = {"discord": {"login": email, "password": password, "token": token}}
        discord_infos.append(discord_info)

    with open(write_file, "w") as f2:
        json.dump(discord_infos, f2, indent=4)




# def write_txt():
#     with open("constants/discord_infos.txt", "w") as f:
#         i = 0
#         while i < len(logins):
#             f.writelines(f'{logins[i]}-{passwords[i]}\n')
#
#             i += 1
def write_json2():
    open_file = "constants/ec881a-20230202.txt"
    write_file = "constants/ec881a-20230202.json"
    is_dir(write_file)  # 如果json不存在则创建
    with open(open_file, "r") as f:
        datas = f.read()
        logins = re.findall("login: (.*)", datas)
        passwords = re.findall("password: (.*)", datas)
        tokens = re.findall("TOKEN: (.*)", datas)
        print(logins[0])
    with open(write_file, "r") as f1:
        discord_infos = json.load(f1)

    i = 0
    while i < len(logins):
        discord_info = {"discord": {"login": logins[i], "password": passwords[i], "token": tokens[i]},
                        # "mail": {"login": mail_logins[i], "password": mail_passwords[i]}
                        }
        if discord_info not in discord_infos:
            discord_infos.append(discord_info)
        i += 1
    with open(write_file, "w") as f2:
        json.dump(discord_infos, f2)


def write_json3():
    open_file = "constants/ec881a-20230202.txt"
    write_file = "constants/ec881a-20230202.json"
    is_dir(write_file)
    with open(open_file, "r") as f:

        datas = f.readlines()
        for i in datas:
            print(i.split(":"))
    with open(write_file, "r") as f1:
        discord_infos = json.load(f1)
    # exit()
    i = 0
    while i < len(datas):
        datas_list = datas[i].split(":")
        print(len(datas_list))
        if len(datas_list) > 3:
            discord_info = {"discord": {"login": datas_list[5], "password": datas_list[6], "token": datas_list[9][:-1],
                                        "mailPassword": datas_list[8]},
                            # "mail": {"login": mail_logins[i], "password": mail_passwords[i]}
                            }
            if discord_info not in discord_infos:
                discord_infos.append(discord_info)
        i += 1
    with open(write_file, "w") as f2:
        json.dump(discord_infos, f2)


def write_tokens():
    open_file = r"D:\code\python2\ads\discord_all\constants\2024\2024022801.txt"
    write_file = r"D:\code\python2\ads\discord_all\constants\2024\tokens.txt"

    with open(open_file, "r") as f:
        datas = f.readlines()

    with open(write_file, "w") as f2:
        for data in datas:
            # Skip empty lines
            if not data.strip():
                continue

            # Split the line into parts
            parts = data.split(":")
            if len(parts) < 3:
                print(f"Skipping line due to incorrect format: {data}")
                continue

            # The token is the last part
            token = parts[-1].strip()

            # Write the token to the new file
            f2.write(token + "\n")

write_tokens()

