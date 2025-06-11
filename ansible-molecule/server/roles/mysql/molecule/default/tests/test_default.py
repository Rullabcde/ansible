import os
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']
).get_hosts('all')


def test_mysql_is_installed(host):
    """Test that MySQL package is installed."""
    assert (
        host.package("mysql-server").is_installed
        or host.package("mariadb-server").is_installed
        or host.package("mysql").is_installed
    )


def test_mysql_service_running(host):
    """Test that MySQL service is running and enabled."""
    service_names = ["mysql", "mariadb"]
    for name in service_names:
        mysql_service = host.service(name)
        if mysql_service.is_enabled and mysql_service.is_running:
            break
    else:
        assert False, "MySQL/MariaDB service is not running and enabled"


def test_mysql_listening_on_port_3306(host):
    """Test that MySQL is listening on port 3306."""
    assert (
        host.socket("tcp://0.0.0.0:3306").is_listening
        or host.socket("tcp://:::3306").is_listening
        or host.socket("tcp://127.0.0.1:3306").is_listening
    )


def test_mysql_process_running(host):
    """Test that MySQL process is running."""
    mysql_processes = host.process.filter(comm="mysqld")
    assert len(mysql_processes) >= 1

