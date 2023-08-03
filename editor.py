
class WebPFile :
    """
        A WebP File follows the RIFF format, so it consists entirely of chunks.

        Each chunk has a 4-byte ASCII identifier, a 4-byte little-endian length, a length-byte payload, and potentially a single pad byte if the length is odd.

        The RIFF chunk has a 4-byte ASCII identifier, followed by subchunks.

        An image consists of just one 'VP8 ' chunk,
    """
    
    def __init__ ( self, filepath ) :
        self.filepath = filepath
        with open(filepath, 'rb') as f:
            self.data = f.read()
        self.riff = self.parse_chunk_riff()

    def parse_chunk_riff ( self ) :
        riff = self.parse_chunk(0)
        if riff['identifier'] != b'RIFF' :
            raise Exception('Not a RIFF file')
        riff['type'] = riff['data'][:4]
        if riff['type'] != b'WEBP' :
            raise Exception('Not a WebP file')
        riff['subchunks'] = []
        offset = 12
        while offset < len(riff['data']) :
            subchunk = self.parse_chunk(offset)
            riff['subchunks'].append(subchunk)
            offset += 8 + subchunk['length'] + (subchunk['length'] % 2)
        return riff

    def parse_chunk ( self, offset ) :
        return {
            'identifier': self.data[offset:offset+4],
            'length': int.from_bytes(self.data[offset+4:offset+8], byteorder='little'),
            'data': self.data[offset+8:offset+8+int.from_bytes(self.data[offset+4:offset+8])],
        }

image = WebPFile('images/squareextract.webp')
print(image.riff['subchunks'][0]['length'])
for line in range(0, 64) :
    print(image.riff['subchunks'][0]['data'][line*64:line*64+64].hex())