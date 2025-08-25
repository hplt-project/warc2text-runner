# This script visualizes the amount of data per language family in the HPLT datasets

import argparse
import pandas as pd
import plotly.express as px

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg(
        "--stats_file",
        "-s",
        help="Dataframe with statistics",
        default="hpltv3.tsv",
    )
    arg(
        "--lang_fam_file",
        "-l",
        help="Language families file",
        default="hplt2_languages_families.tsv",
    )
    arg(
        "--data",
        "-d",
        help="What to count?",
        choices=["chars", "docs"],
        default="docs",
    )
    arg(
        "--exclude",
        "-e",
        help="Languages to exclude",
        nargs="+",
    )
    arg(
        "--output",
        "-o",
        help="Where to save?",
        default="vis/3_families_cleaned_docs.html",
    )

    args = parser.parse_args()

    stats_file = args.stats_file
    lang_fam_file = args.lang_fam_file

    lang_fam_df = pd.read_csv(lang_fam_file, sep="\t")

    stats_df = pd.read_csv(stats_file, sep="\t")
    print(stats_df)

    lang_fam_df = lang_fam_df[
        lang_fam_df["v3 Language Code (ISO 693-3+script)"].isin(stats_df["lang"].values)
    ]

    assert (
        lang_fam_df["v3 Language Code (ISO 693-3+script)"].values.all()
        == stats_df["lang"].values.all()
    )

    print(lang_fam_df)
    language_families = pd.Series(
        lang_fam_df.Family.values,
        index=lang_fam_df["v3 Language Code (ISO 693-3+script)"],
    ).to_dict()

    stats_df["family"] = stats_df.lang.apply(
        lambda x: next(
            (family for lang, family in language_families.items() if x in lang), None
        )
    )

    stats_df.lang = stats_df.lang.apply(lambda x: x.split("_")[0])

    if args.exclude:
        stats_df = stats_df.loc[~stats_df["lang"].isin(args.exclude)]
        lang_fam_df = lang_fam_df.loc[
            ~lang_fam_df["ISO693-3 code"].isin(args.exclude)
        ]

    fig = px.treemap(
        stats_df,
        path=["family", "lang"],
        values=args.data,
        hover_name=lang_fam_df["Language Name"],
    )

    # Update font size and treemap shape
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        font=dict(size=25),  # Change the font size here
    )
    fig.data[0].textinfo = "label+percent entry"  # percent {parent|root|entry}'
    # fig.data[0].textinfo = "label+text+value"  # if we want to show the real numbers instead of percentage
    # fig.show()

    fig.write_html(args.output, include_plotlyjs="directory", default_height="100%")
