import atexit
import pychromecast
import time
from argparse import ArgumentParser
from signal import signal, SIGINT
from sys import exit
from radio_media import RadioMedia

class AlarmCasterException(Exception):
    pass

def signal_handler(signal_received, frame):
    if signal_received == SIGINT:
        print('SIGINT caught, exiting...')
        exit(0)

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('-d', '--device',   type=str, help='Friendly name of chromecast device')
    parser.add_argument('-n', '--minutes',  type=int, default=5, help='Casting duration')
    parser.add_argument('-c', '--channel',  type=str, help='Channel name')
    parser.add_argument('--list-channels',  action='store_true', help='List available radio channels')
    parser.add_argument('--list-devices',   action='store_true', help='List available chromecast devices')

    return parser.parse_args()

def chromecast_get(name):
    chromecasts = pychromecast.get_chromecasts()
    try:
        (cast,) = [cc for cc in chromecasts if name == cc.device.friendly_name]
        cast.wait()
        return cast
    except ValueError:
        raise AlarmCasterException('Could not find chromecast device "%s"', name)

def list_chromecast_devices():
    chromecasts = pychromecast.get_chromecasts()

    if chromecasts:
        print('Chromecast devices found:')
        print('')

    for device in chromecasts:
        print(f'* {device.device.friendly_name} ({device.device.model_name})')

def find_chromecast_device():
    chromecasts = pychromecast.get_chromecasts()

    if not chromecasts:
        raise AlarmCasterException('No chromecast device found on the network')
    elif len(chromecasts) != 1:
        print('Multiple chromecast devices found, please select one:')
        print('')
        for chromecast in chromecasts:
            print(f'* {chromecast.device.friendly_name} ({chromecast.device.model_name})')

        print('')
        print(f'Example: python {__file__} --device {chromecasts[0].device.friendly_name}')
        exit(1)
    else:
        (cast,) = chromecasts
        cast.wait()
        return cast

class StatusListener(object):
    def new_media_status(self, status):
        print('*** Status listener ***')
        print(status)

def main():
    signal(SIGINT, signal_handler)
    args = parse_args()

    if args.list_channels or not args.channel:
        RadioMedia.list_available_channels()
        return
    if args.list_devices:
        list_chromecast_devices()
        return

    if args.device:
        c = chromecast_get(args.device)
    else:
        c = find_chromecast_device()

    mc = c.media_controller
    mc.register_status_listener(StatusListener())

    channel = RadioMedia.get_channel(args.channel)
    if not channel:
        print(f'Channel "{args.channel}" not found')
        exit(1)

    mc.play_media(channel.url, channel.content_type, title=channel.name)
    mc.block_until_active()
    atexit.register(lambda mc: mc.stop(), mc)

    time.sleep(60 * args.minutes)

if __name__ == '__main__':
    main()
