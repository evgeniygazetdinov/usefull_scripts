import os
import sys
import subprocess

from threading import Thread


class RobotThread(Thread):
    def __init__(self, test_runner_server, python_bin, robot_home, storecraft_url, tests_path, args):
        super(RobotThread, self).__init__()
        self.exit_code = None
        cli_args = [python_bin, '-m', 'robot.run',
                    '-v sc_rst_mngr:http://{host}:{port}/do'.format(
                        host=test_runner_server.server_name,
                        port=test_runner_server.server_port
                    )]
        if '--run_one' in args:
            test_name = args[-2]
            test_path = args[-1]
            cli_args += ['-t', test_name, test_path]
            
        elif '--run_one_by_path' in args:
            test_path = args[-1]
            cli_args += ['-n noncritical', test_path]
            
        else:
            cli_args += args
            cli_args += ['-d',
                         os.path.join(robot_home, 'reports/'),
                         '-P',
                         robot_home,
                         os.path.abspath(tests_path)
                         ]
        env = os.environ.copy()
        env.update({'STORECRAFT_URL': storecraft_url})
        self.robot_process = subprocess.Popen(cli_args, stdout=sys.stdout, stderr=sys.stderr, env=env)
        self.test_runner_server = test_runner_server

    def run(self):
        self.exit_code = self.robot_process.wait()
        self.test_runner_server.shutdown()
