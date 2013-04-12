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
clb = pyrax.cloud_loadbalancers

def main():
  createservers()

def createservers():
  csimage = "d531a2dd-7ae9-4407-bb5a-e5ea03303d98"
  csflavor = 2
  
  print "-------------------------------------"
  print "Going to create two servers and a load balancer for them"
  serverbasename = str(raw_input ("Server name to add (I will add 1 and 2 to the end of this name for the servers): "))
  servername1 = serverbasename + "1"
  servername2 = serverbasename + "2"
  server1 = cs.servers.create(servername1, csimage, csflavor)
  server2 = cs.servers.create(servername2, csimage, csflavor)
  print "Creating servers" , server1.name , "and" , server2.name
  print "Waiting for network info from the new servers... (could take a couple of minutes)"
  while not (server1.networks and server2.networks):
    time.sleep(30)
    print "..."
    server1 = cs.servers.get(server1.id)
    server2 = cs.servers.get(server2.id)
  create_lb(server1, server2, serverbasename)

def create_lb(server1, server2, serverbasename):
  server1_ip = server1.networks["private"][0]
  server2_ip = server2.networks["private"][0]
  
  print "Creating the load balancer named" , serverbasename + "..."
  node1 = clb.Node(address=server1_ip, port=80, condition="ENABLED")
  node2 = clb.Node(address=server2_ip, port=80, condition="ENABLED")
  vip = clb.VirtualIP(type="PUBLIC")
  lb = clb.create(serverbasename, port=80, protocol="HTTP", nodes=[node1, node2], virtual_ips=[vip])

  print "Load balancer" , lb.name , "with ID" , lb.id , "and nodes" , server1.name , "and" , server2.name , "created!"

if __name__ == "__main__":
  main()