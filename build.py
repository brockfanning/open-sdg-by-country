import sdmx
import sdg
import os
from urllib.request import urlretrieve


def get_dsd_url():
    return 'https://registry.sdmx.org/ws/public/sdmxapi/rest/datastructure/IAEG-SDGs/SDG/latest/?format=sdmx-2.1&detail=full&references=children'

def get_dsd():
    dsd_url = get_dsd_url()
    dsd_file = 'SDG_DSD.xml'
    urlretrieve(dsd_url, dsd_file)
    msg = sdmx.read_sdmx(dsd_file)
    return msg.structure[0]


def build_site(ref_area_id, ref_area_name):

    def alter_meta(meta):
        meta['national_geographical_coverage'] = ref_area_name
        return meta

    sdg.open_sdg_build(
        site_dir=os.path.join('_builds', ref_area_id, 'data-build'),
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
