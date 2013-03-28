#!/usr/bin/env python
import os
import sys
import time
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)

region = int(raw_input ("Select 1 for ORD, 2 for DFW, 3 for LON: "))

if region == 1:
  cdb = pyrax.connect_to_cloud_databases(region="ORD")
elif region == 2:
  cdb = pyrax.connect_to_cloud_databases(region="ORD")
elif region == 3:
  cdb = pyrax.connect_to_cloud_databases(region="LON")
else:
  print "Invalid region...  exiting"
  quit()

instname = str(raw_input("What should the Cloud DB Instance be named? "))
print

dbname = str(raw_input("What database name should be created? " ))
print

username = str(raw_input("What username name should be created? " ))
print

password = str(raw_input("What password should be used? " ))
print

print "Flavor types to choose from"
flavor_list = cdb.list_flavors()
for pos, flavor in enumerate(flavor_list):
  print "%s: %s, %s" % (pos, flavor.name, flavor.ram)
flavor_choice = int(raw_input("Select the number for the flavor to use: "))
instflavor = flavor_list[flavor_choice]
print 

instvol = int(raw_input("How big a volume in GB? (Max is 50): "))
print

print "Creating instance..."
print "This will take 3-4 minutes, patience is a virtue!"
instance = cdb.create(instname, flavor=instflavor, volume=instvol)
instanceid = instance.id
time.sleep(240)


instance.create_database(dbname)
time.sleep(10)
instance.create_user(username, password, dbname)


print "----------------------------------------------------------------"
print "Creating instance..."
print "Instance Name:", instance.name
print "Instance ID:", instance.id
print "Instance Hostname:", instance.hostname

print "Instance Volume:", instance.volume.size

