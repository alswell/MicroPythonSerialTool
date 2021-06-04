from setuptools import setup, find_packages


setup(
       name="micropython-serial-tool",
       version="1.0.0",
       description="Use serial to manipulate file-system, GPIO etc. of MCU on which MicroPython is running",
       author="Ning Zhou",
       author_email="icemanzhouning@yeah.net",
       url="https://github.com/alswell/MicroPythonSerialTool",
       license="GPL",
       packages=find_packages(),
       )
