import csv
import asyncio
import winrm

async def get_disk_info(hostname, output_folder):
    username = "user"
    password = "pass"
    try:
        protocol = winrm.Protocol(
            endpoint='http://' + hostname + ':5985/wsman',
            transport='ntlm',
            username=username,
            password=password
        )
        print(f"Connected to {hostname}")

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


        with open(f'{output_folder}/{hostname}.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Model', 'Serial Number'])
            writer.writerow(disk_info.split(', '))


        with open(f'{output_folder}/{hostname}.txt', 'w') as f:
            f.write(f"Disk Info:\n{disk_info}")
            f.write(f"{install_date}\n")


    except Exception as e:
        print(f"Error processing {hostname}: {e}")

def run(hosts_file, output_folder):
    with open(hosts_file, 'r') as f:
        hosts = f.readlines()

    hosts = [host.strip() for host in hosts]

    loop = asyncio.get_event_loop()
    tasks = []

    for host in hosts:
        task = loop.create_task(get_disk_info(host, output_folder))
        tasks.append(task)

    loop.run_until_complete(asyncio.wait(tasks))