import tkinter as tk 
from tkinter import ttk 
import numpy as np 
 
class IntegratedSlopeSystem:
    
    '''
    model = 模型接入处
    '''
    
    
    def __init__(self, master):
        self.master = master 
        master.title("输电塔-边坡危险性预测智能系统 v3.1")
        master.geometry("800x600+200+100")  # 屏幕居中显示 
        
        # 初始化数据容器 
        self.data_1d = np.zeros(6)
        self.data_2d = None 
        self.prediction = None 
        
        # 界面色彩方案 
        self.setup_ui_theme()
        self.create_input_matrix()
        self.create_control_panel()
        self.create_output_console()
 
    def setup_ui_theme(self):
        """配置现代化UI主题"""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#F5F5F5")
        style.map("TButton",
                foreground=[("active", "#FFFFFF"), ("!active", "#333333")],
                background=[("active", "#4682B4"), ("!active", "#B0C4DE")])
 
    def create_input_matrix(self):
        """构建特征输入矩阵界面"""
        matrix_frame = ttk.LabelFrame(self.master, text="地质特征矩阵输入")
        matrix_frame.pack(pady=15, padx=20, fill="x")
        
        features = [
            ("周边土地情况", "1-4项"),
            ("植被类型", "1-4类"),
            ("距离(m)", ">0"),
            ("坡高(m)", ">0"), 
            ("坡度(°)", "0-90"),
            ("岩土性质", "0-3类")
        ]
        
        self.entries = []
        for idx, (label, unit) in enumerate(features):
            row = ttk.Frame(matrix_frame)
            row.grid(row=idx//2, column=idx%2, padx=15, pady=8, sticky="ew")
            
            ttk.Label(row, text=label, width=18, anchor="w").pack(side="left")
            entry = ttk.Entry(row, width=12)
            entry.insert(0, unit)
            entry.pack(side="left", padx=5)
            self.entries.append(entry)
 
    def create_control_panel(self):
        """构建智能控制面板"""
        control_frame = ttk.Frame(self.master)
        control_frame.pack(pady=15)
        
        ttk.Button(control_frame, text="数据标准化", 
                 command=self.convert_data).grid(row=0, column=0, padx=8)
        ttk.Button(control_frame, text="执行智能评估", 
                 command=self.execute_prediction).grid(row=0, column=1, padx=8)
        ttk.Button(control_frame, text="生成分析报告", 
                 command=self.generate_report).grid(row=0, column=2, padx=8)
 
    def create_output_console(self):
        """构建多模态输出控制台"""
        console_frame = ttk.LabelFrame(self.master, text="智能评估结果")
        console_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # 结果展示文本域 
        self.output_text = tk.Text(console_frame, wrap="word", font=("Consolas", 10))
        vsb = ttk.Scrollbar(console_frame, orient="vertical", command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=vsb.set)
        
        vsb.pack(side="right", fill="y")
        self.output_text.pack(fill="both", expand=True)
        
        # 初始化提示信息 
        self.output_text.insert("end", "系统初始化完成\n请按流程执行评估操作")
 
    def convert_data(self):
        """数据格式转换引擎"""
        try:
            # 数据清洗与验证 
            raw_data = []
            validators = [
                (1, 4), (1, 4), 
                (0.1, 1000), (0.1, 500), 
                (0, 90), (0, 3)
            ]
            
            for idx, entry in enumerate(self.entries):
                val = float(entry.get())
                min_val, max_val = validators[idx]
                if not (min_val <= val <= max_val):
                    raise ValueError(f"{entry.get()} 超出有效范围({min_val}-{max_val})")
                raw_data.append(val)
            
            # 构建数据矩阵 
            self.data_1d = np.array(raw_data)
            self.data_2d = self.data_1d.reshape(1, -1)
            
            # 更新状态显示 
            self.output_text.delete(1.0, "end")
            self.output_text.insert("end", 
                "数据标准化成功！\n输入特征矩阵：\n" + 
                "\n".join([f"特征{i+1}: {x:.2f}" for i, x in enumerate(self.data_1d)]))
            
        except Exception as e:
            self.output_text.delete(1.0, "end")
            self.output_text.insert("end", f"数据异常：{str(e)}")
 
    def execute_prediction(self):
        """智能评估核心算法"""
        if self.data_2d is None:
            self.output_text.insert("end", "\n错误：请先执行数据标准化！")
            return 
            
        try:
            # 模拟预测接口 
            self.prediction = self.model.predict(self.data_2d)*100
            
            # 边坡等级智能判定 
            grade_info = self.determine_slope_grade(self.prediction)
            
            # 动态生成评估结果 
            result_str = f"\n\n=== 智能评估结果 ===" 
            result_str += f"\n预测值：{self.prediction[0]:.2f}"
            result_str += f"\n边坡等级：{grade_info[0][0]}"
            result_str += f"\n处置建议：{grade_info[0][2]}"
            
            # 颜色标记配置 
            self.output_text.tag_config("alert", foreground=grade_info[0][1])
            self.output_text.insert("end", result_str, "alert")
            
        except Exception as e:
            self.output_text.insert("end", f"\n评估异常：{str(e)}")
 
    def determine_slope_grade(self, predictions):
        """边坡分级智能决策系统"""
        grade_info = []
        for pred in predictions:
            if pred > 92:
                grade = ("一级边坡", "#FF0000", "立即启动应急预案，实施加固工程")
            elif 80 <= pred <= 92:
                grade = ("二级边坡", "#FF8C00", "30日内完成工程治理方案设计")
            elif 62 <= pred < 80:
                grade = ("三级边坡", "#FFD700", "季度监测频次提升至每周一次")
            else:
                grade = ("四级边坡", "#32CD32", "保持现有监测频率（每月一次）")
            grade_info.append(grade)
        return grade_info 
 
    def generate_report(self):
        """分析报告生成模块"""
        if not self.prediction:
            self.output_text.insert("end", "\n请先执行风险评估！")
            return 
            
        report = f"""
        \n=== 输电塔-边坡灾害分析报告 === 
        生成时间：2025-03-27 20:31 
        --------------------------
        输入特征矩阵维度：{self.data_2d.shape}
        预测模型输出值：{self.prediction[0]:.2f}
        边坡稳定性等级：{self.determine_slope_grade(self.prediction)[0][0]}
        建议处置方案：{self.determine_slope_grade(self.prediction)[0][2]}
        """
        self.output_text.insert("end", report)
 
    def model_predict(self, data_2d):
        """预留模型接口（示例实现）"""
        # 此处替换为实际模型调用 
        return model.predict(data_2d)*100  # 模拟预测结果 
 
if __name__ == "__main__":
    root = tk.Tk()
    app = IntegratedSlopeSystem(root)
    root.mainloop()