def test_nginx_package_installed(host):
    pkg = host.package("nginx")
    assert pkg.is_installed

def test_nginx_service_running(host):
    svc = host.service("nginx")
    assert svc.is_running
    assert svc.is_enabled

def test_nginx_listening_on_port_80(host):
    socket = host.socket("tcp://0.0.0.0:80")
    assert socket.is_listening
