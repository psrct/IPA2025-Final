import subprocess, json

def run_ansible(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True)

        if 'failed=0' in result.stdout:
            print("Ansible successfully.")
            print(result.stdout)
            return "ok"
        else:
            print("Ansible failed.")
            print(result.stderr)
            return "Error: Ansible"
    except subprocess.CalledProcessError as e:
        print("Error running ansible-playbook command.")
        print(e.stderr)
        return "Error: Ansible"
    
def showrun(ip_address, student_id):
    filename = f"show_run_{student_id}_{ip_address}.txt"
    command = ['ansible-playbook', '-i', 'hosts.yaml', '--limit', ip_address, '-e', f'STUDENT_ID={student_id}', '-e', f'output_filename={filename}', 'show_run_playbook.yaml']
    return run_ansible(command)

def set_motd(ip_address, motd_text, student_id):
    motd_message = f"{motd_text}"
    command = [
        'ansible-playbook', '-i', 'hosts.yaml', '--limit', ip_address,
        '-e', json.dumps({"STUDENT_ID": student_id, "motd_message": motd_message}),
        'motd_playbook.yaml'
    ]
    result = run_ansible(command)
    return "Ok: success" if result == "ok" else result