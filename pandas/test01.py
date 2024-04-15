import pandas as pd

def test01():
    df = pd.DataFrame({
        'name': ['张三', '李四', '王五'],
        'age': [21, 25, 30],
        'sex': ['男', '男', '女']
    })
    # 把DataFrame序列化成一个CSV文件
    df.to_csv('data.csv', index=False)
    # 把CSV文件反序列化成一个DataFrame
    new_df = pd.read_csv('data.csv')
    print(new_df)

def test02():
    df = pd.read_csv('data.csv')
    # 包含'男'的行
    male_df = df[df['sex'] == '男']
    # 将行按'age'升序排列
    sorted_df = df.sort_values(by='age')
    print(male_df)
    print(sorted_df)

def test03():
    df1 = pd.DataFrame({
        'id': [0, 1, 2],
        'name': ['张三', '李四', '王五']
    })
    df2 = pd.DataFrame({
        'id': [0, 1, 2],
        'age': [21, 25, 30]
    })
    # 基于'id'合并两个DataFrame
    merged_df = pd.merge(df1, df2, on='id')
    # 垂直叠加两个DataFrame
    concat_df = pd.concat([df1, df2], axis=1)
    print(merged_df)
    print(concat_df)

if __name__ == '__main__':
    test03()