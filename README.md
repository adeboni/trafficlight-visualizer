# trafficlight-visualizer
Traffic Light Spectrograph using a Raspberry Pi

Prerequisites:
----------
Install WiringPi and AlsaAudio for Python

Add the user to the audio group

Usage:
----------
### Standalone Version:
```
sudo ./spectro.py <traffic light index>
```

### Networked Version:
#### On the master light:
```
./spectro-master.py &
sudo ./spectro-slave.py <traffic light index>
```

#### On each of the slave lights:
```
sudo ./spectro-slave.py <traffic light index>
```