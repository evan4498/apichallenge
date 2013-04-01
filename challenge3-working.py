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

def main():
  getinfo()

def getinfo():
  print "--------------------------------------------------"
  container_choice = raw_input("What container should I use (or create)? ")
  print
  
  directory_choice = raw_input("What directory should I upload? ")
  print

  container_use(container_choice, directory_choice)
  
def container_use(container_choice, directory_choice):
  container = cf.create_container(container_choice)
  print "Using container...  " , container.name

  directory_scan(container, directory_choice)

def directory_scan(container, directory_choice):
  files = []
  for filenames in os.walk(directory_choice):
    files.append(os.path.join(filenames))
    container.upload_file(filenames)
 


if __name__ == "__main__":
  main()
