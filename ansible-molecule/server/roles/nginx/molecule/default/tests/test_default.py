import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_nginx_is_installed(host):
    """Test that nginx package is installed."""
    nginx = host.package("nginx")
    assert nginx.is_installed


def test_nginx_service_running(host):
    """Test that nginx service is running and enabled."""
    nginx = host.service("nginx")
    assert nginx.is_enabled
    assert nginx.is_running


def test_nginx_listening_on_port_80(host):
    """Test that nginx is listening on port 80."""
    socket = host.socket("tcp://0.0.0.0:80")
    assert socket.is_listening


def test_nginx_config_file_exists(host):
    """Test that nginx config file exists."""
    config_file = host.file("/etc/nginx/nginx.conf")
    assert config_file.exists
    assert config_file.is_file


def test_nginx_config_syntax(host):
    """Test that nginx configuration syntax is valid."""
    cmd = host.run("nginx -t")
    assert cmd.rc == 0


def test_nginx_process_running(host):
    """Test that nginx process is running."""
    nginx_process = host.process.get(comm="nginx")
    assert len(nginx_process) >= 1


def test_nginx_user_exists(host):
    """Test that nginx user exists."""
    user = host.user("nginx")
    assert user.exists


def test_default_page_accessible(host):
    """Test that default nginx page is accessible."""
    cmd = host.run("curl -f http://localhost/")
    assert cmd.rc == 0