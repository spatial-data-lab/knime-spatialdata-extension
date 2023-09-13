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


############################################
# GDELT nodes
############################################
@knext.node(
    name="GDELT Global Knowledge Graph",
    node_type=knext.NodeType.SOURCE,
    icon_path=__NODE_ICON_PATH + "GDELT.png",
    category=__category,
    after="",
)
@knext.output_table(
    name="GDELT GKG Data Table",
    description="Retrieved geodata from GDELT Global Knowledge Graph",
)
class GDELTGKGNode:
    """This node retrieves GDELT Global Knowledge Graph data.
    The GDELT Global Knowledge Graph (GKG) is a real-time knowledge graph of global human society for open research.
    The GKG is a massive archive of global news and translated into 65 languages, updated every 15 minutes.
    The GKG is a network diagram of the world's events and news coverage, containing more than 1.5 billion people,
    organizations, locations, themes, emotions, counts, quotes, images and events across the planet
    dating back to January 1, 1979 and updated every 15 minutes.
    Please refer to [GDELT Document](https://blog.gdeltproject.org/announcing-our-first-api-gkg-geojson/) for more details.
    """

    key_word = knext.StringParameter(
        label="Key Word",
        description="The key word to search in GDELT GKG.",
        default_value="FOOD_SECURITY",
    )

    last_hours = knext.IntParameter(
        label="Last Hours",
        description="The last hours to search in GDELT GKG.",
        default_value=24,
    )

    def configure(self, configure_context):
        # TODO Create combined schema
        return None

    def execute(self, exec_context: knext.ExecutionContext):
        import geopandas as gp
        import requests

        url = "https://api.gdeltproject.org/api/v1/gkg_geojson?QUERY=%s&TIMESPAN=%d" % (
            self.key_word,
            self.last_hours * 60,
        )
        response = requests.get(url, timeout=120)
        data = response.json()
        gdf = gp.GeoDataFrame.from_features(data, crs="EPSG:4326")
        return knext.Table.from_pandas(gdf)
