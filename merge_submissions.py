#!/usr/bin/env python3
import argparse
import csv
import gzip
from pathlib import Path

import utils  # for field_size_limit


def main():
    parser = argparse.ArgumentParser()
    arg = parser.add_argument
    arg('output')
    arg('inputs', nargs='+')
    arg('--skip', nargs='+')
    args = parser.parse_args()
    all_data = {}
    for path in map(Path, args.inputs):
        print('Reading {}'.format(path))
        with path.open() as f:
            reader = csv.reader(f)
            next(reader)
            all_data.update(
                ((im_id, poly_type), poly) for im_id, poly_type, poly in reader)

    with gzip.open(str(args.output), 'wt') as outf:
        writer = csv.writer(outf)
        with open('sample_submission.csv') as f:
            reader = csv.reader(f)
            header = next(reader)
            writer.writerow(header)
            for im_id, poly_type, _ in reader:
                poly = 'MULTIPOLYGON EMPTY'
                if '{}_{}'.format(im_id, poly_type) not in args.skip:
                    poly = all_data.get((im_id, poly_type)) or poly
                writer.writerow([im_id, poly_type, poly])


if __name__ == '__main__':
    main()
