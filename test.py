import os
import sys
import json
import tempfile
import unittest
import subprocess


EXECUTABLE = "../build/sps"


def get_set() -> dict:
	with open("set.json") as file:
		return json.loads(file.read())


class TestSPreadSheet(unittest.TestCase):
	def _run_test_io(self, data, name):
		for itext, cmd, otext, rcode in data:
			with tempfile.NamedTemporaryFile() as tf:
				with self.subTest(name=name, cmd=[EXECUTABLE] + cmd + [tf.name], itext=itext, otext=otext, rcode=rcode):
					tf.write(itext.encode('utf-8'))
					tf.seek(0)
					r = subprocess.run(
						[self.EXECUTABLE] + cmd + [tf.name],
						encoding="utf-8",
						capture_output=True
					)
					self.assertEqual(r.returncode, rcode, f"Result code must be: {rcode}")
					self.assertEqual(tf.read(), otext)

	def test_io(self):
		data = get_set()
		for key in data:
			self._run_test_io(data[key], key)


if __name__ == "__main__":
	result = unittest.main()


# vim: ts=4 sts=4 sw=4 noet
