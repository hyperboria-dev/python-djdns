from __future__ import print_function

from pymads.server import DnsServer
from pymads.chain  import Chain

from djdns.source import DJSource
from djdns.loaders.disk import DiskLoader

class DJServer(DnsServer):
    '''
    Serve DJDNS data via DNS.

    >>> from pymads.tests.dig import dig
    >>> from threading import Thread

    >>> port = 8988
    >>> server = DJServer(listen_port=port)
    >>> thread = Thread(target=server.serve)
    >>> thread.start()

    >>> host_data = dig('in.root.demo', 'localhost', port)
    >>> success_text = "ANSWER SECTION:\\n%s.\\t\\t1800\\tIN\\tA\\t%s\\n\\n" % (
    ...     'in.root.demo',
    ...     '1.2.3.4',
    ... )

    >>> success_text in host_data
    True

    >>> server.stop()
    >>> thread.join()
    '''
    def __init__(self, **config):
        if 'path' in config:
            self.path = config['path']
        else:
            self.path = 'diskdemo/root.json'

        root = DiskLoader(self.path)
        self.source = DJSource(root, DiskLoader)
        self.chain = Chain([self.source])
        config['chains'] = [self.chain]
        DnsServer.__init__(self, **config)

def serve_standalone():
    server = DJServer(listen_port=8989)
    server.serve()

if __name__ == '__main__':
    serve_standalone()
