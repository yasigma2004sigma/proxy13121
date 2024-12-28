import os
import random
import string

def generate_random_string(length):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

def get_password():
    try:
        return input("Type your password here: ")
    except:
        return input("Type your password here: ")

def setup_dante(username, password_proxy):
    os.system("apt-get update")
    os.system("apt-get -y install build-essential libwrap0-dev libpam0g-dev libkrb5-dev libsasl2-dev")
    os.system("wget --no-check-certificate https://ahmetshin.com/static/dante.tgz")
    os.system("tar -xvpzf dante.tgz")
    os.system("mkdir -p /home/dante")
    os.system("""cd dante && ./configure --prefix=/home/dante && make && make install""")
    os.system("""echo '
    logoutput: syslog /var/log/danted.log
    internal: eth0 port = 1080
    external: eth0

    socksmethod: username
    user.privileged: root
    user.unprivileged: nobody

    client pass {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        log: error
    }

    socks pass {
        from: 0.0.0.0/0 to: 0.0.0.0/0
        command: connect
        log: error
        method: username
    }' > /home/dante/danted.conf""")
    os.system("useradd --shell /usr/sbin/nologin -m {}".format(username))
    os.system('echo "{}:{}" | chpasswd'.format(username, password_proxy))
    os.system("apt-get -y install ufw")
    os.system("ufw allow ssh")
    os.system("ufw allow proto tcp from any to any port 1080")
    os.system("ufw enable")

def main():
    username = generate_random_string(12)  # Генерация логина длиной 12 символов
    password_proxy = get_password()
    setup_dante(username, password_proxy)
    print("Proxy installation success")
    print("\n________________________________\n")
    print(f"YOUR IP ADDRESS: {os.popen('hostname -I').read().split()[0]}")
    print(f"PORT: 1080")
    print(f"LOGIN: {username}")
    print(f"PASSWORD: {password_proxy}")

if __name__ == "__main__":
    main()
