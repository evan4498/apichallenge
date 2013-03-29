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
cs = pyrax.cloudservers

def main():
  getinfo()

def getinfo():
  print "So I hear you want to clone a server?"
  print "Here is a list of your servers for your perusing pleasure:"
  print "--------------------------------------------------"
  servers = cs.servers.list()
  for pos, cloudserver in enumerate(servers):
      print "%s: %s" % (pos, cloudserver.name)
  print
  choice = int(raw_input("Select the number for the server to clone from: "))
  server = servers[choice]
  print
  
  image_name = raw_input("Enter a name for the image to keep: ")
  print
  
  newname = raw_input("What should the new server be named? ")
  print

  createimage(server, image_name, newname)

def createimage(server, image_name, newname):
  image_id = cs.servers.create_image(server.id, image_name)
  image = cs.images.get(image_id)
  
  print "Creating image" , image_name , "with ID" , image_id , "from", server.name + "..."
  print "Patience Daniel-son, this will take a few minutes..."
  
  time.sleep(10)
  
  createnewname(server, image_name, newname, image.id)
  
def createnewname(server, image_name, newname, image_id):
  while True:
    image = cs.images.get(image_id)
    minram = image._info["minRam"]

    if image.status == "ACTIVE":
    	print "Image creation complete!"
    	print "Creating new server", newname
    	newserver = cs.servers.create(newname, image.id, 2)
    	print "New server", newname, " is building...  Enjoy!"
    	break
    elif image.status == "SAVING":
      print "Still waiting..."
      time.sleep(20)
    

if __name__ == "__main__":
  main()