class RadioMedia(object):

    def __init__(self, name, url, content_type):
        self.name = name
        self.url = url
        self.content_type = content_type

    @staticmethod
    def list_available_channels():
        print('Available channels:')
        print('')

        for media in _channels:
            print(f'* {media.name}')

    @staticmethod
    def get_channel(name):
        try:
            return _channels[name]
        except KeyError:
            return None

_channels = {
        'NRK P1': RadioMedia('NRK P1', 'http://lyd.nrk.no/nrk_radio_p1_ostlandssendingen_aac_h', 'audio/aac'),
        'NRK P2': RadioMedia('NRK P2', 'http://lyd.nrk.no/nrk_radio_p2_aac_h', 'audio/aac'),
        'NRK P3': RadioMedia('NRK P3', 'http://lyd.nrk.no/nrk_radio_p3_aac_h', 'audio/aac'),
}

