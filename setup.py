from setuptools import setup

package_name = 'led_gesture_control'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    entry_points={
        'console_scripts': [
            'finger_detector = led_gesture_control.finger_detector_node:main',
            'led_controller = led_gesture_control.led_controller_node:main',
        ],
    },
)