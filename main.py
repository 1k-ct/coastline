import geopandas as gpd
from shapely.geometry import Point

# ==== 志摩市役所の座標（WGS84） ====
lon, lat = 136.82954059154602, 34.32816432956693

# ==== 海岸線データ（例：三重県用のC23ファイル） ====
coastline_file = "C23-06_24-g_Coastline.shp"

# ==== 距離計算用の投影座標系（第7系）====
PROJ_CRS = "EPSG:6675"  # JGD2011 / 平面直角座標系 第7系（三重・和歌山）

# ==== 海岸線読み込み ====
coast_gdf = gpd.read_file(coastline_file)

# CRSが未設定の場合にJGD2000として仮設定
if coast_gdf.crs is None or coast_gdf.crs.to_epsg() is None:
    coast_gdf.set_crs(epsg=4612, inplace=True)

# ==== 座標点をGeoDataFrameに ====
pt = gpd.GeoDataFrame(geometry=[Point(lon, lat)], crs="EPSG:4326")

# ==== 距離計算のために両方を投影座標系に変換 ====
coast_proj = coast_gdf.to_crs(PROJ_CRS)
pt_proj = pt.to_crs(PROJ_CRS)

# ==== 最短距離計算 ====
distances = coast_proj.geometry.distance(pt_proj.geometry.iloc[0])
min_distance = distances.min()

# ==== 結果表示 ====
print(f"志摩市役所（{lat}, {lon}）から海岸線までの最短距離：{min_distance:.2f} メートル")