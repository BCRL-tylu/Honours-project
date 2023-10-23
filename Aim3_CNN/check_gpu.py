import nvidia_smi
import json
import wmi

controllers = wmi.WMI().Win32_VideoController()
_GPU = False
_NUMBER_OF_GPU = 0

gpu_data = list()

for controller in controllers:
   controller_info = {
        'Name': controller.wmi_property('Name').value
    }
   gpu_data.append(controller_info)

print json.dumps(gpu_data, indent=4)


def _check_gpu():
    global _GPU
    global _NUMBER_OF_GPU
    nvidia_smi.nvmlInit()
    _NUMBER_OF_GPU = nvidia_smi.nvmlDeviceGetCount()
    if _NUMBER_OF_GPU > 0:
        _GPU = True

def _print_gpu_usage(detailed=False):

    if not detailed:
        for i in range(_NUMBER_OF_GPU):
            handle = nvidia_smi.nvmlDeviceGetHandleByIndex(i)
            info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)
            print(f'GPU-{i}: GPU-Memory: {_bytes_to_megabytes(info.used)}/{_bytes_to_megabytes(info.total)} MB')

def _bytes_to_megabytes(bytes):
    return round((bytes/1024)/1024,2)

if __name__ == '__main__':
    print('Checking for Nvidia GPU\n')
    _check_gpu()
    if _GPU:
        _print_gpu_usage()
    else:
        print("No GPU found.")