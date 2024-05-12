from typing import List, Optional, Callable
from obspy.clients.seedlink.easyseedlink import EasySeedLinkClient
from obspy.core.trace import Trace
from obspy.core.stream import Stream
from xml.dom.minidom import parseString

from lib.interactions.fdsn import FDSNClient
from lib.interactions.entities import GeoserviceStream, LoadedStream

class IrisClient(EasySeedLinkClient):
    def __init__(self,
                data_callback: Optional[Callable] = None):
        super().__init__('rtserve.iris.washington.edu:18000')
        self.httpclient = FDSNClient('IRIS')
        
        self.channels = []

        self.data_callback = data_callback
        if not self.data_callback:
            self.data_callback = self.default_data_callback

    def default_data_callback(self, stream: Stream):
        print(f'Received iris edu trace from logger:\n{stream}\n')

    def on_data(self, trace: Trace):
        self.data_callback(Stream(traces=[trace]))
    
    def select_stream(self, net, station, selector=None):
        self.channels.append(LoadedStream(net, station, selector))
        super().select_stream(net, station, selector)

    def scrap(self, left_time: str, right_time: str) -> List[Stream]:
        res = []
        for channel in self.channels:
            stream = self.httpclient.timeseries(channel.network,
                                                channel.station,
                                                left_time,
                                                right_time
                                                )
            res.append(stream)
        return res

    def get_streams(self) -> List[GeoserviceStream]:
        raw_data = self.get_info('STREAMS')

        res = []
        doc = parseString(raw_data)
        stations = doc.getElementsByTagName('station')
        for station in stations:
            res.append(GeoserviceStream(network=station.getAttribute('network'), station=station.getAttribute('name')))
        return res