#!/usr/bin/env python
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
    print "%s: %s" % (pos, domain)
  
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
