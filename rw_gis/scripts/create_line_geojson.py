import os
import json

from collections import defaultdict
from shapely import LineString, MultiLineString, ops, to_geojson
from rw_gis import filepath, db, util


# 国土数値情報 鉄道データ
# 1. 路線毎に geojson ファイルに分割
# 2. 開発用 DB に保存

src_file_path = os.path.join(
    filepath.data_dir, "geojson/N02-21_RailroadSection.geojson"
)


def split_to_file():
    geojson = json.load(open(src_file_path))
    features = geojson["features"]

    line_strings = defaultdict(list)
    for feature in features:
        company_name = feature["properties"]["N02_004"]
        line_name = feature["properties"]["N02_003"]
        company_line_name = "{}_{}".format(company_name, line_name)

        coordinates = feature["geometry"]["coordinates"]
        ls = LineString(coordinates)
        line_strings[company_line_name].append(ls)

    for company_line_name, ls_list in line_strings.items():
        mls = MultiLineString(ls_list)
        merged_ls: LineString = ops.linemerge(mls)

        fpath = os.path.join(
            filepath.data_dir, "geojson/line/{}.geojson".format(company_line_name)
        )
        with open(fpath, "w") as f:
            f.write(to_geojson(merged_ls))


def get_company_line_list() -> dict:
    dpath = os.path.join(filepath.data_dir, "geojson/line")
    fname_list = os.listdir(dpath)
    res = {}
    for fname in fname_list:
        fpath = os.path.join(dpath, fname)
        if not os.path.isfile(fpath):
            continue
        fname_base = os.path.splitext(fname)[0]
        [company_name, line_name] = fname_base.split("_")
        [company_name, line_name] = util.convert_company_line_name(company_name, line_name)
        res["{}_{}".format(company_name, line_name)] = fpath
    return res


def get_company_line_list_db() -> dict:
    con = db.get_connection()
    res = {}
    with con.cursor() as cur:
        query = """
            select l.line_id, l.line_name, c.company_name
            from line l
            left join company c on c.company_id = l.company_id
            """
        cur.execute(query)
        rows = cur.fetchall()
        for r in rows:
            line_name = str(r["line_name"]).replace("（", "").replace("）", "")
            res["{}_{}".format(r["company_name"], line_name)] = r["line_id"]
    return res


def save_to_db():
    cl_list = get_company_line_list()
    cl_db_list = get_company_line_list_db()

    con = db.get_connection()

    for company_line_name, fpath in cl_list.items():
        if company_line_name not in cl_db_list:
            print(company_line_name)
            continue
        line_id = cl_db_list[company_line_name]
        geojson = open(fpath).read()
        with con.cursor() as cur:
            query = "insert into line_geojson values(%s, %s)"
            cur.execute(query, [line_id, geojson])

    con.commit()

if __name__ == "__main__":
    pass
    # main()
    save_to_db()
