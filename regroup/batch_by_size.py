import pandas as pd
import fire
import os


def batches_by_size(df, size=2**30):
    res = df.groupby(df['size'].cumsum() // size).agg({'size':'sum', 'path': ' '.join})
    return res


def format_command(r, output_dir):
    output_dir = os.path.join(output_dir, str(r.batch),r.lang)
    url_paths = r.path.replace('text.gz','url.gz')
    return f'mkdir -p {output_dir}; cat {r.path} > {output_dir}/text.gz; cat {url_paths} > {output_dir}/url.gz;'
                

def main(fsizes, output_dir, size=2**30):
    df = pd.read_csv(fsizes, sep='\t', header=None, names=['size','path'])
    df['lang'] = df.path.str.split('/').str[-2]
    bf = df.groupby('lang').apply(lambda df: batches_by_size(df, size))
    bf.index.rename({'size':'batch'}, inplace=True)
    bf = bf.reset_index()

    bf.to_csv(os.path.join(output_dir, 'batches.tsv'), sep='\t', index=False)

    commands = bf.apply(lambda r: format_command(r, output_dir), axis=1)
    print('Lengths of commands:\n', commands.str.len().describe(), sep='')
    with open(os.path.join(output_dir, 'tmp.sh'),'wt', encoding='utf-8') as outp:
        outp.write('\n'.join(commands))



fire.Fire(main)


