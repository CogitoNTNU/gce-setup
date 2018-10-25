import smtplib
import os


def get_users():
    USERS_PATH = 'users.txt'
    try:
        with open(USERS_PATH, 'r') as f:
            return [a.strip() for a in f.read().strip().split('\n')]
    except FileNotFoundError:
        return []


def send_login():
    if not 'groups' in os.listdir('.'):
        return print('Please create VMs first')

    mails = []
    users = get_users()

    if len([a for a in os.listdir('groups') if a.startswith('cogito-')]) < len(users):
        return print('Please create VMs first')

    for i, user in enumerate(users):
        gid = i + 1
        with open('groups/cogito-%r/ip.txt' % gid, 'r') as f:
            ip = f.read().strip()
        with open('groups/cogito-%r/key-%r' % (gid, gid), 'r') as f:
            key = f.read().strip()
        message = \
"""\
Windows users:
  Follow instructions here: <TODO: link here>

Mac / Linux users:
  Open terminal
  Write 'nano key.txt' and press ENTER
  Copy the key below and paste it in the terminal window (including ---BEGIN--- and ---END--- lines)
  Press CTRL + X then Y then ENTER
  Write 'chmod 600 key.txt' and press ENTER
  Write 'ssh -i key.txt user@%s'

Start a jupyter notebook:
  Connect to the VM
  Write 'jupyter notebook --ip 0.0.0.0' and press ENTER
  Copy the url and replace '(...)' with '%s'
  Paste it in a web browser and press ENTER

VM: cogito-%r
IP: %s
KEY:
%s
""" % (ip, ip, gid, ip, key)
        mails.append((user, message))

    send_mails(mails)


def send_mails(mails):
    try:
        from local_settings import EMAIL_USERNAME, EMAIL_PASSWORD, EMAIL_HOST
    except ImportError:
        EMAIL_USERNAME = EMAIL_PASSWORD = ''
        EMAIL_HOST = 'smtp.gmail.com'

    server = smtplib.SMTP_SSL(EMAIL_HOST, 465)
    server.ehlo()
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

    for to, message in mails:
        server.sendmail(EMAIL_USERNAME, to,
"""\
From: Cogito NTNU
To: %s
Subject: Hackathon VM-information

%s
""" % (to, message))

    server.close()


if __name__ == '__main__':
    print('Participants:', ', '.join(get_users()))
    if input('Send mail to everyone? (y/n) ') == 'y':
        send_login()
        print('Mails sent!')
    else:
        print('Action aborted')
