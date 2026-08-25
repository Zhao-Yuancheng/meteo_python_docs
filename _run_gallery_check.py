# -*- coding: utf-8 -*-
"""逐个运行 gallery 的 13 个例子脚本，记录成功/失败与产出文件污染。"""
import os, sys, glob, subprocess, tempfile, shutil

ENV = r"D:\Code\miniforge3\envs\P312"
EX = os.path.join(ENV, "python.exe")
BASE = r"D:\Code\Vibe\meteo_python_docs"

env = dict(os.environ)
env["PYTHONNOUSERSITE"] = "1"
env["MPLBACKEND"] = "Agg"
env["PATH"] = os.pathsep.join([os.path.join(ENV, "Library", "bin"),
                               os.path.join(ENV, "Scripts"), ENV, env["PATH"]])

scripts = sorted(glob.glob(os.path.join(BASE, "examples", "plot_*", "plot_*.py")))
print(f"共 {len(scripts)} 个脚本\n")

for s in scripts:
    # 在临时目录运行，检测脚本是否向 CWD 写文件（污染）
    tmp = tempfile.mkdtemp()
    r = subprocess.run([EX, s], cwd=tmp, env=env,
                       capture_output=True, text=True, timeout=300)
    produced = []
    for root, dirs, files in os.walk(tmp):
        for f in files:
            produced.append(os.path.relpath(os.path.join(root, f), tmp))
    shutil.rmtree(tmp, ignore_errors=True)
    status = "OK " if r.returncode == 0 else "FAIL"
    print(f"[{status}] {os.path.basename(s):32s} 污染文件: {produced if produced else '无'}")
    if r.returncode != 0:
        err = (r.stderr or "").strip().splitlines()
        print("       错误:", err[-1] if err else "?")
        for ln in err[-6:-1]:
            print("        ", ln)