"""
This file is part of CLIMADA.

Copyright (C) 2017 ETH Zurich, CLIMADA contributors listed in AUTHORS.

CLIMADA is free software: you can redistribute it and/or modify it under the
terms of the GNU Lesser General Public License as published by the Free
Software Foundation, version 3.

CLIMADA is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with CLIMADA. If not, see <https://www.gnu.org/licenses/>.

Unit Tests on LitPop exposures.
"""

import unittest
import numpy as np

from climada.entity.exposures.litpop import LitPop
from climada.entity.exposures import litpop as lp



# ---------------------
class TestLitPopClass(unittest.TestCase):

    def test_wrong_iso3_fail(self):
        """Wrong ISO3 code"""
        ent = LitPop()
        with self.assertRaises(ValueError):
            ent = LitPop()
            ent.set_country('OYY')

class TestLitPopFunctions(unittest.TestCase):
    """Test LitPop Class methods"""

    def test_get_country_shape_BEL(self):
        """test _get_country_shape function: get shape and bbox for Belgium"""
        shp = lp._get_country_shape('BEL', only_geo=0)
        self.assertEqual(len(shp.bbox), 4)
        self.assertEqual(shp.bbox[0], 2.5217999276904663)
        self.assertEqual(shp.bbox[3], 51.49623769100013)
        self.assertTrue(0 in shp.parts)
        self.assertEqual(len(shp.parts), 1)
        self.assertEqual(len(shp.points), 653)
        self.assertEqual(max(shp.points)[0], 6.374525187000074)
        self.assertEqual(shp.shapeType, 5)

    def test_get_country_shape_NZL(self):
        """test _get_country_shape function: get shape and bbox for New Zealand"""
        shp = lp._get_country_shape('NZL', only_geo=0)
        self.assertEqual(shp.bbox[0], -177.95799719999985)
        self.assertEqual(len(shp.parts), 25)
        self.assertEqual(max(shp.parts), 4500)
        self.assertEqual(len(shp.points), 4509)
        self.assertEqual(min(shp.points)[1], -29.22275155999992)
        self.assertEqual(shp.shapeType, 5)

    def test_get_country_bbox(self):
        """test _get_country_shape function: get bbox for Swaziland"""
        bbox, lat, lon = lp._get_country_shape('SWZ', only_geo=1)
        self.assertEqual(len(lat), len(lon))
        self.assertEqual(len(lat), 86)
        self.assertEqual(len(bbox), 4)
        self.assertTrue(32.117398316000106 in bbox)
    
    def test_get_country_info(self):
        """test _get_country_info function (Togo and Russia)"""
        countries = ['TGO', 'RUS']
        country_info = dict()
        admin1_info = dict()
        for country in countries:
            country_info[country], admin1_info[country] = \
            lp._get_country_info(country)
        
        # meta information:
        self.assertEqual(country_info['TGO'][0], 217)
        self.assertEqual(country_info['RUS'][0], 189)
        self.assertEqual(country_info['TGO'][1], 'Togo')
        # shape:
        shp = country_info['RUS'][2]
        self.assertEqual(len(shp.bbox), 4)
        self.assertEqual(shp.bbox[0], -179.9999999999999)
        self.assertEqual(shp.bbox[3], 81.85871002800009)
        self.assertTrue(10691 and 140 and 10634 in shp.parts)
        self.assertEqual(len(shp.parts), 214)
        self.assertEqual(len(shp.points), 36776)
        self.assertEqual(min(shp.points)[1], 65.06622947500016)
        self.assertEqual(shp.shapeType, 5)
        # admin-1 record:
        self.assertEqual(admin1_info['TGO'][4].attributes['name_nl'], 'Maritime')
        self.assertEqual(admin1_info['TGO'][4].attributes['woe_id'], 56048437)
        self.assertEqual(admin1_info['TGO'][3].attributes['gn_name'], 'Region des Plateaux')
        self.assertEqual(admin1_info['RUS'][0].attributes['postal'], 'GA')
        self.assertTrue(49.0710110480001 in admin1_info['RUS'][0].bounds)
        self.assertEqual(admin1_info['RUS'][0].geometry.area, 11.832370529488792)
        # index out of bounds:
        with self.assertRaises(IndexError):
            admin1_info['TGO'][5].attributes['woe_id']
        with self.assertRaises(IndexError):
            country_info['TGO'][102]

    def test_mask_from_shape(self):
        """test function _mask_from_shape for Swaziland"""
        curr_country = 'SWZ'
        curr_shp = lp._get_country_shape(curr_country, 0)
        mask = lp._mask_from_shape(curr_shp, resolution=60)
        self.assertEqual(mask.size, 5591)
        self.assertTrue(mask.values.max())
        self.assertTrue(140 and 7663 in mask.sp_index.indices)

    def test_litpop_data(self):
        """test functions _litpop_box2coords and _get_litpop_box for Taiwan"""
        curr_country = 'TWN'
        resolution = 3000
        cut_bbox = lp._get_country_shape(curr_country, 1)[0]
        all_coords = lp._litpop_box2coords(cut_bbox, resolution, 1)
        self.assertEqual(len(all_coords), 25)
        self.assertTrue(117.91666666666666 and 22.08333333333333 in min(all_coords))
        litpop_data = lp._get_litpop_box(cut_bbox, resolution, 0, 2016, [1, 1])
        self.assertEqual(len(litpop_data), 25)
        self.assertEqual(max(litpop_data), 544316890)

        
# Execute Tests
TESTS = unittest.TestLoader().loadTestsFromTestCase(TestLitPopFunctions)
TESTS.addTests(unittest.TestLoader().loadTestsFromTestCase(TestLitPopClass))
unittest.TextTestRunner(verbosity=2).run(TESTS)