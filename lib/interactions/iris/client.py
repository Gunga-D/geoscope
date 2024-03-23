from typing import List, Optional, Callable
from lib.interactions.iris.exception import IrisClientException
from lib.interactions.entities import Channel
from obspy.clients.seedlink.easyseedlink import EasySeedLinkClient

class IrisClient(EasySeedLinkClient):
    def __init__(self, host: str, port: str, channels: List[Channel], data_callback: Optional[Callable] = None):
        super().__init__(host + ':' + port)

        if len(channels) > 5:
            raise IrisClientException('The service iris edu limit the max concurrent connections, no more than 5')
        if len(channels) == 0:
            raise IrisClientException('At least one channel is required to connect the iris edu service')
        
        if not data_callback:
            self.data_callback = self.default_data_callback
            
        for channel in channels:
            super().select_stream(channel.network, channel.station, '???')

    def default_data_callback(self, trace):
        print('Received iris edu trace:')
        print(trace)

    def on_data(self, trace):
        self.data_callback(trace)