import os

import pandas as pd

CNN_FULL_TREE = 'CNN_FULL_TREE'
FFNN_SUMSTATS = 'FFNN_SUMSTATS'

LARGE = 'LARGE'

TARGET_NAMES = ["R_naught", "Infectious_period", 'X_transmission', 'Superspreading_individuals_fraction', 'sampling_proba', 'tree_size']

PREDICTED_NAMES = ["R_naught", "Infectious_period", 'X_transmission', 'Superspreading_individuals_fraction']


PREFIX = os.path.abspath(os.path.dirname(__file__))

ALLOWED_TREE_SIZES = (LARGE,)
ALLOWED_ENCODINGS = (CNN_FULL_TREE, FFNN_SUMSTATS)


def get_ci_tables(encoding, tree_size=LARGE, **kwargs):
    """
    Loads the tables required for CI computation (for approximated parametric bootstrap)

    :param encoding: str, one of ALLOWED_ENCODINGS

    :param tree_size: str, the size of the tree:
        currently the only accepted value is LARGE (199<#tips<501)

    :return: two pd.DataFrame, containing values for CI computation: predicted and target tables
    """
    predicted_path, target_path = get_ci_table_paths(encoding=encoding, tree_size=tree_size, **kwargs)
    return (pd.read_csv(predicted_path, compression='xz', header=None, names=PREDICTED_NAMES),
            pd.read_csv(target_path, compression='xz', header=None, names=TARGET_NAMES))


def get_ci_table_paths(encoding, tree_size=LARGE, **kwargs):
    """
    Returns the paths to the tables required for CI computation (for approximated parametric bootstrap)

    :param encoding: str, one of ALLOWED_ENCODINGS

    :param tree_size: str, the size of the tree:
        currently the only accepted value is LARGE (199<#tips<501)

    :return: tuple containing the paths to the tables containing values for CI computation: predicted and target
    """
    if tree_size not in ALLOWED_TREE_SIZES:
        raise ValueError('Tree size must be one of: {}'.format(', '.join(ALLOWED_TREE_SIZES)))
    if encoding not in ALLOWED_ENCODINGS:
        raise ValueError('Encoding must be one of: {}'.format(', '.join(ALLOWED_ENCODINGS)))
    tree_size = tree_size.lower()
    return (os.path.join(PREFIX, tree_size, '{}.csv.xz'.format(encoding)),
            os.path.join(PREFIX, tree_size, 'target.csv.xz'))


def main():
    """
    Entry point, calling :py:func:`phylodeep_data_bdss.get_ci_table_paths`  with command-line arguments.
    :return: void
    """
    import argparse

    parser = argparse.ArgumentParser(description="Constructs the paths to the tables required for CI computation"
                                                 " (for approximated parametric bootstrap).",
                                     prog='bdss_ci_paths')

    parser.add_argument('-s', '--tree_size',
                        help="input tree size, can only be {} (200-500 tips).".format(LARGE),
                        type=str, required=True, choices=ALLOWED_TREE_SIZES, default=LARGE)

    parser.add_argument('-e', '--encoding', help="input tree encoding",
                        type=str, required=True, choices=ALLOWED_ENCODINGS,
                        default=CNN_FULL_TREE)

    params = parser.parse_args()

    print(get_ci_table_paths(**vars(params)))


if '__main__' == __name__:
    main()
