# ERDI laser rangefinder ROS 2 examples (RViz, launch files, filters)

Datasheets and public prices are on the [LRF22VB page](https://erdilrf.com/models/lrf22vb/?utm_source=github&utm_medium=readme&utm_campaign=erdi-lrf-ros2-examples) and in the [full ERDI laser rangefinder model list](https://erdilrf.com/models/?utm_source=github&utm_medium=readme&utm_campaign=erdi-lrf-ros2-examples).

Ready-to-run **ROS 2 examples for ERDI 905 nm laser rangefinder modules**: launch files, an **RViz2 `sensor_msgs/Range` display**, a **median and slew-rate filter node**, a **hardware-free demo** (synthetic range publisher) and a two-sensor namespace launch. It sits on top of the [`erdi_lrf_driver`](https://github.com/ErdiTech/erdi-lrf-drivers/tree/main/ros2/erdi_lrf_driver) driver package, which publishes `sensor_msgs/Range` for **LRF22VB, LRF50VB, LRF50H-LRF1500H, LR1000E2 ... LR2000E4, LRF1200A1, LRF3000A1 and SPD1200N\*** modules. Use it as a starting point for a **ROS 2 laser distance sensor** on a robot, AGV, drone companion computer or test bench.

## Build

```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
git clone https://github.com/ErdiTech/erdi_lrf_driver.git
git clone https://github.com/ErdiTech/erdi-lrf-ros2-examples.git
sudo apt install python3-serial
cd ~/ros2_ws && colcon build --packages-select erdi_lrf_driver erdi_lrf_examples
source install/setup.bash
```

## Run

```bash
# no hardware: synthetic sine wave -> filter -> RViz
ros2 launch erdi_lrf_examples demo_fake_rviz.launch.py

# real module (LRF22VB: millimetre stream at 460800 baud)
ros2 launch erdi_lrf_examples lrf22vb_rviz.launch.py port:=/dev/ttyUSB0

# two sensors, namespaced /front/range and /down/range
ros2 launch erdi_lrf_examples dual_lrf.launch.py
```

| Launch file | What it starts |
|---|---|
| `demo_fake_rviz.launch.py` | `fake_range_node`, `range_filter_node`, static TF, RViz2 |
| `lrf22vb_rviz.launch.py` | `erdi_lrf_driver range_node` + filter + RViz2 |
| `dual_lrf.launch.py` | two `range_node` instances in `front` and `down` namespaces |

Topics: `range` (`sensor_msgs/Range`, raw), `range_filtered` (median of slew-limited samples). Parameters are in [`config/`](config); the driver reads the unit per model (H series centimetres, VB series millimetres, family A metres x 10), so always set the exact `model`.

## Notes

- The pure-Python filters ([`filters.py`](erdi_lrf_examples/filters.py)) and the file syntax of the launch, YAML and RViz files are tested in CI without ROS: `python -m pytest -q test`.
- The nodes and launch files have **not been run in a ROS 2 environment by the maintainers yet**; bench reports and pull requests are welcome. Publishing `Range` does not make a module a PX4 / ArduPilot rangefinder: see [flight-controller integration](https://github.com/ErdiTech/erdi-lrf-drivers/blob/main/docs/flight-controller-integration.md) and [erdi-lrf-pixhawk-ardupilot](https://github.com/ErdiTech/erdi-lrf-pixhawk-ardupilot).
- Module pages and datasheets: <https://erdilrf.com/models/?utm_source=github&utm_medium=readme&utm_campaign=erdi-lrf-ros2-examples>.

## Related projects

- [ErdiTech/erdi-lrf-drivers](https://github.com/ErdiTech/erdi-lrf-drivers): Python, Arduino and ROS 2 drivers
- [erdi-lrf-raspberry-pi-python](https://github.com/ErdiTech/erdi-lrf-raspberry-pi-python): Raspberry Pi logger, MQTT and MAVLink bridge
- [laser-rangefinder-module-database](https://github.com/ErdiTech/laser-rangefinder-module-database): dataset of laser rangefinder modules

## License

MIT — see [LICENSE](LICENSE).
