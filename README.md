# subnet_scanner
Conducts a trace to a specific target and scans all hosts along the way. You can then select a specific scan target for the service version and operating system.

Делает трассировку до определенной цели и сканирует все хосты по пути. Затем можно выбрать цель для конкретного сканирования на версию служб и операционных систем.

###requirements требования: mtr-tiny, nmap
~~~bash
sudo apt install mtr-tiny nmap
~~~
###USAGE:
~~~bash
usage: subnet_scanner.py [-h] [-T] [-m M] ip

positional arguments:
  ip          target ip

options:
  -h, --help  show this help message and exit
  -T          use TCP instead of ICMP echo
  -m M        maximum number of hops


sudo python3 subnet_scanner.py -m 3 1.1.1.1
~~~
![subnets](https://github.com/podsashe4nik/subnet_scanner/blob/main/subnets.drawio.png)
