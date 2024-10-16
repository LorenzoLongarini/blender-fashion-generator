# blender-fashion-generator
Python script to generate train and test set to train NeRF.

create bleder venv
```python -m venv blender``` or ```py -x.y -m venv blender```
```.\blender\Scripts\activate.bat```
```pip install -r requirements.txt```

start with blender:
```add Blender Development plugin to VSCode```
```Ctrl+Shift+P```
```Blender: Start```
```move to main.py```
```Ctrl+Shift+P```
```Blender: Run Script```

create nerf venv
```conda create --name nerfstudio -y python=3.8```
```conda activate nerfstudio```
```python -m pip install --upgrade pip```
move from project dir into C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build, then run:
```.\vcvarsall.bat x64 -vcvars_ver=14.29```

now:
```pip uninstall torch torchvision functorch tinycudann```
```pip install torch==2.1.2+cu118 torchvision==0.16.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118```
```conda install -c "nvidia/label/cuda-11.8.0" cuda-toolkit ```
```pip install git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch ```
```pip install nerfstudio```


```conda remove -n ENV_NAME --all  ```

