import subprocess

STUDENT_ID = "66070191"

def showrun():
    command = ['ansible-playbook', '-i', 'hosts.yaml', '-e', f'STUDENT_ID={STUDENT_ID}', 'newplaybook.yaml']
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        if 'failed=0' in result.stdout:
            print("Ansible successfully.")
            return "ok"
        else:
            print("Ansible failed.")
            print(result.stderr)
            return "Error: Ansible"
            
    except subprocess.CalledProcessError as e:
        print("Error running ansible-playbook command.")
        print(e.stderr)
        return "Error: Ansible"