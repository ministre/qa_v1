from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import socket


@login_required
def sip_invite(request):
    if request.method == 'POST':
        message = 'INVITE sip:user1110000000350@whatever.com SIP/2.0\r\nTo: <sip:user4110000000350@whatever.com>\r\nFrom: sip:user9990000000000@rider.com;tag=R400_BAD_REQUEST;taag=4488.1908442942.0\r\nP-Served-User: sip:user4110000000350@whatever.com\r\nCall-ID: 00000000-00001188-71C0873E-0@10.44.40.47\r\nCSeq: 1 INVITE\r\nContact: sip:user9990000000000@rider.com\r\nMax-Forwards: 70\r\nVia: SIP/2.0/TCP 10.44.40.47;branch=z9hG4bK1908442942.4488.0\r\nContent-Length: 10\r\n\r\nRandomText'
        d_ip = request.POST['d_ip']
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(message.encode(), (d_ip, 5060))
        return render(request, 'sip_invite/sip_invite.html', {'message': message})
    else:
        return render(request, 'sip_invite/sip_invite.html')
