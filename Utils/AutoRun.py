################################################################################
# 本文件用于实现项目的自动化运行
################################################################################
# 导入必要模块
import os
import time
import psutil
import platform
import subprocess
import datetime as dt
from pathlib import Path
from Send import Auto_Email
from Send import check_Internet
################################################################################
# 自动化运行类
class Auto_Run:
    def __init__(
        self,
        Project,
        content='Linear_UMAP',
        MRPY="Make_Results_LUMAP.py",
        lock=False,
        root_content='REUMAP',
        run_file=None,
        is_parallel=False,
        check_interval=20,
        cpu_ratio=50
    ):
        """
        初始化自动运行类
        可以自动运行某文件夹下的所有py文件或单个文件
        :param Project: 一个字符串，用于在邮件中表明项目名称
        :param content: 代码所处的路径，从根目录的下一级算起
        :param MRPY: 整理实验结果用的专门文件
        :param lock: 是否锁定邮件通知功能
        :param root_content: 根目录路径，全部代码所处的路径
        :param run_file: 运行单个文件时的文件名称
        :param is_parallel: 是否并行运行多个代码
        :param check_interval: 检查间隙
        :param cpu_ratio: 并行运行的最低CPU要求
        """
        self.Project = Project
        self.lock = lock
        self.MRPY = MRPY
        self.run_file = run_file
        self.is_parallel = is_parallel
        self.root = "/".join(Path(__file__).parts[0:Path(__file__).parts.index(root_content) + 1])
        self.path = os.path.join(self.root, content)
        self.content = content
        self.check_interval = check_interval
        self.cpu_ratio = cpu_ratio

    def Run(self):
        """
        主函数
        :return: None
        """
        self._deter_system()
        self._begin_information()
        if self.run_file is not None:
            result = subprocess.run([self.interpreter, os.path.join(self.path, self.run_file)], capture_output=False, text=True)
        else:
            self._get_list()
            if self.is_parallel:
                self._run_files_in_parallel()
            else:
                self._run_non_parallel()
        if self.MRPY is not None:
            self._make_result()
        self._end_information()

    def _begin_information(self):
        """
        项目开始时发送通知邮件
        :return: None
        """
        if check_Internet(self.lock):
            AS = Auto_Email(subject="项目开始通知")
            AS.Send_txt(txt=self.Project + "项目开始运行！")

    def _end_information(self):
        """
        项目结束时发送通知邮件
        :return: None
        """
        if check_Internet(self.lock):
            AS = Auto_Email(subject="项目结束通知")
            AS.Send_txt(txt=self.Project + "项目所有实验运行结束！")

    def _deter_system(self):
        """
        确定计算机系统和python解释器
        :return: None
        """
        self.interpreter = "python"
        if platform.system().startswith('Linux'):
            self.interpreter = "python3"

    def _get_list(self):
        """
        运行多个文件时，获取文件列表
        :return: None
        """
        self.py_list = list(map(str, list(Path(self.path).rglob("*.py"))))

    def _run_non_parallel(self):
        """
        非并行运行多个文件
        :return: None
        """
        for py in self.py_list:
            if check_Internet(self.lock):
                AS = Auto_Email(subject="实验开始通知")
                AS.Send_txt(txt=py + "实验开始运行！")
            result = subprocess.run([self.interpreter, py], capture_output=False, text=True)
            if check_Internet(self.lock):
                if result.returncode == 0:
                    AS = Auto_Email(subject="实验结束通知")
                    AS.Send_txt(txt=py + "实验顺利结束！")
                else:
                    AS = Auto_Email(subject="实验结束通知")
                    AS.Send_txt(txt=py + "实验非正常结束！")

    def _make_result(self):
        """
        通过指定文件整理产生的实验结果
        :return: None
        """
        result = subprocess.run([self.interpreter, self.MRPY], capture_output=False, text=True)

    def _check_system_resources(self):
        """
        检查系统资源
        :return: None
        """
        cpu_usage = psutil.cpu_percent(interval=self.check_interval)
        memory_info = psutil.virtual_memory()
        return cpu_usage, memory_info

    def print_system_resources(self, delta_time=300):
        """
        打印系统资源
        :param delta_time: 自动打印间隔（秒）
        :return: None
        """
        while True:
            DATE = str(dt.date.today())
            TIME = dt.datetime.now().time().strftime("%H:%M:%S")
            cpu_usage, memory_info = self._check_system_resources()
            print(DATE + " " + TIME + f" CPU Usage: {cpu_usage}%, Memory Usage: {memory_info.percent}%")
            time.sleep(delta_time)

    def path_difference(self, path1, path2):
        """
        计算相对路径
        :param path1: 根目录
        :param path2: 叶目录
        :return: 叶目录 - 根目录
        """
        # 分别拆分为列表
        parts1 = os.path.normpath(path1).split(os.sep)
        parts2 = os.path.normpath(path2).split(os.sep)
        common_length = 0
        for part1, part2 in zip(parts1, parts2):
            if part1 == part2:
                common_length += 1
            else:
                break
        # 去掉重复部分
        difference1 = parts1[common_length:]
        difference2 = parts2[common_length:]
        # 确定根路径
        diff = difference1 if len(difference1) > len(difference2) else difference2
        return os.sep.join(diff)

    def _run_file_parallel_single(self, file_path):
        """
        并行运行的单次运行
        :param file_path: 文件路径
        :return: 进程
        """
        file_name = os.path.splitext(Path(file_path).parts[-1])[0]
        DATE = str(dt.date.today())
        TIME = dt.datetime.now().time().strftime("%H:%M:%S")
        diff = os.path.split(self.path_difference(self.root, file_path))[0]
        os.makedirs(f"log_files/{diff}", exist_ok=True)
        log_file_path = f"./log_files/{diff}/{file_name}.log"
        if check_Internet(self.lock):
            AS = Auto_Email(subject="实验开始通知")
            AS.Send_txt(txt=file_path + "实验开始运行！")
        log_file = open(log_file_path, "w")
        process = subprocess.Popen([self.interpreter, file_path], stdout=log_file, stderr=log_file, text=True, encoding='utf-8')
        print(DATE + " " + TIME + f" Start Running {file_path}")
        return process

    def _check_process_list(self, process_list):
        """
        检查进程列表
        :param process_list: 正在运行的进程列表
        :return: 检查后的进程列表
        """
        DATE = str(dt.date.today())
        TIME = dt.datetime.now().time().strftime("%H:%M:%S")
        for process in process_list:
            # 如果运行结束就打印结果
            if process.poll() is not None:
                if process.poll() == 0:
                    if check_Internet(self.lock):
                        AS = Auto_Email(subject="实验结束通知")
                        AS.Send_txt(txt=process.args[1] + "实验顺利结束！")
                    print(DATE + " " + TIME + f" {process.args[1]} running successful!")
                else:
                    if check_Internet(self.lock):
                        AS = Auto_Email(subject="实验结束通知")
                        AS.Send_txt(txt=process.args[1] + "实验非正常结束！")
                    print(DATE + " " + TIME + f" {process.args[1]} error!")
                process_list.remove(process)
        return process_list

    def _run_files_in_parallel(self):
        """
        并行运行的控制函数
        :return: None
        """
        processes = []
        DATE = str(dt.date.today())
        TIME = dt.datetime.now().time().strftime("%H:%M:%S")
        # 依次运行代码
        for file_path in self.py_list:
            cpu_usage, memory_info = self._check_system_resources()
            print(DATE + " " + TIME + f" CPU Usage: {cpu_usage}%, Memory Usage: {memory_info.percent}%")
            # 检查资源
            while cpu_usage > self.cpu_ratio or memory_info.percent > self.cpu_ratio:
                time.sleep(self.check_interval)
                cpu_usage, memory_info = self._check_system_resources()
                DATE = str(dt.date.today())
                TIME = dt.datetime.now().time().strftime("%H:%M:%S")
                print(DATE + " " + TIME + f" CPU Usage: {cpu_usage}%, Memory Usage: {memory_info.percent}%")
            process = self._run_file_parallel_single(file_path)
            processes.append(process)
            processes = self._check_process_list(processes)
        # 检查进程列表
        while processes:
            processes = self._check_process_list(processes)
            time.sleep(self.check_interval)
