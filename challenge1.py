#!/usr/bin/env python
# Copyright 2012 Rackspace

# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import os
import sys
import time
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers

def main():
  csnumber = int(raw_input ("How many servers should I create: "))
  csbasename = str(raw_input ("What do you want the servers to be named: "))
  print "This should take a few minutes, and possibly as much as 12 parsecs..."
  total = 0
  while total < csnumber:
    total = total + 1
    csname = csbasename + str(total)
    createserver(csname)

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



if __name__ == "__main__":
  main()
