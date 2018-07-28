import kankei_paths
import yaml

with open(kankei_paths.CONF_PATH) as conf_file:
    KANKEI_CONFIG = yaml.load(conf_file)


