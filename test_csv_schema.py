import unittest

import pandas as pd

from csv_schema import normalize_text_dataframe, split_manual_text


class CsvSchemaTest(unittest.TestCase):
    def test_accepts_xquik_tweet_text_export(self):
        df, schema = normalize_text_dataframe(
            pd.DataFrame({"Tweet Text": ["Great launch", " ", None]})
        )

        self.assertEqual(df["text"].tolist(), ["Great launch"])
        self.assertEqual(schema.text_column, "Tweet Text")
        self.assertEqual(schema.dropped_rows, 2)

    def test_accepts_review_text_alias(self):
        df, schema = normalize_text_dataframe(
            pd.DataFrame({"review_text": ["Loved it", "Needs work"]})
        )

        self.assertEqual(df["text"].tolist(), ["Loved it", "Needs work"])
        self.assertEqual(schema.total_rows, 2)

    def test_manual_text_split_drops_blank_lines(self):
        self.assertEqual(split_manual_text("alpha\n\n beta "), ["alpha", "beta"])


if __name__ == "__main__":
    unittest.main()
