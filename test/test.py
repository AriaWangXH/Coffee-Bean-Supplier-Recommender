import sys
from os import path

sys.path.append('./src')
from train_model import get_scaler, stand_feat

import pandas as pd
from sklearn.preprocessing import StandardScaler

def test_scaler_stand_feat_1():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
    scaler = StandardScaler()
    result_true = scaler.fit_transform(df[['col1', 'col2']])

    temp = get_scaler(df, ['col1', 'col2'], './test/test_scaler.pkl')
    result_test = stand_feat(df, ['col1', 'col2'], temp)
    assert (result_true == result_test).all()


def test_scaler_stand_feat_2():
    df = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4], 'col3': [3, 4]})
    scaler = StandardScaler()
    result_true = scaler.fit_transform(df[['col1']])

    temp = get_scaler(df, ['col1'], './test_scaler.pkl')
    result_test = stand_feat(df, ['col1'], temp)
    assert (result_true == result_test).all()

