import sys
import ctypes
dll_path = r"./hidapi.dll"
try:
    ctypes.CDLL(dll_path)
    print(f"成功手动加载 DLL: {dll_path}")
except OSError as e:
    print(f"手动加载 DLL 失败: {e}")
    sys.exit(1)
import hid
# 替换成你设备的 VID 和 PID
VID = 0x5131   # 示例，请修改为实际值
PID = 0x2007   # 示例，请修改为实际值

# 报告 ID 定义
REPORT_ID_SET_CONFIG = 0x04
REPORT_ID_GET_CONFIG = 0x04
CONFIG_DATA_LEN = 30   # 30 字节

def main():
    # 先枚举找到 Vendor Usage Page 的接口
    target_path = None
    for dev_info in hid.enumerate(VID, PID):
        if dev_info['usage_page'] == 0xFF00:
            target_path = dev_info['path']
            print(f"找到 Vendor 接口: {target_path}")
            break

    if target_path is None:
        print("未找到 Vendor Feature 接口")
        return

    # 用 path 打开指定接口
    device = hid.Device(path=target_path)
    print("设备打开成功！")

    try:
        data = bytes().fromhex("04 00 10 00 11 00 3B 77 44 5A 00 00 0A 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00")
        device.send_feature_report(data)
        print(f"配置数据: {data[1:].hex(' ')}")
        # time.sleep(1)  # 等待设备处理
        # data = device.get_feature_report(REPORT_ID_GET_CONFIG, CONFIG_DATA_LEN+1)
        # print(f"配置数据: {data[1:].hex(' ')}")
    except hid.HIDException as e:
        print(f"失败: {e}")
    finally:
        device.close()

if __name__ == "__main__":
    main()