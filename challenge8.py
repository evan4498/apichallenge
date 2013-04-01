#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
cf = pyrax.cloudfiles
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

  while True:
    fqdn = str(raw_input("What is the FQDN you want for the site? "))
    if not domain.name in fqdn:
      print "You must type the full FQDN..."
    else:
      break
   
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

  container_create(fqdn, domain, ttltime)


def container_create(fqdn, domain, ttltime):
  container_choice = raw_input("What container should I create? ")
  print

  print "Creating" , container_choice , "and enabling CDN..."
  print

  container = cf.create_container(container_choice)
  container.make_public(ttl=900)
  
  index_content = "This is a test of Challenge 8"
  index = cf.store_object(container.name, "index.html", index_content)

  container.set_web_index_page("index.html")

  dns_create(fqdn, domain, ttltime, container)

  
def dns_create(fqdn, domain, ttltime, container):
  cdn_url = container.cdn_uri
  
  if cdn_url.startswith('http://'): 
    cdn_url = cdn_url[7:] 
  elif cdn_url.startswith('https://'): 
    cdn_url = cdn_url[8:]

  subcreate = domain.add_records({"type": "CNAME","name": fqdn,"data": cdn_url,"ttl": ttltime}) 

if __name__ == "__main__":
  main()


