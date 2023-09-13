# The root category of all knime-spatialdata-extension categories
import knime_extension as knext

# This defines the root knime-spatialdata-extension KNIME category that is displayed in the node repository
category = knext.category(
    path="/community",
    level_id="knime-spatialdata-extension", # this is the id of the category in the node repository #FIXME: 
    name="knime-spatialdata-extension",
    description="Open Spatial Data For Knime",
    # starting at the root folder of the extension_module parameter in the knime.yml file
    icon="icons/icon/knime-spatialdata-extension.png",
)


# need import node files here
import nodes.my_nodes_catergery
