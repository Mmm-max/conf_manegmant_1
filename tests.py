import unittest
from shell import Shell
from unittest.mock import patch
from io import StringIO

CONF = "/Users/eugensolopov/code/python/mirea/conf_managment/1/conf.csv"

class TestShell(unittest.TestCase):
    
    def setUp(self) -> None:
        self.shell = Shell()
        self.shell.read_config(CONF)
        self.shell.load_fs_from_zip()
        
    # cd tests
    
    def test_cd_valid(self):
        self.shell.cd("first")
        self.assertEqual(self.shell.current.path, "~/first")
    
    def test_cd_valid_2(self):
        self.shell.cd("first/second")
        self.assertEqual(self.shell.current.path, "~/first/second")
    
    def test_valid_cd_root(self):
        self.shell.cd("/")
        self.assertEqual(self.shell.current.path, "~")
    
    def test_invalid_cd(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.shell.cd("first/third")
            self.assertEqual(fake_out.getvalue().strip(), "Invalid path ~/first/third does not exist")
    
    # ls tests
    
    def test_ls_valid(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.shell.ls()
            self.assertEqual(fake_out.getvalue().strip(), "first")
    
    def test_ls_valid_2(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.shell.ls("first")
            self.assertEqual(fake_out.getvalue().strip(), "alternative second")

    def test_ls_invalid(self):
        with patch('sys.stdout', new=StringIO()) as fakeout:
            self.shell.ls("first/third")
            self.assertEqual(fakeout.getvalue().strip(), "Invalid path ~/first/third does not exist")
    
    # rm tests
    
    
    def test_rm_invalid_1(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.shell.rm("first")
            self.assertEqual(fake_out.getvalue().strip(), "rm: first: is a folder")
    
    def test_rm_invalid_2(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.shell.rm("first/third")
            self.assertEqual(fake_out.getvalue().strip(), "Invalid path ~/first/third does not exist")
    
    def test_rm_valid(self):
        self.shell.rm("first/second/2.txt")
        self.shell.cd("first/second")
        content_names = self.shell.current.return_content_names()
        self.assertNotIn("2.txt", content_names)
    
    # cat tests
    
    def test_cat_valid(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.shell.cat("first/second/1.txt")
            self.assertEqual(fake_out.getvalue().strip(), "hellow word")
    
    def test_cat_invalid(self):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            self.shell.cat("first/third/2.txt")
            self.assertEqual(fake_out.getvalue().strip(), "Invalid path ~/first/third does not exist")
        
if __name__ == "__main__":
    unittest.main()