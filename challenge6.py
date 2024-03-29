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
  container_create()

def container_create():
  print "--------------------------------------------------"
  container_choice = raw_input("What container should I create? ")
  print

  print "Creating" , container_choice , "and enabling CDN..."
  print

  container = cf.create_container(container_choice)
  container.make_public(ttl=900)

  print "Done!" 

if __name__ == "__main__":
  main()


