import os
import sys
import json
import tempfile
import unittest
import subprocess


def get_set(name: str) -> list:
	with open("set.json") as file:
		return json.loads(file.read())[name]


class TestSPreadSheet(unittest.TestCase):

	EXECUTABLE = "../build/sps"

	def _run_test_io(self, data):
		for itext, cmd, otext, rcode in data:
			with tempfile.NamedTemporaryFile() as tf:
				with self.subTest(cmd=[self.EXECUTABLE] + cmd + [tf.name], itext=itext, otext=otext, rcode=rcode):
					tf.write(itext.encode('utf-8'))
					tf.seek(0)
					print(tf.name)
					r = subprocess.run(
						[self.EXECUTABLE] + cmd + [tf.name],
						encoding="utf-8",
						capture_output=True
					)
					self.assertEqual(r.returncode, rcode, f"Result code must be: {rcode}")
					self.assertEqual(tf.read(), otext)

	def _run_test_result(self, data):
		for itext, cmd, otext, rcode in data:
			with self.subTest(cmd=cmd, itext=itext, otext=otext, rcode=rcode):
				r = subprocess.run(
					[self.EXECUTABLE] + cmd,
					input=itext,
					encoding="utf-8",
					capture_output=True
				)
				self.assertEqual(r.returncode, rcode, f"Result code must be: {rcode}")

	def test_result(self):
		data = get_set('results')
		self._run_test_result(data)

	def test_delimiter(self):
		pass

	def test_cell_selection(self):
		""" Test Cell Selection """

		data = get_set('cell_selection')
		self._run_test_io(data)


if __name__ == "__main__":
	result = unittest.main()


# vim: ts=4 sts=4 sw=4 noet
