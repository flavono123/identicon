import hashlib
import unittest

import Identicon


class IdenticonTestCase(unittest.TestCase):

    def test_to_hash_hex_list_return_32bytes(self):
        self.assertEqual(len(Identicon._to_hash_hex_list('some_code')), 32)
        self.assertEqual(len(Identicon._to_hash_hex_list('other_code')), 32)

    def test_extract_color_return_hex_rgb_string(self):
        hex_list = Identicon._to_hash_hex_list('test_extract_color')

        self.assertRegex(Identicon._extract_color(hex_list), r'^#[0-9a-fA-F]{6}$')

    def test_build_grid_return_5x5_list(self):
        #dummy_hex_list = str(0x0123456789abcdef) 
        dummy_hex_list = hashlib.md5('dummy'.encode('utf8')).hexdigest()
        
        grid = Identicon._build_grid(dummy_hex_list)

        self.assertEqual(len(grid), 5)
        for i in range(5):
            self.assertEqual(len(grid[i]), 5)

    def test_mirror_row_works_for_odd_num_column_grid(self):
        half_grid = [[ 1, 2, 3],
                     [ 4, 5, 6],
                     [ 7, 8, 9],
                     [10,11,12],
                     [13,14,15]]
        expected_grid = [[ 1, 2, 3, 2, 1],
                         [ 4, 5, 6, 5, 4],
                         [ 7, 8, 9, 8, 7],
                         [10,11,12,11,10],
                         [13,14,15,14,13]]

        self.assertEqual(Identicon._mirror_row(half_grid), expected_grid)
        
        half_grid_3x3 = [[1,2],
                         [3,4],
                         [5,6]]
        expected_grid_3x3 = [[1,2,1],
                             [3,4,3],
                             [5,6,5]]

        self.assertEqual(Identicon._mirror_row(half_grid_3x3), expected_grid_3x3)


if __name__ == '__main__':
    unittest.main(warnings='ignore')
