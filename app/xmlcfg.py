from lxml import etree

PROFILES = {
    "standard": {
        "resolve_entities": False,
        "no_network": True,
        "load_dtd": False,
        "huge_tree": True,
    },
    "instrument": {
        "resolve_entities": True,
        "no_network": False,
        "load_dtd": True,
        "huge_tree": True,
    },
}


def build_parser(profile):
    options = PROFILES[profile]
    return etree.XMLParser(**options)
