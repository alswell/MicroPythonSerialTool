# MicroPythonSerialTool
Use serial to manipulate file-system, GPIO etc. of MCU on which MicroPython is running

## usage
### help
```bash
python -m mpys.tool help
```
### examples
```bash
python -m mpys.tool ls
python -m mpys.tool cat /main.py
python -m mpys.tool mkdir mydir
python -m mpys.tool cp /local/dir/test.py /mydir
python -m mpys.tool rm /mydir
python -m mpys.tool pin 5 out 1
python -m mpys.tool pin 5 in
python -m mpys.tool pwm 5 1024 512
```
### use alias
```bash
alias MPYS='mpys_port=/dev/ttyUSB0 mpys_baud=115200 python -m mpys.tool'
MPYS ls
```