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
import pyrax.exceptions as exc
import exceptions

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cs = pyrax.cloudservers
dns = pyrax.cloud_dns

def main():
  print "A list of your domains for your perusing pleasure:"
  print "--------------------------------------------------"
  domslist = dns.list()
  for pos, domain in enumerate(domslist):
    print "%s: %s" % (pos, domain.name)
  dom_choice = int(raw_input("Select the number for the domain to use: "))
  domain = domslist[dom_choice]
  print ""

  while True:
   csname = str(raw_input("What is the full FQDN of the server to create? "))
   if not domain.name in csname:
     print "You must type the full FQDN..."
   else:
     print ""
     break

  print "A list of possible images to choose from"
  print "--------------------------------------------------"

  images = cs.images.list()
  for pos, image in enumerate(images):
    print pos , image.id , image.name

  print ""  
  csimage = int(raw_input("What image number should I use? "))
  image = images[csimage]
  print ""

  print "A list of possible flavors to choose from (you know, for kids!)"
  print "--------------------------------------------------"

  flavors = cs.flavors.list()
  for flv in flavors:
    print "  ID:", flv.id , "Name:", flv.name , "  RAM:", flv.ram, "  Disk:", flv.disk , "  VCPUs:", flv.vcpus
  while True:
    csflavor = raw_input("What flavor number id should I use? ")
    try:
      csflavor = int(csflavor)
      if csflavor < 2 or csflavor > 8:
        print "You must enter an ID between 2 and 8"
      else:
        break
    except:
        print "You must enter an ID between 2 and 8"

  print "This should take a few minutes, and possibly as much as 12 parsecs..."
  
  createserver(csname, image, csflavor, domain)


def createserver(csname, image, csflavor, domain):
  server = cs.servers.create(csname, image, csflavor)
  rootpass = server.adminPass
  time.sleep(10)
  print ""
  print "Creating server \'" + server.name + "\' with ID \'" + server.id + "\'"
  print "gathering server info..."
  showdetails(csname, server, rootpass, domain)

def showdetails(csname, server, rootpass, domain):
  serverinfo = cs.servers.get(server.id)
  networks = serverinfo.networks
  if len(serverinfo.networks) > 0:
    for pubaddr in  serverinfo.addresses["public"]:
      if "." in pubaddr['addr']:
        ipaddr = pubaddr['addr']
    print "-------------------------------------------------"
    print "Name:", serverinfo.name
    print "Admin Password:", rootpass
    print "Public Network:", ipaddr
    print "-------------------------------------------------"
    createrecord(csname, ipaddr, serverinfo, domain)
  else:
    time.sleep(10)
    showdetails(csname, serverinfo,rootpass, domain)

def createrecord(csname, ipaddr, serverinfo, domain):
  try:
    subcreate = domain.add_records({"type": "A","name": csname,"data": ipaddr,"ttl": 300})
    print ""
    print "DNS Record created for" , serverinfo.name
  except exc.DomainRecordAdditionFailed as excmsg:
    print "FAILED: ", excmsg
    quit()
  except exc.BadRequest as excmsg:
    print "FAILED: ", excmsg
    quit()


if __name__ == "__main__":
  main()
