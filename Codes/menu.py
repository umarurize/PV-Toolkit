import sys

imported_modules_list =[]
for m in sys.modules:
    if str(sys.modules[m]).find('built-in') == -1:
        imported_modules_list.append(m)

while True:
    choose_num =  input('-----------------------\n请输入想要调用的功能序号\n1 - 319 IV 数据处理\n2 - 319 稳态电流数据处理\n3 - 317 EQE 数据处理\n4 - 退出程序\n：')
    if choose_num.isdigit():
        if eval(choose_num) in [1, 2, 3, 4]:
            break
        else:
            print('请输入1至4范围内的有效整数数字...')
    else:
        print('请输入有效整数数字，而不是其它...')

if eval(choose_num) == 1:
    print('-----------------------\n当前正在执行功能1 - 319 IV 处理')
    if 'iv_helper' in imported_modules_list:
        del sys.modules['iv_helper']
        import iv_helper
    else:
        import iv_helper
elif eval(choose_num) == 2:
    print('-----------------------\n当前正在执行功能2 - 319 稳态电流数据处理')
    if 'steady_current_helper' in imported_modules_list:
        del sys.modules['steady_current_helper']
        import steady_current_helper
    else:
        import steady_current_helper
elif eval(choose_num) == 3:
    print('-----------------------\n当前正在执行功能3 - 317 EQE 数据处理')
    if 'eqe_helper' in imported_modules_list:
        del sys.modules['eqe_helper']
        import eqe_helper
    else:
        import eqe_helper
else:
    print('程序结束，按任意键关闭窗口...')



