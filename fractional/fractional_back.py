import winrm


def execute_winrm_command(hostname, callback):
    username = "user"
    password = "pass"
    protocol = None
    shell_id = None

    try:
        protocol = winrm.Protocol(
            endpoint='http://' + hostname + ':5985/wsman',
            transport='ntlm',
            username=username,
            password=password
        )
        shell_id = protocol.open_shell()

        command_get_disk_info = "wmic diskdrive get Model, SerialNumber"
        command_get_install_date = "wmic os get installdate"

        get_model_number = protocol.run_command(shell_id, command_get_disk_info)
        get_install_date = protocol.run_command(shell_id, command_get_install_date)

        disk_info = protocol.get_command_output(shell_id, get_model_number)[0]
        disk_info = disk_info.decode()
        install_date = protocol.get_command_output(shell_id, get_install_date)[0]
        install_date = install_date.decode()

        protocol.cleanup_command(shell_id, get_model_number)
        protocol.cleanup_command(shell_id, get_install_date)
        protocol.close_shell(shell_id)

        callback(disk_info + '\n' + install_date)

    except Exception as e:
        callback("Ошибка: " + str(e))


def save_file(hostname, directory, result):
    with open(f"{directory}/{hostname}.txt", 'w') as f:
        f.write(result)
    with open(f"{directory}/{hostname}.csv", 'w') as f:
        f.write(result)

