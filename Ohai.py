#!/usr/bin/env python

import commands

class Ohai:
    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config

    def run(self):
      status, output = commands.getstatusoutput("ohai")
      if status != 0:
        return False
      else:
        try:
          try:
            import json
            return json.loads(output)
          except ImportError, e:
            self.checks_logger.debug('Could not load modern json module. Falling back to minjson.')
            import minjson
            return minjson.safeRead(output)
        except Exception, e:
            import traceback
            self.checks_logger.error('Unable to load facter JSON - Exception = ' + traceback.format_exc())
            return False

if __name__ == '__main__':
  import sys
  import logging
  logger =  logging.getLogger()
  handler = logging.StreamHandler(sys.stderr)
  logger.addHandler(handler)

  ohai = Ohai(None, logger, None)
  print ohai.run()
