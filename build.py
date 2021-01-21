import sdmx
import sdg
import os
import yaml
from urllib.request import urlretrieve
from pathlib import Path


def get_dsd_url():
    return 'https://registry.sdmx.org/ws/public/sdmxapi/rest/datastructure/IAEG-SDGs/SDG/latest/?format=sdmx-2.1&detail=full&references=children'

def get_dsd():
    dsd_url = get_dsd_url()
    dsd_file = 'SDG_DSD.xml'
    urlretrieve(dsd_url, dsd_file)
    msg = sdmx.read_sdmx(dsd_file)
    return msg.structure[0]


def get_site_config(ref_area_id, ref_area_name):
    with open('config_site.yml', 'r') as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)
    config['title'] = ref_area_name + ' Indicators for the Sustainable Development Goals'
    config['baseurl'] = '/open-sdg-by-country/' + ref_area_id
    config['remote_data_prefix'] = '../../data/' + ref_area_id
    config['country'] = {
        'name': ref_area_name,
        'adjective': ref_area_name
    }
    return config


def build_site(ref_area_id, ref_area_name):

    site_folder = os.path.join('_builds', 'site', ref_area_id)
    data_folder = os.path.join('_builds', 'data', ref_area_id)
    Path(site_folder).mkdir(parents=True, exist_ok=True)
    Path(data_folder).mkdir(parents=True, exist_ok=True)

    site_config = get_site_config(ref_area_id, ref_area_name)
    with open(os.path.join(site_folder, '_config.yml'), 'w') as stream:
        yaml.dump(site_config, stream)

    def alter_meta(meta):
        meta['national_geographical_coverage'] = ref_area_name
        return meta

    sdg.open_sdg_build(
        site_dir=data_folder,
        schema_file='_prose.yml',
        languages=['en'],
        translations=[
            {'class': 'TranslationInputSdgTranslations'},
            {'class': 'TranslationInputSdmx', 'source': get_dsd_url()},
        ],
        inputs=[
            {'class': 'InputSdmxMl_UnitedNationsApi', 'reference_area': ref_area_id},
        ],
        alter_meta=alter_meta,
        docs_subfolder='data-docs',
    )


def get_ref_area_codes():
    dsd = get_dsd()
    ref_area = next(dim for dim in dsd.dimensions if dim.id == 'REF_AREA')
    codelist = ref_area.local_representation.enumerated
    numeric_codes = list(filter(lambda code: code.id.isnumeric(), codelist))
    numeric_codes.sort(key=lambda x: int(x.id))
    return numeric_codes


for code in get_ref_area_codes():
    build_site(code.id, str(code.name))
    break
