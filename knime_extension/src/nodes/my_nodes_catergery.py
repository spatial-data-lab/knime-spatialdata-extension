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

############################################
# Download Data From ArcGIS Online Node
############################################
@knext.node(
    name="Download Data From ArcGIS Online",
    node_type=knext.NodeType.SOURCE,
    icon_path=__NODE_ICON_PATH + "ArcGISOnline.png",
    category=__category,
    after="",
)
@knext.output_table(
    name="data content",
    description="Retrieved data contents from ArcGIS Online",
)
class DownloadDataFromArcGISOnlineNode:
    """This node retrieves data from ArcGIS Online.
    ArcGIS Online is a complete cloud-based GIS mapping software that connects people, locations and data using interactive maps.
    Please refer to [ArcGIS Online](https://www.arcgis.com/home/index.html) for more details.
    """

    public_data_item_id = knext.StringParameter(
        label="Public Data Item ID",
        description="The public data item ID to download from ArcGIS Online.",
        default_value="a04933c045714492bda6886f355416f2",
    )

    download_path = knext.StringParameter(
        label="Download Path",
        description="The path to save the downloaded data.",
        default_value="C:\\Users\\xif626\\Downloads",
    )

    def configure(self, configure_context):
        # TODO Create combined schema
        return None
    
    def execute(self, exec_context: knext.ExecutionContext):
        from arcgis.gis import GIS
        from pathlib import Path
        from zipfile import ZipFile
        import pandas as pd
        gis = GIS()

        public_data_item_id = self.public_data_item_id
        data_item = gis.content.get(public_data_item_id)


        # download_path = knext.get_workflow_data_area_dir(exec_context)
        # download_path = "data"
        download_path = self.download_path
        # configure where to save the data, and where the ZIP file is located
        data_path = Path(download_path)
        if not data_path.exists():
            data_path.mkdir()
        # zip_path = data_path.joinpath('%s.zip'%public_data_item_id)
        # extract_path = data_path.joinpath(public_data_item_id)
        data_item.download(save_path=data_path)

        zip_file_path = data_path.joinpath(data_item.name)
        zip_file = ZipFile(zip_file_path)
        zip_file.extractall(path=data_path)
        extract_path = data_path.joinpath(data_item.name.strip('.zip'))
        files = [str(file) for file in extract_path.glob('*')]
        df = pd.DataFrame(files, columns=['file_name'])
        # df = pd.DataFrame([])
        return knext.Table.from_pandas(df)

