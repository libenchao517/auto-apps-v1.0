################################################################################
# 本文件存储了一个整理数据集的函数
################################################################################
# 导入模块
import os
import shutil
import pandas as pd
import datetime as dt
from pathlib import Path
################################################################################
# 整理结果类
class Make_Results:
    def __init__(self, project, index=(), methods=(), datasets=()):
        """
        初始化函数
        :param project: 项目名称
        :param index: 指标列表
        :param methods: 方法列表
        :param datasets: 数据集列表
        """
        self.project = project
        self.root = os.getcwd()
        self.analysis = os.path.join(self.root, 'Analysis')
        self.temp_file = os.path.join(self.root, 'Temp-Files')
        self.result_file = os.path.join(self.root, 'Result-Files')
        self.index = index
        self.method = methods
        self.datasets = datasets
        os.makedirs(self.temp_file, exist_ok=True)
        os.makedirs(self.result_file, exist_ok=True)

    def make(self):
        """
        控制函数
        :return: None
        """
        self.concat_datasets(self.datasets)
        results_all = self.concat_all()
        self.total_index(self.index, self.method, self.datasets, results_all)
        self.move()

    def concat_datasets(self, datasets):
        """
        按数据集汇总结果
        :param datasets: 数据集列表
        :return: None
        """
        for d in datasets:
            temp = pd.DataFrame()
            path = os.path.join(self.analysis, d)
            xlsx_list = list(map(str, list(Path(path).rglob("*.xlsx"))))
            for xlsx in xlsx_list:
                df = pd.read_excel(xlsx, header=0, index_col=0)
                temp = pd.concat([temp, df])
            xlsx_path = d + '.xlsx'
            temp.to_excel(os.path.join(self.temp_file, xlsx_path))

    def concat_all(self):
        """
        汇总所有数据集的结果
        :return: 汇总的结果
        """
        Total_Results = pd.DataFrame()
        xlsx_list = list(map(str, list(Path(self.temp_file).rglob("*.xlsx"))))
        for xlsx in xlsx_list:
            df = pd.read_excel(xlsx, header=0, index_col=0)
            Total_Results = pd.concat([Total_Results, df])
        return Total_Results

    def total_index(self, index, method, datasets, Total_Results):
        """
        按指标进行整理
        :param index: 指标列表
        :param Total_Results: 汇总的结果
        :return: None
        """
        for idx in index:
            Results = Total_Results[['Method', 'Datasets', idx]].copy()
            Results.set_index(['Method', 'Datasets'], inplace=True)
            Result = self.padding_data(Results= Results, method=method, datasets=datasets)
            with pd.ExcelWriter(os.path.join(self.result_file, idx + ".xlsx")) as writer:
                Result.to_excel(writer, sheet_name=idx)

    def padding_data(self, Results, method, datasets):
        """
        将单列表格转化为多列表格
        :param Results: 一个DataFrame表格，所有方法在所有数据集上的结果
        :param method: 方法列表
        :param data: 数据集列表
        :return: 一个DataFrame表格，每行一个方法，每列一个数据集
        """
        Result = pd.DataFrame(index=method, columns=datasets)
        for m in method:
            for d in datasets:
                try:
                    Result.loc[m, d] = Results.loc[m, d][0]
                except:
                    Result.loc[m, d] = None
        return Result

    def move(self):
        """
        将所有结果移动到指定文件夹
        :return: None
        """
        fromdir = os.getcwd()
        todir = "-".join([self.project, str(dt.date.today()), dt.datetime.now().time().strftime("%H-%M")])
        os.makedirs(todir, exist_ok=True)
        shutil.move(self.analysis, todir)
        shutil.move(self.temp_file, todir)
        shutil.move(self.result_file, todir)
        self.result_file = os.path.join(self.root, todir, "Result-Files")
        if os.path.exists(os.path.join(fromdir, "Figure")):
            shutil.move(os.path.join(fromdir, "Figure"), todir)
        if os.path.exists(os.path.join(fromdir, "log_files")):
            shutil.move(os.path.join(fromdir, "log_files"), todir)
