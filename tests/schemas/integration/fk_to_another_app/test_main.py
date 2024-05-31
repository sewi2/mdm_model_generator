import os
import tempfile
from filecmp import dircmp
from pathlib import Path

from tests.common import SCHEMA_FILENAME, print_diff_items


BASE_DIR = Path(__file__).parent
SCHEMA_FILEPATH = BASE_DIR / SCHEMA_FILENAME
EXPECTED_RESULTS_DIR = BASE_DIR / 'expected_results'
COMMAND_TEMPLATE = "python -m mdm_model_generator %s %s"


class TestMainFKToAnotherApp:
    def test_main(self):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            cmd = COMMAND_TEMPLATE % (str(SCHEMA_FILEPATH), str(tmp_dir_name))
            print('Command has been run.', cmd)
            os.system(cmd)
            dcmp = dircmp(str(EXPECTED_RESULTS_DIR), str(tmp_dir_name))
            dcmp.report_full_closure()
            print_diff_items(dcmp)
            assert not dcmp.diff_files
