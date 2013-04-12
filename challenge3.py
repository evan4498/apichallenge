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
import pyrax

creds_file = os.path.expanduser("~/.rackspace_cloud_credentials")
pyrax.set_credential_file(creds_file)
cf = pyrax.cloudfiles

def main():
  getdir()

def getdir():
  print "--------------------------------------------------"
  
  directory = raw_input("What directory should I upload? ")
  
  if os.path.isdir(directory) == True:
    container_build(directory)
  else:
    print "The directory" , directory , "does not exist..."
    getdir()

  
def container_build(directory):
  container_choice = raw_input("What container should I use (or create)? ")
  container = cf.create_container(container_choice)

  upload_files(directory,container)
  
def upload_files(directory,container):
  upload = cf.upload_folder(directory,container.name)    
  print "Uploading", directory , "to container" , container.name , "..."

if __name__ == "__main__":
  main()
