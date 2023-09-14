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


############################################
# Open Sky Network Data Node
############################################
@knext.node(
    name="Open Sky Network Data",
    node_type=knext.NodeType.SOURCE,
    icon_path=__NODE_ICON_PATH + "OpenSkyNetwork.png",
    category=__category,
    after="",
)
@knext.output_table(
    name="Open Sky Network Data Table",
    description="Retrieved geodata from Open Sky Network Data",
)
class OpenSkyNetworkDataNode:
    """This node retrieves Open Sky Network Data.
    The OpenSky Network is a non-profit association based in Switzerland that operates a crowdsourced global
    database of air traffic control data.
    The network consists of thousands of sensors connected to the Internet by volunteers, whose main purpose is to
    measure the radio signals emitted by aircraft to track their position.
    Please refer to [Open Sky Network Document](https://opensky-network.org/) for more details.
    """

    user = knext.StringParameter(
        label="User",
        description="The user name to access Open Sky Network Data.",
        default_value="",
    )

    password = knext.StringParameter(
        label="Password",
        description="The password to access Open Sky Network Data.",
        default_value="",
    )

    def configure(self, configure_context):
        # TODO Create combined schema
        return None

    def execute(self, exec_context: knext.ExecutionContext):
        import geopandas as gp
        import pandas as pd
        import requests

        url = "https://opensky-network.org/api/states/all"
        kws = {"url": url, "timeout": 120}
        if len(self.user) != 0 and len(self.password) != 0:
            kws["auth"] = (self.user, self.password)

        response = requests.get(**kws)
        # if (self.user is not None or ) and (self.password is not None or len(self.password)!=0):
        #     response = requests.get(url, timeout=120,auth=(self.user, self.password))
        # else:
        #     response = requests.get(url, timeout=120)
        json_data = response.json()
        states = pd.DataFrame(
            json_data["states"],
            columns=[
                "icao24",
                "callsign",
                "origin_country",
                "time_position",
                "last_contact",
                "longitude",
                "latitude",
                "baro_altitude",
                "on_ground",
                "velocity",
                "true_track",
                "vertical_rate",
                "sensors",
                "geo_altitude",
                "squawk",
                "spi",
                "position_source",
            ],
        )
        gdf = gp.GeoDataFrame(
            states,
            geometry=gp.points_from_xy(states.longitude, states.latitude),
            crs="EPSG:4326",
        )
        return knext.Table.from_pandas(gdf)


############################################
# Blockchain Data Center Node
############################################
@knext.node(
    name="Blockchain Data Center",
    node_type=knext.NodeType.SOURCE,
    icon_path=__NODE_ICON_PATH + "BlockchainDataCenter.png",
    category=__category,
    after="",
)
@knext.output_table(
    name="Blockchain Data Center Table",
    description="Retrieved geodata from Blockchain Data Center",
)
class BlockchainDataCenterNode:
    """This node retrieves Blockchain Data Center.
    Blockchain Data Center is a data center that is used to store blockchain data.
    Please refer to [Blockchain Data Center Dashboard](https://dashboard.internetcomputer.org/centers) for more details.
    """

    def configure(self, configure_context):
        # TODO Create combined schema
        return None

    def execute(self, exec_context: knext.ExecutionContext):
        import geopandas as gp
        import pandas as pd
        import requests

        url = "https://ic-api.internetcomputer.org/api/v3/data-centers"
        response = requests.get(url, timeout=120)
        json_data = response.json()
        data = pd.DataFrame(json_data["data_centers"])

        gdf = gp.GeoDataFrame(
            data,
            geometry=gp.points_from_xy(data.longitude, data.latitude),
            crs="EPSG:4326",
        )

        return knext.Table.from_pandas(gdf)
