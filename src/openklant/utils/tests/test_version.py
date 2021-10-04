from subprocess import CalledProcessError
from unittest import skipIf
from unittest.mock import mock_open, patch

from django.conf import settings
from django.test import TestCase
from django.utils.module_loading import import_string

from openklant.conf.utils import get_current_version


class VersionTestCase(TestCase):
    def setUp(self):
        patched_subprocess = patch("openklant.conf.utils.check_output")
        self.mocked_subprocess = patched_subprocess.start()

        patched_which = patch("openklant.conf.utils.which")
        self.mocked_which = patched_which.start()

    @patch.dict("os.environ", {"VERSION_TAG": "foobar"})
    def test_version_tag_set(self):
        self.assertEqual(get_current_version(), "foobar")


@patch.dict("os.environ", {"VERSION_TAG": ""})
class GitVersionTestCase(VersionTestCase):
    def setUp(self):
        super().setUp()

        self.mocked_which.return_value = True # assume git is installed for this testcase

    def tearDown(self):
        patch.stopall()

    def test_tagged_commit(self):
        self.mocked_subprocess.return_value = "v1.2.4"

        self.assertEqual(get_current_version(), "v1.2.4")

    def test_multiple_tags(self):
        self.mocked_subprocess.return_value = "v5.1.1\nv3.4.1\nv0.2.2\n"

        self.assertEqual(get_current_version(), "v5.1.1")

    def test_tag_error(self):
        self.mocked_subprocess.side_effect = (
            CalledProcessError(1, "/bin/false"),
            "c4a364ccce8b99105b8d371100918645559174b1",
        )

        self.assertEqual(
            get_current_version(), "c4a364ccce8b99105b8d371100918645559174b1"
        )

    def test_tag_and_commit_error(self):
        self.mocked_subprocess.side_effect = (
            CalledProcessError(1, "/bin/false"),
            CalledProcessError(1, "/bin/false"),
        )

        self.assertEqual(get_current_version(), "")

    def test_commit_hash(self):
        self.mocked_subprocess.side_effect = (
            "",
            "c4a364ccce8b99105b8d371100918645559174b1",
        )

        self.assertEqual(
            get_current_version(), "c4a364ccce8b99105b8d371100918645559174b1"
        )

    def test_no_tag_or_commit(self):
        self.mocked_subprocess.side_effect = (
            "",
            "",
        )

        self.assertEqual(get_current_version(), "")


@patch.dict("os.environ", {"VERSION_TAG": ""})
class FileVersionTestCase(VersionTestCase):
    def setUp(self):
        super().setUp()

        # assume git is not installed for this testcase
        self.mocked_which.return_value = False

        patched_listdir = patch("openklant.conf.utils.os.listdir")
        self.mocked_listdir = patched_listdir.start()

    @patch("builtins.open", new_callable=mock_open, read_data="commit-hash")
    def test_simple(self, mock_file):
        self.mocked_listdir.return_value = (
            "master", "main", "foo"
        )

        self.assertEqual(get_current_version(), "commit-hash")

    def test_non_existing_dir(self):
        self.mocked_listdir.side_effect = FileNotFoundError

        self.assertEqual(get_current_version(), "")

    def test_empty_dir(self):
        self.mocked_listdir.return_value = []

        self.assertEqual(get_current_version(), "")

    def test_head_not_found(self):
        self.mocked_listdir.return_value = ("foo", "bar", "foobar")

        self.assertEqual(get_current_version(), "")


class BeatConfigTests(SimpleTestCase):
    @skipIf(not hasattr(settings, "CELERY_BEAT_SCHEDULE")
    def test_task_references_correct(self):
        """
        Assert that the task import paths in the Beat config are valid.
        """
        for entry in settings.CELERY_BEAT_SCHEDULE.values():
            task = entry["task"]
            with self.subTest(task=task):
                try:
                    import_string(task)
                except ImportError:
                    self.fail(
                        f"Could not import task '{task}' in settings.CELERY_BEAT_SCHEDULE"
                    )
