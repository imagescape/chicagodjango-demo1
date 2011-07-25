def get_client_ip(request):
    """
    Given an http request, return a client ip address, remote ip address
    and forwarded ip address.
    
    Client IP = forwarded IP if it exists, otherwise the remote address
    Remote IP = The client IP address assuming it has not gone through proxy
    Forwarded IP = the client IP if it has gone through proxy. 
    """
    remote_ip = request.META.get('REMOTE_ADDR',"")
    forwarded_ip = request.META.get('HTTP_X_FORWARDED_FOR',"")
    client_ip = remote_ip if not forwarded_ip else forwarded_ip
    return (client_ip, remote_ip, forwarded_ip)

