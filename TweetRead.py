import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import Stream
import socket
import json


# Set up your credentials
consumer_key    = ''
consumer_secret = ''
access_token    = ''
access_token_secret   = ''


class TweetListener(Stream):

  def __init__(self,*args, csocket):
    super().__init__(*args)
    self.client_socket = csocket


  def on_data(self, data):
      try:
          msg = json.loads( data )
          print(msg['text'].encode('utf-8'))
          self.client_socket.send( msg['text'].encode('utf-8'))
          return True
      except BaseException as e:
          print("Error on_data: %s" % str(e))
      return True

  def on_error(self, status):
      print(status)
      return True

def send_data(c_socket):
  twtr_stream = TweetListener(
    consumer_key, consumer_secret,access_token, access_token_secret,csocket=c_socket)
  twtr_stream.filter(track=['#corona'])

if __name__ == "__main__":
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # Create a socket object
  host = "127.0.0.1"     # Get local machine name
  port = 9999               # Reserve a port for your service.
  s.bind((host, port))        # Bind to the port

  print("Listening on port: %s" % str(port))

  s.listen(5)                 # Now wait for client connection.
  c, addr = s.accept()        # Establish connection with client.

  print("Received request from: " + str(addr))

  send_data(c)

