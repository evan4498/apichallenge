#!/usr/bin/env python
import os
import sys
import time
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers


def createserver(csname):
  csimage = "d531a2dd-7ae9-4407-bb5a-e5ea03303d98"
  csflavor = 2
  server = cs.servers.create(csname, csimage, csflavor)
  rootpass = server.adminPass
  time.sleep(10)
  print ""
  print "Creating server \'" + server.name + "\' with ID \'" + server.id + "\'"
  print "gathering server info..."
  showdetails(server,rootpass)

def showdetails(server,rootpass):
  serverinfo = cs.servers.get(server.id)
  networks = serverinfo.networks
  if len(serverinfo.networks) > 0:
    print "-------------------------------------------------"
    print "Name:", serverinfo.name
    print "Admin Password:", rootpass
    for pubaddr in  serverinfo.addresses["public"]:
      print "Public Network:", pubaddr['addr']
    print "-------------------------------------------------"

  else:
    time.sleep(10)
    showdetails(serverinfo,rootpass)

def main():
  csnumber = int(raw_input ("How many servers should I create: "))
  csbasename = str(raw_input ("What do you want the servers to be named: "))
  print "This should take a few minutes, and possibly as much as 12 parsecs..."
  total = 0
  while total < csnumber:
    total = total + 1
    csname = csbasename + str(total)
    createserver(csname)

if __name__ == "__main__":
  main()
