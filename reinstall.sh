#! /bin/bash
pip3.9 uninstall -y appbuilder-sdk
python3.9 setup.py bdist_wheel
pip3.9 install dist/appbuilder_sdk-0.9.8.3-py3-none-any.whl