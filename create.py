import os
import sys
from mail import get_users

try:
    from local_settings import PROJECT
except ImportError:
    PROJECT = ''


def get_template():
    with open('etc/template.sh', 'r') as f:
        return f.read().strip()


def get_keys(n):
    keys = []
    for i in range(n):
        os.system('ssh-keygen -P "" -f "tmpkey" -q')
        with open('tmpkey') as f:
            private = f.read().strip()
        with open('tmpkey.pub') as f:
            public_raw = f.read().strip().replace('\n', '')
            parts = public_raw.split(' ')
            public = ' '.join(parts[:-1] + ['user@cogito'])
        os.system('rm tmpkey tmpkey.pub')
        keys.append((private, public))
    return keys


def get_ips():
    os.system('gcloud compute instances list >> tmpips')
    with open('tmpips', 'r') as f:
        ips = f.read().strip()
    os.system('rm tmpips')
    items = [a.split() for a in ips.split('\n')[1:]]
    return [(a[0], a[4]) for a in items]


def generate_script_and_keys(n=3):
    if 'groups' in os.listdir('.'):
        return print('Please remove old "groups" folder before running this command')

    if len(get_users()) > n:
        return print('Please create more VMs than amount of users')

    template = get_template()
    keys = get_keys(n)
    command = ' & '.join(
        template % {'project': PROJECT, 'id': i + 1, 'user': 'user', 'key': keys[i][1]} for i in range(n))

    os.system('mkdir groups')
    for i, key in enumerate(keys):
        gid = i + 1
        os.system('mkdir groups/cogito-%r' % gid)
        with open('groups/cogito-%r/key-%r' % (gid, gid), 'w') as f:
            f.write(key[0])
        os.system('chmod 600 groups/cogito-%r/key-%r' % (gid, gid))

    os.system(command)

    for ip in get_ips():
        gid = ''.join([a for a in ip[0] if a.isnumeric()])
        os.system('touch groups/%s/%s' % ip)
        with open('groups/%s/ip.txt' % ip[0], 'w') as f:
            f.write(str(ip[1]))
        with open('groups/%s/ssh.sh' % ip[0], 'w') as f:
            f.write('ssh -i key-%s user@%s' % (gid, ip[1]))
        os.system('chmod +x groups/%s/ssh.sh' % ip[0])

    print('Successfully created %r instances' % n)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        try:
            generate_script_and_keys(int(sys.argv[1]))
        except ValueError:
            print('Invalid amount')
    else:
        generate_script_and_keys()
