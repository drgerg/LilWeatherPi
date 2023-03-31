#!/usr/bin/env python3
#
# socketHost.py - on LilweatherPi
#
# Cobbled together by Greg Sanders 2020 to be handle interrogation of the ShopPi system.
#
import socket,os,sys,traceback,ast,logging,signal,configparser,pickle,wxStats
from time import sleep



def main():
    host = ''
    port = 64444
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lwpHome = os.path.abspath(os.path.dirname(__file__))
    try:
        s.bind((host, port))
    except socket.error as e:
        print(str(e))

    while True:
        try:
            s.listen(1)
            # print('Waiting for a connection.')
            conn, addr = s.accept()
            # print('connected to: '+addr[0]+':'+str(addr[1]))
            conn.send(str.encode('LilWeatherPi socketHost.py'))
        except Exception:
                traceback.print_exc(file=sys.stdout)
                incoming = 'An error was caught and displayed.'
                data = str.encode('It is time to part ways.')
                conn.sendall(data)
                pass

        while True:
            try:
                sockXferIn = conn.recv(2048)
                InCmd = pickle.loads(sockXferIn)
            except EOFError:
                logger.info("Encountered an empty .pkl file.  Moving on without it.")
                InCmd = 'break'
            #logger.info('InCmd variable was populated from sockXferIn: ' + str(InCmd))
            # print(str(InCmd))
##  BREAK
            if InCmd == 'break':
                pass
##  SEND ENVIRONMENTAL STATS
            if InCmd == 'LWPenvStats':
                # print('Received request for environmental stats.')
                wxStats.envStats()
                # sleep(2)
                lwpStats = (lwpHome + '/LilWPEnvStats.pkl')
                with open(lwpStats, 'rb') as lwps:
                    packet = lwps.read(4096)
                    conn.sendall(packet)
                # print("Sent LilweatherPi's environment stats.")
            try:
                conn.shutdown(1)
                conn.close()
                #logger.info('Connection from ' + str(addr[0]) + ' closed.')
                break
            # except Exception:
            #     traceback.print_exc(file=sys.stdout)
            #     incoming = 'An error was caught and displayed.'
            except OSError as oerror:
                logger.info("There was an error: {}".format(oerror))
                break
    #
        conn.close()
        # print("Connection closed.")
    else:
        # print('All Finished.')
        pass

def SignalHandler(signal, frame):
        logger.info("- - - - - - - - - - - Cleaning up - - - - - - - - - - - - - - - ")
        logger.info("Shutting down gracefully")
        logger.debug("This is SignalHandler")
        logger.info("Displayed .info and .debug in SignalHandler")
        logger.info("Shutdown initiated")
        logger.debug("Wrote to log in SignalHandler")
        sys.exit(0)


if __name__ == "__main__":
        try:
            import argparse
            ## Init area.  configparser and logger
            #
            sockHome = os.path.abspath(os.path.dirname(__file__))
            config = configparser.RawConfigParser()
            config.read(sockHome + '/sock.conf')
            logger = logging.getLogger(__name__)

            ## Command line arguments parsing
            #
            parsersm = argparse.ArgumentParser()
            parsersm.add_argument("-d", "--debug", help="Turn on debugging output to stderr", action="store_true")
            argssm = parsersm.parse_args()
            if argssm.debug:
                logging.basicConfig(filename=sockHome + '/sock.log', format='[%(name)s]:%(levelname)s: %(message)s. - %(asctime)s', datefmt='%D %H:%M:%S', level=logging.DEBUG)
                logging.info("Debugging output enabled")
            else:
                logging.basicConfig(filename=sockHome + '/sock.log', format='%(asctime)s - %(message)s.', datefmt='%a, %d %b %Y %H:%M:%S', level=logging.INFO)
            #
            ## End Command line arguments parsing
            logger.info(" - - - - - - - - - - - STARTING socketHost.py NORMALLY - - - - - - - - - - - - - - ")
            signal.signal(signal.SIGINT, SignalHandler)
            logger.debug("Top of try")
            main()
            logger.info("Bottom of try")

        except  ValueError as errVal:
            print(errVal)
            pass
        logger.info("That's all folks.  Goodbye")

