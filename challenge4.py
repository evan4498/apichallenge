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
dns = pyrax.cloud_dns

def main():
  print "A list of your domains for your perusing pleasure:"
  print "--------------------------------------------------"
  domslist = dns.list()
  for pos, domain in enumerate(domslist):
    print "%s: %s" % (pos, domain.name)
  
  dom_choice = int(raw_input("Select the number for the domain to use: "))
  domain = domslist[dom_choice]
  
  print
  print "Using domain...", domain.name
  print

  getinfo(domain)

def getinfo(domain):
  while True:
    fqdn = str(raw_input("What is the FQDN you want an A record for? "))
    if not domain.name in fqdn:
      print "You must type the full FQDN..."
    else:
      break
  
  while True:
    ipaddr = str(raw_input("What IP address should this A record point to? "))
    try:
      first, second, third, fourth = [part for part in map(int, ipaddr.split(".")) if part < 255]
      break
    except exceptions.ValueError as excmsg:
      print "You did not enter a valid IP..."
   
  while True:
    ttltime = raw_input("What do you want the ttl to be? (300-86400) ")
    try:
      ttltime = int(ttltime)
      if ttltime < 300 or ttltime > 86400:
        print "You must enter a TTL between 300 and 86400..."
      else:
        break
    except:
        print "You must enter a valid integer between 300 and 86400..."

  createrecord(fqdn, ipaddr, ttltime, domain)

def createrecord(fqdn, ipaddr, ttltime, domain):
  try:
    subcreate = domain.add_records({"type": "A","name": fqdn,"data": ipaddr,"ttl": ttltime})
    print ""
    print "Created" , fqdn , "with IP" , ipaddr
  except exc.DomainRecordAdditionFailed as excmsg:
    print "FAILED: ", excmsg
    quit()
  except exc.BadRequest as excmsg:
    print "FAILED: ", excmsg
    quit()

if __name__ == "__main__":
  main()
