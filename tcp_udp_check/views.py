from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import socket


@login_required
def tcp_udp_check(request):
    if request.method == 'POST':
        s_port = int(request.POST['s_port'])
        e_port = int(request.POST['e_port'])
        d_ip = request.POST['d_ip']
        protocol = request.POST['protocol']
        result_messages = []
        if protocol == 'tcp':
            for tcp in range(s_port, e_port):
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect_ex((d_ip, tcp))
                message = "TCP, Dst Port: {} IPv4, Dst: {}".format(tcp, d_ip)
                result_messages.append(message)
            return render(request, 'tcp_udp_check/tcp_udp_check.html', {'result_messages': result_messages})
        if protocol == 'udp':
            for udp in range(s_port, e_port):
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.sendto("hello".encode(), (d_ip, udp))
                message = "UDP, Dst Port: {} IPv4, Dst: {}".format(udp, d_ip)
                result_messages.append(message)
            return render(request, 'tcp_udp_check/tcp_udp_check.html', {'result_messages': result_messages})
    else:
        return render(request, 'tcp_udp_check/tcp_udp_check.html')
