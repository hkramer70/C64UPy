import argparse
from C64UClient import C64UClient

#
# Main entry point for the C64 Ultimate PRG uploader.
#
# Parses command-line arguments, creates a client, and attempts to run
# the specified PRG file on the C64 Ultimate device.
#

def main():
    parser = argparse.ArgumentParser(
        description="Sendet ein PRG an den C64 Ultimate und startet es"
    )

    parser.add_argument(
        "filename",
        help="Pfad zur PRG-Datei"
    )

    args = parser.parse_args()
    fname = args.filename

    client = C64UClient()
    success = client.runPrg(fname)

    print("Done" if success else "Error")

if __name__ == "__main__":
    main()
