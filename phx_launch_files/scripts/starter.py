import subprocess
import time


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def wait(seconds):
    print 'waiting', seconds, 'seconds'
    for i in range(seconds):
        print i,
        time.sleep(1)
    print 'finished'


while True:
    print 'select the node configuration:'
    print '  (1) - phx_basics'
    print '  (2) - phx_basics - phx_mapping'
    print '  (3) - phx_basics - phx_camera'
    print '  (4) - phx_basics - phx_camera - phx_mapping'
    print '  (end)'
    input = raw_input('>>> ')
    if input is '1':
        print 'starting ' + \
              bcolors.OKGREEN + 'roslaunch phx_launchfiles phx_basics.launch' + bcolors.ENDC
        launch_basic = subprocess.Popen(['roslaunch', 'phx_launch_files', 'phx_basics.launch'], stdout=subprocess.PIPE)
    elif input is '2':
        print 'starting ' + \
              bcolors.OKGREEN + 'roslaunch phx_launchfiles phx_basics.launch' + bcolors.ENDC
        launch_basic = subprocess.Popen(['roslaunch', 'phx_launch_files', 'phx_basics.launch'], stdout=subprocess.PIPE)
        print 'waiting for mapping startup'
        wait(15)
        print 'starting ' + \
              bcolors.OKGREEN + 'roslaunch phx_launchfiles phx_mapping.launch' + bcolors.ENDC
        launch_mapping = subprocess.Popen(['roslaunch', 'phx_launch_files', 'phx_mapping.launch'], stdout=subprocess.PIPE)
    elif input is '3':
        print 'starting ' + \
              bcolors.OKGREEN + 'roslaunch phx_launchfiles phx_basics.launch' + bcolors.ENDC
        launch_basic = subprocess.Popen(['roslaunch', 'phx_launch_files', 'phx_basics.launch'], stdout=subprocess.PIPE)
        wait(5)
        print 'starting ' + \
              bcolors.OKGREEN + 'roslaunch phx_launchfiles phx_camera.launch' + bcolors.ENDC
        launch_camera = subprocess.Popen(['roslaunch', 'phx_launch_files', 'phx_camera.launch'], stdout=subprocess.PIPE)
    elif input is '4':
        print 'starting ' + \
              bcolors.OKGREEN + 'roslaunch phx_launchfiles phx_basics.launch' + bcolors.ENDC
        launch_basic = subprocess.Popen(['roslaunch', 'phx_launch_files', 'phx_basics.launch'], stdout=subprocess.PIPE)
        print 'starting ' + \
              bcolors.OKGREEN + 'roslaunch phx_launchfiles phx_camera.launch' + bcolors.ENDC
        launch_camera = subprocess.Popen(['roslaunch', 'phx_launch_files', 'phx_camera.launch'], stdout=subprocess.PIPE)
        print 'waiting for mapping startup'
        wait(15)
        print 'starting ' + \
              bcolors.OKGREEN + 'roslaunch phx_launchfiles phx_mapping.launch' + bcolors.ENDC
        launch_mapping = subprocess.Popen(['roslaunch', 'phx_launch_files', 'phx_mapping.launch'], stdout=subprocess.PIPE)
    elif input == 'end':
        break
    else:
        'input was not useful.'
        input = '0'
    print 'startup done.\n\n'

    print 'press ctrl - C to stop roscore'
    while input is not '0':
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            if input is '1':
                launch_basic.terminate()
            elif input is '2':
                launch_basic.terminate()
                launch_mapping.terminate()
            elif input is '3':
                launch_basic.terminate()
                launch_camera.terminate()
            elif input is '4':
                launch_basic.terminate()
                launch_camera.terminate()
                launch_mapping.terminate()
            break
    print 'all launch files stopped'
