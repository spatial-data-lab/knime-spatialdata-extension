import knime_extension as knext
import util.knime_utils as knut



__category = knext.category(
    path="/community/knime-spatialdata-extension",
    level_id="my_nodes_catergery",
    name="Open Datasets",
    description="Nodes for providing open geospatial datasets.",
    # starting at the root folder of the extension_module parameter in the knime.yml file
    icon="icons/icon/OpendatasetCategory.png",
    after="LocationAnalysis",
)

# Root path for all node icons in this file
__NODE_ICON_PATH = "icons/icon/OpenDataset/"
