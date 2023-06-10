# Read data from a DHT-11 sensor connected to your raspberry pi via HTTP

## Example output
`curl http://localhost:8001`
```
{
    "tempC": 23.8, 
    "humidity": 0.61, 
    "readAt": "2023-06-10T10:47:56.651335"
}
```

## Setup on rapsberry pi
1. install python + pip
   * `apt install python3 python3-pip`
   * `python3 -m pip install -r requirements.txt`
2. clone this repo in home directory (`/home/pi/dht11-pi-py/`) 
3. setup + start systemd service
   * `cp dht11-pi-py.service /etc/systemd/system/dht11-pi-py.service`
   * `systemctl enable dht11-pi-py.service`
   * `systemctl start dht11-pi-py.service`




