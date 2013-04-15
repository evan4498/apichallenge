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
clb = pyrax.cloud_loadbalancers
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
  print "Using domain...", domain.name
  print "--------------------------------------------------"

  createservers(domain)

def createservers(domain):
  csimage = "d531a2dd-7ae9-4407-bb5a-e5ea03303d98"
  csflavor = 2
    
  print "Going to create two servers and a load balancer for them"
  serverbasename = str(raw_input ("Server name to add (I will add 1 and 2 to the end of this name for the servers): "))
  
  fqdn = serverbasename + "." + domain.name
  servername1 = serverbasename + "1" + "." + domain.name
  servername2 = serverbasename + "2" + "." + domain.name
  server1 = cs.servers.create(servername1, csimage, csflavor)
  server2 = cs.servers.create(servername2, csimage, csflavor)
  print "Creating servers" , server1.name , "and" , server2.name
  print "Waiting for network info from the new servers... (could take a couple of minutes)"
  while not (server1.networks and server2.networks):
    time.sleep(30)
    print "..."
    server1 = cs.servers.get(server1.id)
    server2 = cs.servers.get(server2.id)
  create_lb(server1, server2, fqdn, domain)

def create_lb(server1, server2, fqdn, domain):
  server1_ip = server1.networks["private"][0]
  server2_ip = server2.networks["private"][0]
  print "Creating the load balancer named" , fqdn + "..."
  node1 = clb.Node(address=server1_ip, port=80, condition="ENABLED")
  node2 = clb.Node(address=server2_ip, port=80, condition="ENABLED")
  vip = clb.VirtualIP(type="PUBLIC")
  lb = clb.create(fqdn, port=80, protocol="HTTP", nodes=[node1, node2], virtual_ips=[vip])
  print "Load balancer" , lb.name , "with IP" , lb.virtual_ips[0].address , "building..."
  print "Please wait just a couple more minutes..."
  if not pyrax.utils.wait_until(lb, 'status', 'ACTIVE', interval=30, verbose=True):
    print "Creating the lb failed"
    sys.exit(3)

  lb_options(fqdn, lb, domain)

def lb_options(fqdn, lb, domain):
  error_html = "<html><body>Oh noes this is an ERROR page...  Noooooooooo</body></html>"
  lb.manager.set_error_page(lb, error_html)
  container = cf.create_container(fqdn)
  cferror = cf.store_object(container.name, "error.html", error_html)
  print "Created an error page, which is also backed up to cloud files, and a health monitor"
  create_dns(fqdn, lb, domain)

def create_dns(fqdn, lb, domain):
  ttltime = 300
  ipaddr = lb.virtual_ips[0].address
  try:
    subcreate = domain.add_records({"type": "A","name": fqdn,"data": ipaddr,"ttl": ttltime})
    print "Created DNS record for", fqdn
  except exc.DomainRecordAdditionFailed as excmsg:
    print "FAILED: ", excmsg
    quit()
  except exc.BadRequest as excmsg:
    print "FAILED: ", excmsg
    quit()

  lb.add_health_monitor(type="CONNECT", delay=10, timeout=10, attemptsBeforeDeactivation=3)
  print "Enjoy the wonderful world of" , fqdn , "!!!"

if __name__ == "__main__":
  main()