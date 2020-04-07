from elliptic import *
from finitefield.finitefield import FiniteField

import os


def generateSecretKey(numBits):
   return int.from_bytes(os.urandom(numBits // 8), byteorder='big')


def sendDH(privateKey, generator, sendFunction):
   return sendFunction(privateKey * generator)


def receiveDH(privateKey, receiveFunction):
   return privateKey * receiveFunction()


def slowOrder(point):
   Q = point
   i = 1
   while True:
      if type(Q) is Ideal:
         return i
      else:
         Q = Q + point
         i += 1


