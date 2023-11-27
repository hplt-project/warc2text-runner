from contextlib import ExitStack
import sys
import pandas as pd
from pathlib import Path

merged_df = None

release_1 = [
    'cc40',
    # 'wide00006', # wasn't used for this release
    'wide00015',
    'wide00016',
    'wide00017'
]


with ExitStack() as ctx:
    release_1_langs = frozenset(
        line.strip()
        for file in ['cld2'] + [f'{n+1}' for n in range(5)]
        for line in open(f'_langs/langs_{file}.txt')
        if line.strip() != ''
    )


names_df = pd.read_csv('_langs/code2name_cld2.tsv', header=0, sep='\t', index_col='Code')

for collection in release_1:
    stats_dir = f'{collection}_filtered_stats'
    df = pd.read_csv(Path(stats_dir) / 'stats.tsv', sep='\t', header=0)
    if merged_df is None:
        merged_df = df
    else:
        merged_df = pd.concat([merged_df, df], ignore_index=True)
    print(f"read {collection}, df is now {merged_df.size}", file=sys.stderr)

ldf = merged_df[merged_df.lang.isin(release_1_langs)]\
    .groupby("lang")\
    .agg('sum')\
    .join(names_df, validate='m:1')\
    .reset_index()\
    .sort_values('text_bytes')
cols = {
    'Name':          'Language',
    'lang':          'Code',
    'text_newlines': '\\# Segments',
    'text_wcwords':  '\\# Words',
    'text_bytes':    '\\# Bytes',
    'docs':          '\\# Documents'
}
# ldf.to_csv(sys.stdout, sep='\t', index=False)
tex_tbl = ldf[cols.keys()].to_latex(
    index=False,
    longtable=True,
    label='tab:perlang_stats',
    column_format='ll|llll',
    caption='Raw texts extracted with \\texttt{warc2text} per language using CLD2: the number of segments (new line symbols), words (as defined by \\texttt{wc(1)}), bytes and documents. Ordered by size in bytes.',
    header=[
        f'\\textbf{{{{{name}}}}}' # double escape because to_latex calls header[n].format(..)
        for name in cols.values()
    ],
    formatters={
        col: '{:0.2e}'.format
        for col in ['text_newlines', 'text_wcwords', 'text_bytes', 'docs']
    } | {
        'Name': lambda name: name.capitalize()
    })

tex_sum = '&'.join(['Total', ''] + [f"{ldf[col].sum():0.2e}" for col in ['text_newlines', 'text_wcwords', 'text_bytes', 'docs']])

# Isnert tex_sum bit
end_offset = tex_tbl.find('\\end{longtable}')
tex_tbl = tex_tbl[:end_offset] + '\\hline\n' + tex_sum + '\\\\\n\\bottomrule\n' + tex_tbl[end_offset:]

print(tex_tbl)