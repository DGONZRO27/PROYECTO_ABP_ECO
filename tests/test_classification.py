import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ecovision.application.classification import classify_image
from ecovision.domain.categories import guide_for_label
from ecovision.infrastructure.labels import read_labels


class ClassificationTests(unittest.TestCase):
    def test_paper_carton_label_maps_to_white_bin(self):
        guide = guide_for_label("Papel_Carton")

        self.assertEqual(guide.display_name, "Papel y cartón")
        self.assertEqual(guide.bin_name, "Caneca blanca")

    def test_all_supported_materials_use_the_white_bin(self):
        labels = ("Plastico", "Papel_Carton", "Metal", "Vidrio")

        self.assertTrue(all(guide_for_label(label).bin_name == "Caneca blanca" for label in labels))

    def test_classification_returns_top_class_and_alternatives(self):
        result = classify_image(
            image=object(),
            labels=("Plastico", "Papel_Carton", "Metal", "Vidrio"),
            predict=lambda _image: (0.1, 0.7, 0.15, 0.05),
        )

        self.assertEqual(result.label, "Papel y cartón")
        self.assertEqual(result.confidence, 0.7)
        self.assertEqual(result.guide.bin_name, "Caneca blanca")
        self.assertEqual(result.alternatives[0].label, "Metal")

    def test_classification_rejects_mismatched_model_output(self):
        with self.assertRaisesRegex(ValueError, "puntuaciones"):
            classify_image(
                image=object(),
                labels=("Metal", "Vidrio"),
                predict=lambda _image: (0.8,),
            )

    def test_classification_rejects_unknown_model_label(self):
        with self.assertRaisesRegex(ValueError, "no tiene una guía"):
            classify_image(
                image=object(),
                labels=("Orgánico",),
                predict=lambda _image: (1.0,),
            )

    def test_labels_are_ordered_by_numeric_index(self):
        with TemporaryDirectory() as temporary_directory:
            labels_path = Path(temporary_directory) / "labels.txt"
            labels_path.write_text("1 Papel_Carton\n0 Plastico\n", encoding="utf-8")

            self.assertEqual(read_labels(labels_path), ("Plastico", "Papel_Carton"))


if __name__ == "__main__":
    unittest.main()
