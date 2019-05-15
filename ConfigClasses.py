from ConfigStructure import Config
from xml.dom import minidom

class ConfigBaseSvc:
  def __init__(self, config_file_name):
    self.doc = minidom.parse(config_file_name)

  def get_config_info(self, node_name):
    node = self.doc.getElementsByTagName('address')

    if (not node):
      return Config("", "", "", "")
    else:
      for element in node:
        if (element.attributes['name'].value == node_name):
          url = element.getElementsByTagName('url')[0].firstChild.data
          port = element.getElementsByTagName('port')[0].firstChild.data
          username = element.getElementsByTagName('username')[0].firstChild.data
          password = element.getElementsByTagName('password')[0].firstChild.data

          return Config(url, port, username, password)

      return Config("", "", "", "")

class ConfigSvc(ConfigBaseSvc):

  def get_source_path(self):
    return self.get_config_info("source")

  def get_destination_path(self):
    return self.get_config_info("destination")