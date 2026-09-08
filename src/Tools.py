import os
import subprocess


class Tools:
    def __init__(self):
        pass

    def execute_command(self, cmd):
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=True
            )
            print(result.stdout)
            return result
        except subprocess.CalledProcessError as e:
            print(e.stdout)
            return None

    def reload(self):
        cmd = ["sudo", "systemctl", "reload", "nginx"]
        self.execute_command(cmd)

    def enable_site(self, config, available_path, enabled_path):
        target = os.path.join(available_path, config)
        link = os.path.join(enabled_path, config)

        if not os.path.isfile(target):
            print("No such file or directory")
            return

        try:
            os.symlink(target, link)
            result = self.config_check()
            if result is None or result.returncode != 0:
                os.unlink(link)
                print(f"Error in configuration. Rolled back {config}.")
                print("-" * 20)
                if result is not None:
                    print(result.stdout)
                return
            self.reload()
            print(f"Successfully enabled and reloaded nginx config {config}")
        except FileExistsError:
            print(f"Directory {link} already exists")
        except PermissionError:
            print(f"Permission denied")

    def disable_site(self, config, enabled_path):
        link = os.path.join(enabled_path, config)

        try:
            os.unlink(link)
            result = self.config_check()
            if result is None or result.returncode != 0:
                print(f"Error in configuration {config} reload canceled.")
                print("-" * 20)
                if result is not None:
                    print(result.stdout)
                return
            self.reload()
            print(f"Successfully disabled and reloaded nginx config {config}")
        except FileNotFoundError:
            print(f"Directory {link} does not exist")
        except PermissionError:
            print(f"Permission denied")


    def config_check(self):
        print("Testing configs...")
        cmd = ["sudo", "nginx", "-t"]
        result = self.execute_command(cmd)
        return result
