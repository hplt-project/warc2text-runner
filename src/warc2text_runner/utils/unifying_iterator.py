import base64
import pandas as pd


def _release2_iterator(inps, batch_size):
        readers = [
            pd.read_json(inp, orient='records', lines=True, chunksize=batch_size)
            for inp in inps]
#        import pdb; pdb.set_trace()
        for dfs in zip(*readers):
            assert all(len(dfs[i]) == len(dfs[0]) for i in range(1, len(dfs)))
            df = pd.concat(dfs, axis=1)
            # text field is 't' for stage2out, no field 't' for later stages and rename() does nothing
            df.rename(columns={'t': 'text'}, inplace=True)
            df.lang, df.text = df.lang.astype(object), df.text.astype(str)
            yield df


def _release1_warc2textout_iterator(inps, batch_size):
    assert len(inps) == 1, 'Specify only the file with base64-encoded texts! '
    reader = pd.read_csv(inps[0], sep='\t', header=None, chunksize=batch_size, names=['text'])
    for df in reader:
        df.text = df.text.apply(lambda b: base64.b64decode(b).decode('utf-8'))
        yield df


version2impl = {
    'r2': _release2_iterator,
    'r1_warc2textout': _release1_warc2textout_iterator
}


def batch_iterator(data_version, inp, batch_size=10**5):
    f = version2impl.get(data_version)
    if f is None:
        raise ValueError(f'Unsupported dataset version {data_version}, select among {version2impl.keys()}')
    f(inp, batch_size)
