# OmindOS Navigation · 导航与四足仿真

## Q1 ROS 2 开发代码

[Q1 ROS 2 仿真代码 0.1.0-preview.1](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/tag/q1-ros2-v0.1.0-preview.1) 将已有自研 Q1 Dynamics R2 接入原生 ROS 2，提供两个独立工作区、站立/起身/步态服务与实时状态反馈。已在 ROS 2 Jazzy 上验证；代码包需配合所有者本地的私有 Q1 模型使用。[功能、验证与安装范围](docs/Q1_ROS2_RELEASE.zh-CN.md)。

面向**差速轮式、全向轮式和四足**的导航项目。当前推荐安装包提供三维参数工作台与四足动力学仿真；轮式导航预览的独立环境见专业指南。

![差速、全向、四足三类平台示意](docs/media/platforms.svg)

## 下载 Ubuntu 安装包

**0.2.0-preview.8 · 约 681 MB · Ubuntu · Intel / AMD 64 位电脑**

工作台、ROS 2、四足策略和 MuJoCo 仿真环境已经包含在包内。**只下载这一份，无需再下载轻量工作台或独立算法包。** 首次运行需要电脑已安装 Docker Engine。

### [下载 Ubuntu 安装包 →](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.8/omindos-navigation-0.2.0-preview.8-ubuntu-amd64.tar)

[安装与首次使用指南 →](docs/GET_STARTED.zh-CN.md)

## 装好后能做什么？

- **V1.1 CAD 装配**：查看修正后的机器狗，预览全部 12 轴联动、恢复几何零位并导出标定表。
- **三维调参**：导入自己的 URDF，编辑关节、连杆和电机参数，保存配置版本。
- **运动学预览**：查看关节变化，进行点动和轨迹预览；可使用 ROS 2 预览服务。
- **四足动力学仿真**：使用 MEVIUS2 参考模型体验起身、站立、行走、转向和扰动场景。

## 工作台长什么样？

![Ubuntu 安装包实际工作台：OriginMind V1.1 装配 R1](https://github.com/maganrobotics-boop/OmindOS-Navigation-Release/releases/download/v0.2.0-preview.8/workbench.png)

**默认打开 V1.1 CAD 装配 R1：988 个实例、12 轴几何联动。** 已补齐前腿摇臂组件并修正右后摇臂位置。展开“轴线、零位与映射依据”可导出标定表；电机方向、编码器零位及机械限位仍待真机回读。

切换“关节参数调试”可导入 URDF、编辑参数、保存版本。参数页保留原 MEVIUS2 参考功能；CAD 模型和控制配置分别管理。

## 自己的参数怎么改？

1. **进入参数页**：点击“关节参数调试”，在左侧导入自己的 URDF 或完整配置文件。
2. **编辑参数**：选择关节或连杆，填写连接尺寸、限位及电机参数。
3. **写入并保存**：点击“将以上参数写入程序”，设为工作台当前配置；再保存版本或导出备份。

[查看图文操作指南 →](docs/WORKBENCH_USAGE.zh-CN.md)

## 需要登录吗？可以调用 API 吗？

**当前本地工作台无需注册或登录。** 启动后在浏览器打开 `http://127.0.0.1:8085/`，参数配置保存在本机独立数据目录，更新程序时可继续使用。

开发者可以用自己的程序调用本地 API，提交参数、保存和读取配置版本。[API 使用指南 →](docs/API_GUIDE.zh-CN.md)

**当前为预览发行，真实机器人尚未验收。** 保存参数不会使能真实电机；三维调参与四足策略仿真是独立功能。

## 更多资料

[轮式导航、Jetson 与板卡固件](docs/DEVELOPER.zh-CN.md) · [历史版本](docs/RELEASE_HISTORY.zh-CN.md) · [下载、校验与常见问题](docs/DOWNLOAD_HELP.zh-CN.md)

后续主机端开发与交付以 **Ubuntu** 为主，Windows 暂不继续开发。
