import pychromecast
import time

p3_channel = ('http://lyd.nrk.no/nrk_radio_p3_mp3_h', 'audio/mp3')

def chromecast_get(name):
    chromecasts = pychromecast.get_chromecasts()
    (cast,) = [cc for cc in chromecasts if name == cc.device.friendly_name]
    return cast

def main():
    c = chromecast_get('Geneva')
    c.wait()

    print(c.device)
    print(c.status)

    mc = c.media_controller
    mc.play_media(*p3_channel)
    mc.block_until_active()

    print(mc.status)

    time.sleep(60 * 30)
    mc.stop()

if __name__ == '__main__':
    main()
