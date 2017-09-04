#!/usr/bin/env python3
"""
The goTenna firmware images are encoded in a modified form of the
INTELHEX encoding which is used as the de facto standard encoding
for microprocessor and microcontroller code.

The goTenna images have the same record header format but all data
is serialized as raw bytes instead of being hex encoded. This is
presumably to reduce the number of bytes to transfer over the
relatively slow BlueTooth LE connection during firmware upgrades.
"""
import binascii
import io

import intelhex


def gotenna_to_intelhex(firmware_data):
    """
    Convert raw bytes in goTenna firmware to the hex encoded INTELHEX
    """
    firmware_bytes = bytearray(firmware_data)
    output_bytes = bytearray()

    while firmware_bytes:
        header_byte = firmware_bytes.pop(0)
        assert header_byte == 0x3a
        output_bytes.append(header_byte)

        # Read the rest of the record and hex encoded its data
        record_length = firmware_bytes.pop(0)
        record_bytes, firmware_bytes = firmware_bytes[:record_length+4], firmware_bytes[record_length+4:]
        record_bytes.insert(0, record_length)

        record_hex_bytes = bytearray(binascii.hexlify(record_bytes))
        output_bytes.extend(record_hex_bytes)

        record_end = firmware_bytes.pop(0)
        assert record_end == 0x0a
        output_bytes.append(record_end)

    return bytes(output_bytes)


def intelhex_to_raw(intelhex_data):
    # The intelhex library is broken with bytes, encoding data as string first
    intelhex_file = io.StringIO(intelhex_data.decode("utf-8"))
    ih = intelhex.IntelHex(intelhex_file)
    return ih


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Convert goTenna firmware file to raw binary image')
    parser.add_argument('firmware', metavar='FIRMWARE-FILE', type=str, help='Firmware file to convert')
    parser.add_argument('output', metavar='OUTPUT-FILE', type=str, help='Name of output firmware image')
    args = parser.parse_args()

    with open(args.firmware, "rb") as firmware_file:
        firmware_data = firmware_file.read()

    intelhex_format_firmware = gotenna_to_intelhex(firmware_data)
    ih = intelhex_to_raw(intelhex_format_firmware)
    ih.tobinfile(args.output)

    print("Wrote binary file {} containg {} segments".format(args.output, len(ih.segments())))
