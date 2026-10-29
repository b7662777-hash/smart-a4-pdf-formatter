"""Upload contract tests; image algorithms are stubbed, PDF/ZIP I/O is real."""
import asyncio
import io
import os
import shutil
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from fastapi import UploadFile
from PIL import Image

import main


class UploadTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.original_cwd = Path.cwd()
        self.workspace = tempfile.TemporaryDirectory()
        os.chdir(self.workspace.name)
        for folder in ("uploads", "processed", "output"):
            Path(folder).mkdir()
        self.groups = []
        self.stages = []

        def stage(name):
            def process(source, destination):
                self.stages.append(name)
                shutil.copyfile(source, destination)
            return process

        def layout(paths, destination):
            self.groups.append(len(paths))
            with Image.new("RGB", (32, 48), "white") as image:
                image.save(destination, "JPEG")

        for name, replacement in (
            ("fix_rotation", stage("rotation")),
            ("enhance_image", stage("enhancement")),
            ("crop_image", stage("crop")),
            ("create_a4_layout", layout),
        ):
            patcher = patch.object(main, name, replacement)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.addCleanup(self.restore_workspace)

    def restore_workspace(self):
        os.chdir(self.original_cwd)
        self.workspace.cleanup()

    def files(self, count):
        uploads = []
        for index in range(count):
            stream = io.BytesIO()
            with Image.new("RGB", (8, 8), "white") as image:
                image.save(stream, "JPEG")
            stream.seek(0)
            upload = UploadFile(file=stream, filename=f"scan-{index}.jpg")
            self.addCleanup(stream.close)
            uploads.append(upload)
        return uploads

    async def deliver(self, response):
        messages = []

        async def send(message):
            messages.append(message)

        async def receive():
            await asyncio.sleep(3600)

        scope = {
            "type": "http", "method": "POST", "path": "/upload",
            "headers": [], "asgi": {"version": "3.0", "spec_version": "2.4"},
        }
        await response(scope, receive, send)
        start = next(message for message in messages if message["type"] == "http.response.start")
        body = b"".join(message.get("body", b"") for message in messages
                        if message["type"] == "http.response.body")
        return start, body

    async def test_empty_direct_call_preserves_error_contract(self):
        self.assertEqual(main.upload_images([]), {"error": "Upload at least 1 image"})

    async def test_single_image_returns_one_pdf_zip(self):
        response = main.upload_images(self.files(1))
        start, body = await self.deliver(response)
        self.assertEqual(start["status"], 200)
        headers = dict(start["headers"])
        self.assertEqual(headers[b"content-type"], b"application/zip")
        self.assertIn(b"all_pdfs.zip", headers[b"content-disposition"])
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            self.assertEqual(archive.namelist(), ["pdf_1.pdf"])
            self.assertTrue(archive.read("pdf_1.pdf").startswith(b"%PDF-"))
        self.assertEqual(self.groups, [1])
        self.assertEqual(self.stages, ["rotation", "enhancement", "crop"])

    async def test_five_images_preserve_four_image_grouping(self):
        response = main.upload_images(self.files(5))
        _, body = await self.deliver(response)
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            self.assertEqual(archive.namelist(), ["pdf_1.pdf", "pdf_2.pdf"])
        self.assertEqual(self.groups, [4, 1])
        self.assertEqual(self.stages, ["rotation", "enhancement", "crop"] * 5)


if __name__ == "__main__":
    unittest.main()
