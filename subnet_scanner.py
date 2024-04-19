import subprocess
import argparse
from os import geteuid


class Menu:
    def __init__(self, subnets_dict):
        self.subnets_dict = subnets_dict
        self.target = None
    def print_keys(self, items):
        for num, (key, value) in enumerate( items.items() ):
            print(num, key)

    def finder_key(self, items, num_target):
        for num, (key, value) in enumerate( items.items() ):
            if num_target == num:
                return key

    def select_subnet(self):
        while True:
            self.print_keys(self.subnets_dict)
            num = input("\nchoose subnet ")
            if num.isdigit():
                num = int(num)
                if num <= len(self.subnets_dict)-1:
                    break

        subnet_ip = self.finder_key(self.subnets_dict, num)

        return self.subnets_dict[subnet_ip]

    def select_target(self, targets_dict):
        while True:
            self.print_keys(targets_dict)
            num = input("\nchoose target: ")
            if num.isdigit():
                num = int(num)
                if num <= len(targets_dict)-1:
                    break

        self.target = self.finder_key(targets_dict, num)

        return self.target



def create_proc(args):
    try:
        print(" ".join(args))
        proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        error = proc.stderr.readline().decode()
        if error:
            print("error:", error)
            raise Exception(error)

        return proc

    except Exception as E:
        print(f"{E},    arguments: {args}")
        exit()


def get_ips(proc):
    ips = []
    for line in proc.stdout:
        line = line.decode().strip()

        if "Start" in line:
            continue

        if "|--" in line:
            ips.append(line.split()[1])

        print(line)

    return ips

def scan_subnet(ip):
    nmap_args = ["nmap", f"{ip}/24"]
    proc = create_proc(nmap_args)
    targets = {}
    last_ip = None

    for line in proc.stdout:
        line = line.decode()
        if "Nmap scan" in line:
            last_ip = line.split()[4]
            targets[ last_ip ] = []
            print("\n" + line, end="")

        elif ( last_ip ) and ( "tcp" and "/" in line ):
            targets[last_ip].append( line )
            print(line, end="")

    print("\n")
    return targets

def scan_target(target):
    proc = create_proc(["nmap", "-sV", "-O", target])
    for line in proc.stdout:
        line = line.decode()
        print(line, end="")

def menu(subnets):
    menu = Menu(subnets)
    while True:
        subnet_ip = menu.select_subnet()

        target = menu.select_target(subnet_ip)
        if target:
            scan_target(target)


def parse():
    parser = argparse.ArgumentParser(description=": ")
    parser.add_argument("-T", action="store_true", help="use TCP instead of ICMP echo")
    parser.add_argument("-m", type=str, help="maximum number of hops")
    parser.add_argument("ip", type=str, help="target ip")
    pars = parser.parse_args()

    return pars


def main():

    mtr_args = ["mtr", "-r"]

    args = parse()
    if geteuid() != 0:
        print("TCP/IP fingerprinting (for OS scan) requires root privileges. ")
    if args.T:
        mtr_args.append("-T")
    if args.m:
        mtr_args.extend(["-m", args.m])

    mtr_args.append(args.ip)
    proc = create_proc(mtr_args)
    ips = get_ips(proc)

    subnets = {}
    for num, ip in enumerate(ips):
        print(f"\n\n{num}. subnet")
        targets = scan_subnet(ip)
        subnets[ip] = targets

    menu(subnets)


if __name__ == "__main__":
    main()