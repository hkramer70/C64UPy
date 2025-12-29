import argparse
from C64UClient import Client

#
# Main entry point for the C64 Ultimate PRG uploader.
#
# Parses command-line arguments, creates a client, and attempts to run
# the specified PRG file on the C64 Ultimate device.
#

def main():
    parser = argparse.ArgumentParser(
        description="Kommuniziert mit dem Commodore64 Ultimate",
        add_help=False
    )

    parser.add_argument(
        "-h", "--h",
        action="help",
        help="Zeige diese Hilfe an"
    )

    parser.add_argument(
        "-runprg",
        metavar="<Pfad zum PRG File>",
        help="Überträgt zum und startet die PRG-Datei auf dem C64U"
    )

    args = parser.parse_args()
    client = Client()

    if args.runprg:
        success = client.runPrg(args.runprg)
        print("Done" if success else "Error")
    else:
        version = client.requestVersion()
        if version:
            print(f"REST-API Version: {version.version}")
        else:
            print("Error getting information from C64U")

if __name__ == "__main__":
    main()
