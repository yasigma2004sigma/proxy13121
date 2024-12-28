import os

def main():
    username = "userproxy"
    try:
        password_proxy = input("Type your password here: ")
    except:
        password_proxy = input("Type your password here: ")

    os.system("sudo apt-get update")
    os.system("sudo apt-get -y install build-essential libwrap0-dev libpam0g-dev libkrb5-dev libsasl2-dev")
    os.system("wget --no-check-certificate https://ahmetshin.com/static/dante.tgz")
    os.system("tar -xvpzf dante.tgz")
    os.system("sudo apt-get -y install libwrap0 libwrap0-dev")
    os.system("sudo apt-get -y install gcc make")
    os.system("sudo mkdir -p /etc/danted")
    os.system("cd dante && ./configure --prefix=/etc/danted && make && sudo make install")
    os.system("""
        echo '
        logoutput: /var/log/danted.log
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
        }' > /etc/danted/danted.conf
    """)
    os.system(f"sudo useradd --shell /usr/sbin/nologin -m {username}")
    os.system(f'echo "{username}:{password_proxy}" | sudo chpasswd')
    os.system("sudo apt-get -y install ufw")
    os.system("sudo ufw allow ssh")
    os.system("sudo ufw allow from any to any port 1080 proto tcp")
    os.system("sudo ufw enable")
    os.system("sudo systemctl enable danted")
    os.system("sudo systemctl start danted")
    os.system("echo 'Proxy installation successful'")
    os.system(f"echo 'YOUR IP ADDRESS: `hostname -I | awk '{{print $1}}'`'")
    os.system("echo 'PORT: 1080'")
    os.system(f"echo 'LOGIN: {username}'")
    os.system(f"echo 'PASSWORD: {password_proxy}'")

if __name__ == "__main__":
    main()
